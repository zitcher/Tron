import os
import tensorflow as tf
from models import DeepQModel
import time
from customgame import CustomGame
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def train():
    """
    Trains DeepQModels
    """
    with tf.Session() as sess:
        gamma = 0.9
        # p1, p2 = DeepQModel(), DeepQModel()
        p1 = DeepQModel()
        # with tf.variable_scope("p1"):
        #     p1 = DeepQModel()
        # with tf.variable_scope("p2"):
        #     p2 = DeepQModel()

        sess.run(tf.global_variables_initializer())

        saver = tf.train.Saver()
        # players = [p1, p2]
        game = CustomGame()

        delay = 0.2

        exploration = 1
        num_e_steps = 100
        sub = exploration / num_e_steps

        for i in range(1, 100000):
            reset_distribution = i % num_e_steps == 0
            exploration -= sub
            visualize = i % 10 == 0
            # visualize = True

            game.reset()
            print("Game", i, "exploration", exploration)

            while not (game.game_over()):
                ptm = game.player_to_move()
                # model = players[ptm]
                model = p1
                i_board_state = game.get_game_parsed_state(ptm)
                nextQ = sess.run(model.qVal, feed_dict={model.input: i_board_state})
                action = np.argmax(nextQ)
                if np.random.rand(1) < exploration:
                    if visualize:
                        print("random_move")
                    action = game.get_random_safe_move(ptm)
                if visualize:
                    print("PTM", ptm, "action", action, game.num_to_action[action], "Q", nextQ)
                game.take_num_action(action, ptm)
                rwd = game.score_state(ptm)
                if game.game_over():
                    nextQ[0, action] = rwd
                    if visualize:
                        print("PTM", ptm, "PLAYER LOSS TRAINED ONs", nextQ, "reward", rwd)
                else:
                    opp = game.player_to_move()
                    board_state = game.get_game_parsed_state(opp)
                    oppAction = game.get_random_safe_move(opp)
                    game.see_num_action_result(oppAction, opp)
                    if game.state_over():
                        rwd = game.score_state(ptm)
                        board_state = game.get_game_parsed_state(ptm)
                        nQVal = sess.run(model.qVal, feed_dict={model.input: board_state})
                        nextQ[0, action] = rwd
                        if visualize:
                            print("Win action", game.num_to_action[action], action, game.num_to_action[action], "reward", rwd)
                    else:
                        board_state = game.get_game_parsed_state(ptm)
                        nQVal = sess.run(model.qVal, feed_dict={model.input: board_state})
                        nextQ[0, action] = rwd + gamma * np.amax(nQVal)
                        if visualize:
                            print("Neutral trained on", nextQ, "Estimate MAX", np.amax(nQVal), "nQEstimate", nQVal, "reward", rwd)

                game.rewind()
                if visualize:
                    print("TRAINED ON", nextQ)
                    game.visualize()
                    time.sleep(delay)

                sess.run(model.optimizer, feed_dict={model.input: i_board_state, model.nextQ: nextQ})

            if reset_distribution:
                exploration = 1
            if visualize:
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
