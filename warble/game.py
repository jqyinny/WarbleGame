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
        self.current_round = None

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
        self.current_round = Round(self.turn_number%len(self.players))
        choices = self.get_word_choices()
        # Update turn number
        self.turn_number += 1
        return choices
        
    # TODO add wordset options
    def load_word_set(self, wordset):
        with open("warble/words/"+wordset+".txt") as f:
            self.wordset = f.readlines()
            f.close()

    def get_word_choices(self):
        return random.sample(self.wordset, 3)

    def choose_word(self, choosen_word):
        self.current_round.word = choosen_word

    def get_current_player_name(self):
        return self.players[self.current_round.current_player_index].name

    def get_current_player_id(self):
        return self.players[self.current_round.current_player_index].sid
    
    def answer(self, answer, name):
        word_picked = self.current_round.word != ""
        correct = self.current_round.word == answer
        not_answered = name in self.current_round.answered
        if(word_picked and correct and not_answered):
            points = 100
            next(player for player in self.players if player.name == name).award_points(points)
            return points
        return 0

class Round:
    def __init__(self, index):
        self.current_player_index = index
        self.word = ""
        self.answered = {}
        self.results = {}

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.points = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.name == other.name

    def award_points(self, points):
        self.points += points
