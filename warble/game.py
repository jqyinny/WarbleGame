# -*- coding: utf-8 -*-

import os
import random

class Game:
    def __init__(self, game_id):
        """
        :param game_id:
        :param score_max_distance: The max distance above which player scores will be null
        :param leaderboard_answer_count: How many answers are used to compute user scores in the leaderboard
        :param max_response_time: The time given to a player to answer a question
        :param between_turns_duration: The time between two turns
        :return:
        """
        self.game_id = game_id
        self.players = []
        self.turn_number = 0
        self.wordset = []
        self.current_round = Round()

    def add_player(self, player_id, player_name):
        self.players.append(Player(player_id, player_name))

    def remove_player(self, player_id):
        # Get the player corresponding to the given sid and remove it if it is found
        player = self.get_player(player_id)

        if player:
            self.players.remove(player)

    def get_other_players(self, current_player):
        return [player.get_id() for player in self.players if player != current_player]

    def start_new_turn(self):
        # Reset answers for this turn
        self.answers = []

        current_player = self.players[self.turn_number%len(self.players)]
        choices = self.get_word_choices()
        # Update turn number
        self.turn_number += 1

        return current_player, choices
        
    # TODO add wordset options
    def load_word_set(self, wordset):
        with open("warble/words/"+wordset+".txt") as f:
            self.wordset = f.readlines()
            f.close()

    def get_word_choices(self):
        word_choices = []
        word_choices.append(random.choice(self.wordset))
        word_choices.append(random.choice(self.wordset))
        word_choices.append(random.choice(self.wordset))
        return word_choices

    def choose_word(self, choosen_word):
        self.curr

class Round:
    def __init__(self):
        self.sid = ""
        self.name = ""
        self.answers = {}
        self.results = {}



class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
