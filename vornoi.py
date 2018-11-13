from collections import deque
import sys

class vornoi:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
    def mark_squares_with_distance(self, board, player1, player2):
        self.player1_score = 0
        self.player2_score = 0
        playerLocs = self.find_player_loc(board, player1, player2)
        dist_board = []
        for row in range(len(board)):
            dist_board.append([])
            for col in range(len(board[0])):
                dist_board[row].append([])
                dist_board[row][col].append(board[row][col])
                dist_board[row][col].append(float('inf'))
                dist_board[row][col].append('w')
        dist_board[playerLocs[0][0]][playerLocs[0][1]][2] = 'O'
        dist_board[playerLocs[1][0]][playerLocs[1][1]][2] = 'T'
        dist_board[playerLocs[0][0]][playerLocs[0][1]][1] = 0
        dist_board[playerLocs[1][0]][playerLocs[1][1]][1] = 0
        queue1 = deque()
        queue2 = deque()
        queue1.append(playerLocs[0])
        queue2.append(playerLocs[1])
        while(len(queue1) != 0 or len(queue2) != 0):
            if len(queue1) != 0:
                self.check_and_push_adjacent(dist_board, queue1, player1)
            if len(queue2) != 0:
                self.check_and_push_adjacent(dist_board, queue2, player2)
        self.printy_time(dist_board)
        return(self.player1_score, self.player2_score)




    def check_and_push_adjacent(self, dist_board, queue, player):
        next_level = deque()
        while(len(queue) != 0):
            curr = queue.popleft()
            curr_square = self.get_square(dist_board, curr)
            list_adjacents = self.get_list_adjacent(curr)
            for pos in list_adjacents:
                square_to_check = self.get_square(dist_board, pos)
                self.mark_with_dist_and_player(curr_square, square_to_check, player, pos, next_level)
        for pos in next_level:
            queue.append(pos)

    def get_list_adjacent(self, pos):
        x = pos[0]
        y = pos[1]
        return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))

    def printy_time(self, board):
        for i in range(len(board)):
            row = []
            for j in range(len(board[0])):
                row.append(board[i][j][2])
            print row


    def get_square(self, board, pos):
        return board[pos[0]][pos[1]]

    def mark_with_dist_and_player(self, curr_square, square_to_check, player, pos, next_level):

        if(square_to_check[0] != '#'):
            if square_to_check[2] != curr_square[2] and square_to_check[2] != 'n':
                if(square_to_check[2] == 'w'):
                    self.augment_score(player)
                    square_to_check[1] = curr_square[1] + 1
                    square_to_check[2] = str(player)
                    next_level.append(pos)
                elif(square_to_check[1] == curr_square[1] + 1):
                    if(curr_square[2] != 'n'):
                        self.augment_score(player)
                    square_to_check[2] = 'n'

    def augment_score(self, player):
        if(player == 1):
            self.player1_score += 1
        if(player == 2):
            self.player2_score += 1
    @staticmethod
    def find_player_loc(, board, player1, player2):
        player1_tuple = (None, None)
        player2_tuple = (None, None)
        for row in range(len(board)):
            for square in range(len(board[row])):
                if board[row][square] == str(player1) :
                    player1_tuple = (row, square)
                if board[row][square] == str(player2):
                    player2_tuple = (row, square)
                if player1_tuple[0] != None and player2_tuple[0] != None:
                    return (player1_tuple, player2_tuple)

def check_vernoi(board_with_move_list, player, player1, player2):
    max = 0
    my_vornoi = vornoi()
    for board in board_list:
        board_result = my_vornoi.mark_squares_with_distance(board[0], player1, player2)[player -1]
        if(board_result > max):
            max = board_result


myboard = ( ('#', '#', '#', '#', '#', '#'),
            ('#', ' ', '1', ' ', ' ', '#'),
            ('#', '#', ' ', '#', ' ', '#'),
            ('#', ' ', ' ', '#', ' ', '#'),
            ('#', ' ', ' ', '#', ' ', '#'),
            ('#', ' ', '2', '#', ' ', '#'),
            ('#', ' ', '#', '#', ' ', '#'),
            ('#', ' ', ' ', ' ', ' ', '#'),
            ('#', ' ', ' ', ' ', ' ', '#'),
            ('#', ' ', ' ', ' ', ' ', '#'),
            ('#', '#', '#', '#', '#', '#')
            )
mine = vornoi()
print(mine.mark_squares_with_distance(myboard, 1, 2))
