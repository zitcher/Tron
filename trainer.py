import os
import torch
from torch import nn, optim
from tqdm import tqdm  # optional progress bar
from models import DeepQModel, QTable
import time
from customgame import CustomGame
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def trainQT(game):
    """
    Trains Tabular Model
    """
    learning_rate = 0.2  # learning rate
    future_confidence = 0.95  # weight of future results
    num_episodes = 1000000
    exploration = 0.1
    delay = 0.5
    q_table = QTable()
    # q_table.load_table("modeldata/qtable.json")

    for i in range(num_episodes):
        print("Game", i, i/num_episodes)
        visualize = i % 100000 == 0
        game.reset()

        while not (game.game_over()):
            ptm = game.player_to_move()
            initial_state = game.get_game_string_parsed_state(ptm)
            action = None

            if visualize:
                if q_table.knows_state(initial_state):
                    print(q_table.table[initial_state])
                else:
                    print("New State", "table size:", len(q_table.table))

            if np.random.rand(1) < exploration:
                if visualize:
                    print("random_move")
                action = game.get_random_safe_move(ptm)
            else:
                action = q_table.get_optimal_action(initial_state)

            game.take_num_action(action, ptm)
            reward = game.score_state(ptm)

            if game.game_over():
                q_table.set_state_action_as_index(initial_state, action, reward)
                if visualize:
                    print("Learned State", q_table.table[initial_state], q_table.get_state_action_value(initial_state, action))
            else:
                opp = game.player_to_move()
                opp_state = game.get_game_string_parsed_state(opp)
                opp_action = q_table.get_optimal_action(opp_state)

                if opp_action not in game.safe_moves(opp):
                    opp_action = game.get_random_safe_move(opp)

                game.see_num_action_result(opp_action, opp)
                if game.state_over():
                    reward = game.score_state(ptm)
                    q_table.set_state_action_as_index(initial_state, action, reward)
                    if visualize:
                        print("Win action", game.num_to_action[action], "reward", reward)
                else:
                    next_state = game.get_game_string_parsed_state(ptm)
                    next_action = q_table.get_optimal_action(next_state)
                    delta = reward
                    delta += future_confidence * q_table.get_state_action_value(next_state, next_action)
                    delta -= q_table.get_state_action_value(initial_state, action)

                    q_table.set_state_action_as_index(initial_state,
                                                      action,
                                                      q_table.get_state_action_value(initial_state, action) + learning_rate * delta)

                    if visualize:
                        print("Learning State", q_table.table[initial_state], q_table.get_state_action_value(initial_state, action))
            if visualize:
                game.visualize()
                time.sleep(delay)

            game.rewind()

    q_table.save_table("modeldata/qtable.json")


def trainDQ(game):
    """
    Trains DeepQModels
    """
    gamma = 0.5

    models = [DeepQModel().to(device), DeepQModel().to(device)]
    optimizers = [optim.Adam(models[0].parameters(), 0.0001), optim.Adam(models[1].parameters(), 0.0001)]
    models[0] = models[0].train()
    models[1] = models[1].train()
    loss_fn = torch.nn.MSELoss(size_average=None, reduce=None, reduction='mean')
    # players = [p1, p2]

    delay = 0.2

    current_exploration = 0.9
    # runs = 20000
    # sub = 1/runs

    for i in range(1, 400000):
        exploration = current_exploration
        visualize = i % 100 == 0
        if visualize:
            current_exploration = current_exploration*0.9
            exploration = 0
        game.reset()
        print("Game", i, "exploration", exploration)
        hist = [{"actionDistributions": [], "actions": [], "rewards": []}, {"actionDistributions": [], "actions": [], "rewards": []}]
        while not (game.game_over()):
            ptm = game.player_to_move()
            model = models[ptm]

            numpy_board, metadata = game.get_game_parsed_state(ptm)

            input = torch.tensor(numpy_board).unsqueeze(0).float()
            input = input.to(device)
            actionDistribution = model(input).squeeze(0)
            hist[ptm]["actionDistributions"].append(actionDistribution)

            action = np.argmax(actionDistribution.tolist())
            if np.random.rand(1) < exploration:
                if visualize:
                    print("random_move")
                action = game.get_random_safe_move(ptm)
            game.take_num_action(action, ptm)
            rwd = game.score_state(ptm)

            hist[ptm]["actions"].append(action)
            hist[ptm]["rewards"].append(rwd)

            if visualize:
                print("E", exploration, "PTM", ptm, "action", action, game.num_to_action[action], "aDist", actionDistribution, "rwd", rwd)
                game.visualize()
                time.sleep(delay)

            if game.game_over():
                # game is over so need to give opposing player winning score
                if len(hist[1 - ptm]["rewards"]) > 0:
                    hist[1 - ptm]["rewards"][-1] = game.score_state(1 - ptm)

                # game is over so train
                for player in [0, 1]:
                    model = models[player]
                    optimizer = optimizers[player]



                    if len(hist[player]["actions"]) == 0:
                        continue
                    # propagate gamma through time
                    hist[player]["rewards"] = offsetRewardsByTime(hist[player]["rewards"][:], gamma)

                    # label predictions

                    predictions = torch.stack(hist[player]["actionDistributions"]).to(device)
                    labels = torch.tensor(labelPredictions(predictions.tolist(), hist[player]["rewards"], hist[player]["actions"])).to(device)
                    loss = loss_fn(predictions, labels)
                    loss.backward()  # calculate gradients
                    optimizer.step()  # update model weights

                if visualize:
                    print('Gameover')
                    print("player", 0, "rwd", hist[0]["rewards"])
                    print("player", 1, "rwd", hist[1]["rewards"])

    for i in range(len(models)):
        torch.save(model[i].state_dict(), './modeldata/model_' + i + '.pt')

def labelPredictions(predictions, rewards, actions):
    for i, a in enumerate(actions):
        predictions[i][a] = rewards[i]

    return predictions


def offsetRewardsByTime(rewards, gamma):
    rewards.reverse()
    for i in range(len(rewards)):
        if i + 1 == len(rewards):
            break
        if rewards[i] == 0:
            break
        rewards[i+1] = rewards[i+1] + gamma * rewards[i]
    rewards.reverse()
    return rewards


def main():
    trainDQ(CustomGame())
    # trainQT(CustomGame())


if __name__ == "__main__":
    main()
