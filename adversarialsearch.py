import math


def alpha_beta_cutoff(asp, cutoff_ply, eval_func):
    """
    This function should:
    - search through the asp using alpha-beta pruning
    - cut off the search after cutoff_ply moves have been made.

    Inputs:
        asp - an AdversarialSearchProblem
        cutoff_ply- an Integer that determines when to cutoff the search
            and use eval_func.
            For example, when cutoff_ply = 1, use eval_func to evaluate
            states that result from your first move. When cutoff_ply = 2, use
            eval_func to evaluate states that result from your opponent's
            first move. When cutoff_ply = 3 use eval_func to evaluate the
            states that result from your second move.
            You may assume that cutoff_ply > 0.
        eval_func - a function that takes in a GameState and outputs
            a real number indicating how good that state is for the
            player who is using alpha_beta_cutoff to choose their action.
            You do not need to implement this function, as it should be provided by
            whomever is calling alpha_beta_cutoff, however you are welcome to write
            evaluation functions to test your implemention

    Output: an action(an element of asp.get_safe_actions(asp.get_start_state()))
    """
    state = asp.get_start_state()
    player = state.player_to_move()
    v, action = abc_max_value(asp, player, state, eval_func, -math.inf, math.inf, cutoff_ply, 1)
    return action


def abc_max_value(asp, player, state, eval_func, alpha, beta, cutoff, turn_num):
    if asp.is_terminal_state(state):
        evaluation = asp.evaluate_state(state)
        if evaluation[player] == 1:
            return float("inf"), None
        else:
            return float("-inf"), None
    if turn_num > cutoff:
        return eval_func(state, player), None
    v = -math.inf
    chosen_action = None
    actions = asp.get_safe_actions(state.board, state.player_locs[player])
    for a in actions:
        vm, action = abc_min_value(asp, player, asp.transition(state, a), eval_func, alpha, beta, cutoff, turn_num + 1)
        if vm > v:
            v = vm
            chosen_action = a

        if v >= beta:
            return v, chosen_action

        alpha = max(alpha, v)

    return v, chosen_action


def abc_min_value(asp, player, state, eval_func, alpha, beta, cutoff, turn_num):
    if asp.is_terminal_state(state):
        evaluation = asp.evaluate_state(state)
        if evaluation[player] == 1:
            return float("inf"), None
        else:
            return float("-inf"), None
    if turn_num > cutoff:
        return eval_func(state, player), None
    v = math.inf
    chosen_action = None
    actions = asp.get_safe_actions(state.board, state.player_locs[player == 0])
    for a in actions:
        vm, action = abc_max_value(asp, player, asp.transition(state, a), eval_func, alpha, beta, cutoff, turn_num + 1)
        if vm < v:
            v = vm
            chosen_action = a

        if v <= alpha:
            return v, chosen_action

        beta = min(beta, v)

    return v, chosen_action
