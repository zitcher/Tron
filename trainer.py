import os
import tensorflow as tf
from models import DeepQModel
import time
from customgame import CustomGame
import numpy as np
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def train():
    """
    Trains DeepQModels
    """
    with tf.Session() as sess:
        gamma = 0.5
        # p1, p2 = DeepQModel(), DeepQModel()
        p1, p2 = None, None
        with tf.variable_scope("p1"):
            p1 = DeepQModel()
        with tf.variable_scope("p2"):
            p2 = DeepQModel()

        sess.run(tf.global_variables_initializer())

        saver = tf.train.Saver()
        players = [p1, p2]
        game = CustomGame()

        delay = 0.2

        e_num = 1
        e_dem = 1

        for i in range(1, 10000):
            visualize = i % 100 == 0
            # visualize = True
            exploration = e_num/e_dem
            e_dem += 1

            game.reset()
            print("Game", i)

            while not (game.game_over()):
                if visualize:
                    e_dem = 1
                    game.visualize()
                    time.sleep(delay)
                ptm = game.player_to_move()
                model = players[ptm]
                i_board_state = game.get_game_parsed_state(ptm)
                nextQ = sess.run(model.qVal, feed_dict={model.input: i_board_state})
                action = np.argmax(nextQ)
                if np.random.rand(1) < exploration:
                    if visualize:
                        print("random_move")
                    action = game.get_random_safe_move(ptm)

                game.take_num_action(action, ptm)
                rwd = game.score_state(ptm)
                if game.game_over():
                    nextQ[0, action] = rwd
                    # print("LOSE", nextQ)
                else:
                    opp = game.player_to_move()
                    board_state = game.get_game_parsed_state(opp)
                    oppModel = players[opp]
                    oppQVal = sess.run(oppModel.qVal, feed_dict={oppModel.input: board_state})
                    oppAction = np.argmax(oppQVal)
                    game.see_num_action_result(oppAction, opp)
                    if game.state_over():
                        nextQ[0, action] = game.score_state(ptm)
                        # print("WIN", nextQ, action)
                    else:
                        board_state = game.get_game_parsed_state(ptm)
                        nQVal = sess.run(model.qVal, feed_dict={model.input: board_state})
                        nextQ[0, action] = rwd + gamma * np.amax(nQVal)
                        # print(nextQ, np.amax(nQVal), nQVal)

                game.rewind()
                sess.run(model.optimizer, feed_dict={model.input: i_board_state, model.nextQ: nextQ})

            if visualize:
                game.visualize()
                if game.game_over():
                    winner = game.get_results().index(1) + 1
                    print("Player %s won!" % winner)
                    print("Win Reward", game.score_state(game.get_results().index(1)))
                    print("Lose Reward", game.score_state(game.get_results().index(0)))

                    save_path = saver.save(sess, "./model_data/dqm.ckpt")
                    print("Model saved in path: %s" % save_path)


def main():
    train()


if __name__ == "__main__":
    main()
