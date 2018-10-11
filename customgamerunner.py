import time
from tronproblem import TronProblem
import copy
import signal
import support
import random
import numpy as np


def run_game(asp, bots, visualizer=None, delay=0.2, max_wait=0.3, colored=True):
    """
    Inputs:
        - asp: an adversarial search problem
        - bots: a list in which the i'th element is the bot for player i
        - visualizer (optional): a void function that takes in a game state
          and does something to visualize it. If no visualizer argument is
          passed, run_game will not visualize games.

    Runs a game and outputs the evaluation of the terminal state.
    """
    state = asp.get_start_state()
    if visualizer is not None:
        visualizer(state, colored)
        time.sleep(delay)

    while not (asp.is_terminal_state(state)):
        exposed = copy.deepcopy(asp)
        signal.signal(signal.SIGALRM, support.timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, max_wait)
        try:
            # run AI
            decision = bots[state.ptm].decide(exposed)
        except support.TimeoutException:
            if visualizer:
                print(
                    """Warning. Player %s took too long to decide on a move.
They will go UP this round."""
                    % (state.ptm + 1)
                )
            decision = "U"
        signal.setitimer(signal.ITIMER_REAL, 0)

        available_actions = asp.get_available_actions(state)
        if decision not in available_actions:
            decision = list(available_actions)[0]

        result_state = asp.transition(state, decision)
        asp.set_start_state(result_state)

        state = result_state
        if visualizer is not None:
            visualizer(state, colored)
            time.sleep(delay)

    return asp.evaluate_state(asp.get_start_state())


# Note to self: clean this up for students.


def main():
    random.seed(None)
    np.random.seed(None)
    bots = support.determine_bot_functions(["student", "student"])

    maps = ["./maps/joust.txt", "./maps/divider.txt", "./maps/hunger_games.txt"]
    game = TronProblem(random.choice(maps), 0)

    visualizer = TronProblem.visualize_state

    outcome = run_game(copy.deepcopy(game), bots, visualizer, 0.1, 0.3, True)
    winner = outcome.index(1) + 1
    print("Player %s won!" % winner)
    main()


if __name__ == "__main__":
    main()
