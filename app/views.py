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
    if(room_code == None):
        room_code = checkout_room_code()
        GameMap[room_code] = Game(room_code)
    player_id = room_code + player_name
    join_room(player_id)
    GameMap[room_code].add_player(player_id, player_name)
    # TODO handle error if same name.
    player_names = [player.get_name() for player in GameMap[room_code].players]
    for player in GameMap[room_code].players:
        print(player.get_id())
        socketio.emit('add_player_to_list', {"player_name":player_names,
                      "room_code":room_code}, room=player.get_id())

@socketio.on('start_game')
def start_game(room_code):
    game = GameMap[room_code]
    game.load_word_set("movies")
    current_player, choices = game.start_new_turn()
    other_players = game.get_other_players(current_player)
    for player_id in other_players:
        print(current_player.get_name())
        socketio.emit('start_round',
                        {"current_player":current_player.get_name()},
                        room=player_id)
    print(current_player.get_id())    
    socketio.emit('start_player_turn', {"current_player":current_player.get_name(), "choices":choices},
                    room="ABCDjess")


@socketio.on('choosen_word')
def choosen_word(choosen_word, room_code):
    GameMap[room_code].choose_word(choosen_word)