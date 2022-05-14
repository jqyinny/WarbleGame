from flask import render_template, request
from flask_socketio import join_room
from app import app, socketio
from .dal import checkout_room_code, GameMap
from warble.game import Game
import json

wordset = json.load(open('app/wordsets.json'))

@app.route('/', methods = ['GET', 'POST'])
def render_game():
    return render_template('game.html')

# TODO handle how to add players when game already starts
@socketio.on('add_player')
def add_player(player_name, room_code):
    if(room_code == None or room_code == ""):
        room_code = checkout_room_code()
        GameMap[room_code] = Game(room_code)
    join_room(room_code)
    GameMap[room_code].add_player(request.sid, player_name)
    # TODO handle error if same name.
    player_names = [player.name for player in GameMap[room_code].players]
    socketio.emit('add_player_to_list', {"player_name":player_names, "room_code":room_code}, room=room_code)

@socketio.on('start_game')
def start_game(room_code, wordset_choice):
    game = GameMap[room_code]
    # TODO give options to players
    game.load_settings(wordset[wordset_choice], num_rounds=3, round_duration=30)
    game.reset()
    choices = game.start_new_turn() 
    socketio.emit('start_turn',
                    {"current_player":game.get_current_player_name(), "choices":choices, "round_num":game.get_round_num(), "total_num_rounds":game.num_rounds, "duration":game.duration},
                    room=room_code)

@socketio.on('choose_word')
def choose_word(choosen_word, room_code):
    game = GameMap[room_code]
    game.choose_word(choosen_word)
    socketio.emit('choosen_word', {"choosen_word": choosen_word, "current_player":game.get_current_player_name()},
                  room = room_code)
    socketio.sleep(game.duration)
    player_names = [player.name for player in game.players]
    scores = [player.points for player in game.players]
    socketio.emit('turn_over', {"player_names":player_names, "scores":scores}, room = room_code)

@socketio.on('send_chat')
def send_chat(msg, room_code, player_name):
    game = GameMap[room_code]
    # Players who answered correctly are not allowed to chat
    if(game.already_answered(player_name) or game.get_current_player_name() == player_name):
        return
    points = game.answer(msg, player_name)
    socketio.emit('recieve_messages', {"msg": msg, "messenger_name":player_name, "points":points},
                  room = room_code)
    # End turn
    if(game.all_players_answered()):
        player_names = [player.name for player in GameMap[room_code].players]
        scores = [player.points for player in GameMap[room_code].players]
        socketio.emit('turn_over', {"player_names":player_names, "scores":scores}, room = room_code)

@socketio.on('next_turn')
def next_turn(room_code):
    game = GameMap[room_code]
    if(game.game_over()):
            game.players.sort()
            player_names = [player.name for player in GameMap[room_code].players]
            scores = [player.points for player in GameMap[room_code].players]
            socketio.emit('game_over', {"player_names":player_names, "scores":scores, "winner":game.get_winner()}, room = room_code)
    else:
        choices = game.start_new_turn() 
        socketio.emit('start_turn',
                        {"current_player":game.get_current_player_name(), "choices":choices, "round_num":game.get_round_num(), "total_num_rounds":game.num_rounds, "duration":game.duration},
                        room=room_code)

@socketio.on('get_wordset_set')
def get_wordset_set():
    socketio.emit("populate_wordset_options", {"wordset_set": list(wordset.keys())})