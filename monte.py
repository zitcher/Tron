import vornoi

class node():
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parent = parent
        self.children = []
        self.last_player_to_move = state.player_to_move()
        self.valid_moves = TronProblem.get_safe_actions(state, vornoi.find_player_loc(state, "1", "2")[int(state.player_to_move()) -1]
        self.win_count = 0
        self.game_count = 0

    def sort_child_nodes(self):
        return sort(self.children, key= lamba x: (x.win_count/x.game_count) + sqrt(2*log(self.game_count)/c.game_count))

    def move_counters(game_result):
        self.win_count += game_result
        self.visit += 1

    def make_new_game_state(self, move, state):
        new_node = node(move, self, state)
        self.children.append(new_node)
        self.available_actions.remove(move)
        return new_node


def monte_carlo(root, number_iterations):
    monte_workhorse(root.start_state, number_iterations)

def monte_workhorse(root_board, number_iterations):
    curr_node = node(root_board)
    for i in range(number_iterations):

        while()
