#!/usr/bin/python

import numpy as np
from tronproblem import TronState, TronProblem
from trontypes import CellType, PowerupType
import random
import math
import boardparser

# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    """ Write your student bot here"""
    def __init__(self):
        self.parser = boardparser.Parser()

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        state = asp.get_start_state()
        board = state.board
        player = state.player_to_move()
<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
<<<<<<< edfd4a9aecbb277acc8fe6b4454d792f6eb4be36
=======
>>>>>>> parser speed edits
        player_armour = 1 if state.player_has_armor(player) else 0
        player_speed = state.get_remaining_turns_speed(player)
        opp_armour = 1 if state.player_has_armor(1 - player) else 0
        self.parser.parse_board(board, player, player_armour, player_speed, opp_armour)
<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
=======
        print("PLAYER", player)
        p1_armour = 1 if state.player_has_armor(0) else 0
        p1_speed = state.get_remaining_turns_speed(0)
        p2_armour = 1 if state.player_has_armor(1) else 0
        p2_speed = state.get_remaining_turns_speed(1)
        self.parser.parse_board(board, player, p1_armour, p1_speed, p2_armour, p2_speed)
>>>>>>> Parser
=======
>>>>>>> parser speed edits
        return "U"

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass


class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
