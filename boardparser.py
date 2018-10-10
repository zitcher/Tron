import numpy as np


# np.set_printoptions(threshold=np.nan)
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

    def init_input_size(self, board):
        self.row_size = len(board)
        self.col_size = len(board[0])
        self.input_size = self.row_size * self.col_size * self.num_cell_types

<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
<<<<<<< edfd4a9aecbb277acc8fe6b4454d792f6eb4be36
    def parse_board(self, board, player, player_armour, player_speed, opp_armour):
=======
    def parse_board(self, board, player, p1_armour, p1_speed, p2_armour, p2_speed):
>>>>>>> Parser
=======
    def parse_board(self, board, player, player_armour, player_speed, opp_armour):
>>>>>>> parser speed edits
        types = None
        if player == 0:
            types = self.p1_types
        elif player == 1:
            types = self.p2_types

        if self.input_size is None:
            self.init_input_size(board)

<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
<<<<<<< edfd4a9aecbb277acc8fe6b4454d792f6eb4be36
=======
        print(self.col_size)
        print(self.num_cell_types)

>>>>>>> Parser
=======
>>>>>>> parser speed edits
        numpy_board = np.zeros(self.input_size)
        for i, row in enumerate(board):
            for j, element in enumerate(row):
                index = i * self.col_size * self.num_cell_types + j * self.num_cell_types + types[element]
                numpy_board[index] = 1

<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
<<<<<<< edfd4a9aecbb277acc8fe6b4454d792f6eb4be36
=======
>>>>>>> parser speed edits
        metadata = np.zeros(3)
        metadata[0] = player_armour
        metadata[1] = player_speed
        metadata[2] = opp_armour
<<<<<<< 39542a8fa0a7571f1c8fe0b8c2d963a99f8ef901
=======
        metadata = np.zeros(4)
        metadata[0] = p1_armour
        metadata[1] = p1_speed
        metadata[2] = p2_armour
        metadata[3] = p2_speed
>>>>>>> Parser
=======
>>>>>>> parser speed edits

        numpy_board = np.append(numpy_board, metadata)
        return numpy_board
