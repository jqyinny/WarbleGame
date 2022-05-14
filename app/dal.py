from threading import Thread, Lock
roomlist = ["A", "B", "C", "D", "E", "F"]

# TODO add read/write mutex
# Roomcode to Game
GameMap = {}
mutex = Lock()

def checkout_room_code():
    # TODO lock roomlist. Add logic to remove empty and finished games
    return roomlist.pop()

def get_game(key):
    return GameMap[key]