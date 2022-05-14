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
        self.turn_number = -1
        self.wordset = []
        self.current_turn = Turn()
        self.num_rounds = 0

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
        # Update turn number
        self.turn_number += 1
        self.current_turn.reset(self.turn_number%len(self.players))
        choices = self.get_word_choices()
        return choices
        
    def load_settings(self, wordset, num_rounds, round_duration):
        self.wordset = wordset
        self.num_rounds = num_rounds

    def get_word_choices(self):
        return random.sample(self.wordset, 3)

    def choose_word(self, choosen_word):
        self.current_turn.word = choosen_word

    def get_current_player_name(self):
        return self.players[self.current_turn.current_player_index].name

    def get_current_player_id(self):
        return self.players[self.current_turn.current_player_index].sid
    
    def already_answered(self, name):
        return name in self.current_turn.answered

    def answer(self, answer, name):
        word_picked = self.current_turn.word != ""
        correct = self.current_turn.word == answer
        if(word_picked and correct):
            points = 100
            next(player for player in self.players if player.name == name).award_points(points)
            self.players[self.current_turn.current_player_index].award_points(50)
            self.current_turn.answered.append(name)
            return points
        return 0

    def all_players_answered(self):
        return len(self.current_turn.answered) == (len(self.players) - 1)

    def game_over(self):
        return self.get_round_num() == self.num_rounds

    def reset(self):
        self.turn_number = -1
        for player in self.players:
            player.points = 0
    
    def get_round_num(self):
        return self.turn_number/len(self.players)
    
    def get_winner(self):
        return max(self.players).name

class Turn:
    def __init__(self):
        self.current_player_index = 0
        self.word = ""
        self.answered = []

    def reset(self, index):
        self.word = ""
        self.answered = []
        self.current_player_index = index

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.points = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.points > other.points

    def award_points(self, points):
        self.points += points
