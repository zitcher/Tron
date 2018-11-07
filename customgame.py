from tronproblem import TronProblem
import random
import boardparser
import copy


class CustomGame:
    def __init__(self):
        self.maps = ["./maps/joust.txt", "./maps/divider.txt", "./maps/hunger_games.txt", "./maps/maze.txt"]
        self.reset()

    def get_game_problem(self):
        return copy.deepcopy(self.game)

    def player_to_move(self):
        return self.state.ptm

    def reset(self):
        self.game = TronProblem(random.choice(self.maps), 0)
        self.state = self.game.get_start_state()
        self.available_actions = sorted(list(self.game.get_available_actions(None)))
        self.num_to_action, self.action_to_num = self.build_num_to_action()
        self.parser = boardparser.Parser()
        self.visualizer = TronProblem.visualize_state

    def build_num_to_action(self):
        num_to_action = dict()
        action_to_num = dict()
        for i, action in enumerate(self.available_actions):
            num_to_action[i] = action
            action_to_num[action] = i

        return num_to_action, action_to_num

    def take_num_action(self, action, player):
        assert(player == self.game.get_start_state().player_to_move())
        assert(not self.game_over())
        assert(self.state == self.game.get_start_state())
        action = self.num_to_action[action]
        self.state = self.game.transition(self.state, action)
        self.game.set_start_state(self.state)

    def take_action(self, action, player):
        assert(player == self.game.get_start_state().player_to_move())
        assert(not self.game_over())
        assert(self.state == self.game.get_start_state())
        self.state = self.game.transition(self.state, action)
        self.game.set_start_state(self.state)

    def see_num_action_result(self, action, player):
        assert(player == self.state.player_to_move() and not self.game.is_terminal_state(self.state))
        action = self.num_to_action[action]
        self.state = self.game.transition(self.state, action)

    def rewind(self):
        self.state = self.game.get_start_state()
        self.game.set_start_state(self.game.get_start_state())

    def get_random_safe_move(self, player):
        avail = self.game.get_safe_actions(self.state.board, self.state.player_locs[player])
        if len(avail) == 0:
            return 0
        return self.action_to_num[random.sample(avail, 1)[0]]

    def game_over(self):
        return self.game.is_terminal_state(self.game.get_start_state())

    def state_over(self):
        return self.game.is_terminal_state(self.state)

    def score_state(self, player):
        if self.state_over():
            if self.game.evaluate_state(self.state)[player] == 1:
                return 100
            else:
                return -100
        return 1

    def get_results(self):
        return self.game.evaluate_state(self.game.get_start_state())

    def get_game_parsed_state(self, player):
        player_armour = 1 if self.state.player_has_armor(player) else 0
        player_speed = self.state.get_remaining_turns_speed(player)
        opp_armour = 1 if self.state.player_has_armor(1 - player) else 0
        return self.parser.parse_board(self.state.board, player, player_armour, player_speed, opp_armour)

    def visualize(self, colored=True):
        self.visualizer(self.state, colored)


if __name__ == "__main__":
    cgame = CustomGame()
