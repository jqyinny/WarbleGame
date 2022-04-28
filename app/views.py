from flask import render_template, request, redirect
from flask_socketio import join_room
from app import app, socketio
from .dal import checkout_room_code
from warble.game import Game

# TODO add read/write mutex
# Roomcode to Game
GameMap = {}

@app.route('/', methods = ['GET', 'POST'])
def render_game():
    return render_template('game.html')

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
def start_game(room_code):
    game = GameMap[room_code]
    game.load_word_set("movies")
    choices = game.start_new_turn() 
    socketio.emit('start_round',
                    {"current_player":game.get_current_player_name(), "choices":choices},
                    room=room_code)

@socketio.on('choose_word')
def choose_word(choosen_word, room_code):
    game = GameMap[room_code]
    game.choose_word(choosen_word)
    socketio.emit('choosen_word', {"choosen_word": choosen_word, "current_player":game.get_current_player_name()},
                  room = room_code)

@socketio.on('send_chat')
def send_chat(msg, room_code, player_name):
    game = GameMap[room_code]
    socketio.emit('recieve_messages', {"msg": msg, "messenger_name":player_name, "points":game.answer(msg, player_name)},
                  room = room_code)
