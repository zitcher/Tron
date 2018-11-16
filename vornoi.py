from collections import deque
from tronproblem import TronProblem


class Cell:
    def __init__(self, type, owner, turn):
        self.type = type
        self.owner = owner
        self.turn = turn


class Vornoi:
    def __init__(self):
        self.bad_set = set(['x', '#'])
        self.ties = set()
        self.actions = {0: "D", 1: "U", 2: "R", 3: "L"}

    def board_to_cells(self, board):
        cell_board = []
        for r in board:
            cell_board.append([])
            for element in r:
                cell_board[-1].append(Cell(element, None, float('inf')))

        return cell_board

    def calc(self, state, player):
        self.ties = set()
        scores = [0, 0]
        armor = 2 if state.player_has_armor(player) else 0

        board = self.board_to_cells(state.board)
        playerLocs = state.player_locs
        opp = 0 == player

        ptm_location = playerLocs[player]
        board[ptm_location[0]][ptm_location[1]].owner = player

        opp_location = playerLocs[opp]
        board[opp_location[0]][opp_location[1]].owner = opp

        fringe = deque()
        fringe.append(ptm_location)
        fringe.append(opp_location)

        while(len(fringe) != 0):
            cell_location = fringe.popleft()
            cell = board[cell_location[0]][cell_location[1]]
            scores[cell.owner] += self.expand(fringe, board, cell_location)

        if scores[player] - scores[opp] > 0:
            return scores[player] - scores[opp] + armor
        return scores[player] + armor

    def expand(self, fringe, board, cell_location):
        total = 0
        player = board[cell_location[0]][cell_location[1]].owner
        for pos in self.get_list_adjacent(cell_location):
            new_cell = board[pos[0]][pos[1]]
            if pos in self.ties or not self.expandable(new_cell, player):
                continue

            total += 1
            if new_cell.owner is None:
                new_cell.owner = player
                fringe.append(pos)
            else:
                self.ties.add(pos)

        return total

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
            if not (
                element == "#" or
                (element == "x" and not has_armor) or
                element == "1" or
                element == "2"
            ):
                safe.append(self.actions[i])
        return safe
