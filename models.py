import numpy as np
import tensorflow as tf

class QSAModel:
    def __init__(self, num_states, num_actions, batch_size):
        self.input_size = input_size
        self.output_size = output_size
        self._batch_size = batch_size

        # define the placeholders
        self.inputs = tf.placeholder(shape=[None, self.input_size], dtype=tf.float32)
        self._q_s_a = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32)
        self.logits = self.forward_pass()
        self.loss = self.loss_function()
        self.optimizer = self.optimizer()
        self._var_init = tf.global_variables_initializer()

    def forward_pass(self):
        """
        Predicts a label given an image using fully connected layers

        :return: the predicted label as a tensor
        """

        # create a couple of fully connected hidden layers
        fc1 = tf.layers.dense(self._states, int(self.input_size // 2), activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, int(self.input_size // 4), activation=tf.nn.relu)
        fc3 = tf.layers.dense(fc2, int(self.input_size // 8), activation=tf.nn.relu)
        logits = tf.layers.dense(fc3, self.output_size)
        return logits

    def loss_function(self):
        """
        Calculates the model loss

        :return: the loss of the model as a tensor
        """
        return tf.losses.mean_squared_error(self._q_s_a, self._logits)

    def optimizer(self):
        """
        Optimizes the model loss

        :return: the optimizer as a tensor
        """
        return tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)

    def predict_one(self, input, sess):
        return sess.run(self.logits, feed_dict={self.inputs:
                                                input.reshape(1, self.input_size)})

    def predict_batch(self, inputs, sess):
        return sess.run(self._logits, feed_dict={self.inputs: inputs})

    def train_batch(self, sess, x_batch, y_batch):
        sess.run(self._optimizer, feed_dict={self.inputs: x_batch, self._q_s_a: y_batch})
