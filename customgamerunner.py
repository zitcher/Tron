import time
from customgame import CustomGame
import support
import random
import numpy as np


def run_game(bots, visualizer=False, delay=0.2, max_wait=0.3, colored=True):
    """
    Inputs:
        - asp: an adversarial search problem
        - bots: a list in which the i'th element is the bot for player i
        - visualizer (optional): a void function that takes in a game state
          and does something to visualize it. If no visualizer argument is
          passed, run_game will not visualize games.

    Runs a game and outputs the evaluation of the terminal state.
    """
    game = CustomGame()
    if visualizer:
        game.visualize()
        time.sleep(delay)

    while not (game.game_over()):
        exposed = game.get_game_problem()
        decision = bots[game.player_to_move()].decide(exposed)

        available_actions = game.available_actions
        if decision not in available_actions:
            raise("DECISION", decision, "NOT IN available_actions", available_actions)

        game.take_action(decision, game.player_to_move())

        if visualizer:
            game.visualize()
            time.sleep(delay)

    return game.get_results()

# Note to self: clean this up for students.
def main():
    random.seed(None)
    np.random.seed(None)
    bots = support.determine_bot_functions(["student", "student"])

    outcome = run_game(bots, True,  0.5, 0.3, True)
    winner = outcome.index(1) + 1
    print("Player %s won!" % winner)
    time.sleep(.5)
    main()


if __name__ == "__main__":
    main()
