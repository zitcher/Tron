#!/usr/bin/python

import numpy as np
import random
import time
import boardparser
from vornoi import Vornoi
from adversarialsearch import alpha_beta_cutoff

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
        vornoi_solver = Vornoi()
        move = alpha_beta_cutoff(asp, 6, vornoi_solver.calc, vornoi_solver.get_safe_actions)
        state = asp.get_start_state()
        player = state.ptm
        print("PLAYER", asp.get_start_state().ptm, "MOVE", move, "SAFE MOVES", vornoi_solver.get_safe_actions(state, player, state.board, state.player_locs[player]))
        return move

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


class VornoiBot:
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
        vornoi_solver = Vornoi()

        state = asp.get_start_state()
        player = state.ptm
        safe_moves = list(asp.get_safe_actions(state.board, state.player_locs[player]))
        new_states = [asp.transition(state, move) for move in safe_moves]

        start = time.time()
        scored = [vornoi_solver.calc(nstate, player) for nstate in new_states]
        end = time.time()
        print(end - start)

        if len(scored) == 0:
            return "U"

        return safe_moves[np.argmax(scored)]

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
