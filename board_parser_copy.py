import numpy as np

def board_parser(board_state, speed_number1, armor1, curr_player, speed_number2, armor2):
    state_count = 9
    length = (len(board_state) * state_count) + 4 + 1
    parsed_list = np.zeros((length,), dtype=int)
    dict = {
    "x" : 0,
    "1" : which_player("1", curr_player),
    "2" : which_player("2", curr_player),
    " " : 3,
    "#" : 4,
    "*" : 5,
    "^" : 6,
    "!" : 7,
    "@" : 8
    }

    for i in range(len(board_state)):
        parsed_list[i*state_count + dict[board_state[i]] ] = 1
        parsed_list[i*state_count + 8] = 9

    if armor1:
        parsed_list[state_count * len(board_state)] = 1
    if speed_number1 > 0:
        parsed_list[state_count * len(board_state) + speed_number1] = 1
    
    return parsed_list

def which_player(num, curr_player):
    if(num == curr_player):
        return 1
    return 2

def main():
    print (len(["1", "#", "#"]))
    mine = board_parser(["1", "#", "#"], 2, True, "1")
    print(mine)
    print(len(mine))
if __name__ == "__main__":
    main()
