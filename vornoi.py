from collections import deque
import math


class Cell:
    def __init__(self, type, owner, turn):
        self.type = type
        self.owner = owner
        self.turn = turn


class Vornoi:
    def __init__(self):
        self.armor = set(['x', '1', '2'])
        self.bad_set = set(['x', '#', '1', '2'])
        self.good_set = set(['*', '@', '!'])
        self.ties = set()
        self.actions = {0: "D", 1: "U", 2: "R", 3: "L"}
        self.fringe = deque()

    def board_to_cells(self, board):
        cell_board = []
        for r in board:
            row = []
            for element in r:
                row.append(Cell(element, None, math.inf))
            cell_board.append(row)

        return cell_board

    def calc(self, state, player):
        self.ties = set()

        scores = [0, 0]
        armor = 3 if state.player_has_armor(player) else 0

        board = self.board_to_cells(state.board)
        playerLocs = state.player_locs

        opp = 0 == player
        opp_armor = 3 if state.player_has_armor(opp) else 0

        ptm_location = playerLocs[player]
        board[ptm_location[0]][ptm_location[1]].owner = player

        opp_location = playerLocs[opp]
        board[opp_location[0]][opp_location[1]].owner = opp

        self.fringe = deque()
        self.fringe.append(ptm_location)
        self.fringe.append(opp_location)

        while(self.fringe):
            cell_location = self.fringe.popleft()
            cell = board[cell_location[0]][cell_location[1]]
            scores[cell.owner] += self.expand(board, cell_location)

        return scores[player] - scores[opp] + armor - opp_armor

    def expand(self, board, cell_location):
        total = 0
        player = board[cell_location[0]][cell_location[1]].owner
        for pos in self.get_list_adjacent(cell_location):
            new_cell = board[pos[0]][pos[1]]
            if pos in self.ties or not self.expandable(new_cell, player):
                continue

            total += self.value(new_cell)
            if new_cell.owner is None:
                new_cell.owner = player
                self.fringe.append(pos)
            else:
                self.ties.add(pos)

        return total

    def value(self, cell):
        if cell.type in self.good_set:
            return 2
        elif cell.type == "^":
            return 0.5
        return 1

    def expandable(self, cell, player):
        return cell.type not in self.bad_set and cell.owner != player

    def get_list_adjacent(self, pos):
        '''
        returns pos in D U R L order
        '''
        x = pos[0]
        y = pos[1]
        return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))

    def get_safe_actions(self, has_armor, board, loc):
        safe = []
        for i, pos in enumerate(self.get_list_adjacent(loc)):
            element = board[pos[0]][pos[1]]
            if (
                (element in self.armor and has_armor) or
                element not in self.bad_set
            ):
                safe.append(self.actions[i])
        return safe
