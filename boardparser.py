import numpy as np


# np.set_printoptions(threshold=np.nan)
# size of 2604
class Parser(object):
    def __init__(self):
        self.p1_types = dict()
        self.p2_types = dict()
        self.init_types_p1()
        self.init_types_p2()

        assert(len(self.p1_types) == len(self.p2_types))
        self.num_cell_types = len(self.p1_types)
        self.input_size = None
        self.row_size = None
        self.col_size = None

    def init_types_p1(self):
        self.p1_types["#"] = 0
        self.p1_types["x"] = 1
        self.p1_types[" "] = 2
        self.p1_types["*"] = 3
        self.p1_types["^"] = 4
        self.p1_types["!"] = 5
        self.p1_types["@"] = 6
        self.p1_types["1"] = 7
        self.p1_types["2"] = 8

    def init_types_p2(self):
        self.p2_types["#"] = 0
        self.p2_types["x"] = 1
        self.p2_types[" "] = 2
        self.p2_types["*"] = 3
        self.p2_types["^"] = 4
        self.p2_types["!"] = 5
        self.p2_types["@"] = 6
        self.p2_types["1"] = 8
        self.p2_types["2"] = 7


    def parse_board(self, board, player, player_armour, player_speed, opp_armour):
        types = None
        if player == 0:
            types = self.p1_types
        elif player == 1:
            types = self.p2_types

        row_size = len(board)
        col_size = len(board[0])

        numpy_board = np.zeros((len(self.p1_types), row_size, col_size))

        for i, row in enumerate(board):
            for j, element in enumerate(row):
                channel = types[element]
                numpy_board[channel, i, j] = 1

        metadata = np.zeros(3)
        metadata[0] = player_armour
        metadata[1] = player_speed
        metadata[2] = opp_armour

        return numpy_board, metadata


class BoardStringParser(object):
    def __init__(self):
        self.p1_types = dict()
        self.p2_types = dict()
        self.init_types_p1()
        self.init_types_p2()

        assert(len(self.p1_types) == len(self.p2_types))
        self.num_cell_types = len(self.p1_types)
        self.input_size = None
        self.row_size = None
        self.col_size = None

    def init_types_p1(self):
        self.p1_types["#"] = "#"
        self.p1_types["x"] = "x"
        self.p1_types[" "] = " "
        self.p1_types["*"] = "*"
        self.p1_types["^"] = "^"
        self.p1_types["!"] = "!"
        self.p1_types["@"] = "@"
        self.p1_types["1"] = "p"
        self.p1_types["2"] = "o"

    def init_types_p2(self):
        self.p2_types["#"] = "#"
        self.p2_types["x"] = "x"
        self.p2_types[" "] = " "
        self.p2_types["*"] = "*"
        self.p2_types["^"] = "^"
        self.p2_types["!"] = "!"
        self.p2_types["@"] = "@"
        self.p2_types["1"] = "o"
        self.p2_types["2"] = "p"

    def init_input_size(self, board):
        self.row_size = len(board)
        self.col_size = len(board[0])

    def parse_board(self, board, player, player_armour, player_speed, opp_armour):
        types = None
        if player == 0:
            types = self.p1_types
        elif player == 1:
            types = self.p2_types

        string_rep = ""
        for row in board:
            for element in row:
                string_rep += types[element]

        string_rep += player_armour
        string_rep += player_speed
        string_rep += opp_armour

        return string_rep
