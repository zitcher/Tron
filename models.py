import tensorflow as tf


class DeepQModel:
    def __init__(self, input_size=2604, output_size=4):
        self.input_size = input_size  # D L R U
        self.output_size = output_size
        self.learning_rate = 1e-14
        self.expansion = 10
        self.input = tf.placeholder(shape=[1, input_size], dtype=tf.float32)

        self.qVal = self.forward_pass()
        self.nextQ = tf.placeholder(shape=[1, output_size], dtype=tf.float32)
        self.loss = self.loss_function()
        self.optimizer = self.optimizer_function()

    def forward_pass(self):
        """
        Predicts the rewards for actions given an game state using fully connected layers

        :return: the predicted label as a tensor
        """
        w1 = tf.Variable(tf.truncated_normal([self.input_size, self.input_size * self.output_size * self.expansion], stddev=0.01, dtype=tf.float32))
        b1 = tf.Variable(tf.truncated_normal([self.input_size * self.output_size * self.expansion], stddev=0.01, dtype=tf.float32))
        o1 = tf.nn.relu(tf.add(tf.matmul(self.input, w1), b1))

        w2 = tf.Variable(tf.truncated_normal([self.input_size * self.output_size * self.expansion, self.output_size], stddev=0.01, dtype=tf.float32))
        b2 = tf.Variable(tf.truncated_normal([self.output_size], stddev=0.01, dtype=tf.float32))
        o2 = tf.nn.relu(tf.add(tf.matmul(o1, w2), b2))

        return o2

    def loss_function(self):
        return tf.losses.mean_squared_error(self.nextQ, self.qVal)
        # return tf.reduce_sum(tf.square(self.nextQ - self.qVal))

    def optimizer_function(self):
        # return tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
        return tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)


class DQPolicyGradientModel:
    def __init__(self, input_size=2604, output_size=4):
        self.input_size = input_size  # D L R U
        self.output_size = output_size
        self.learning_rate = 0.0001
        self.input = tf.placeholder(shape=[None, input_size], dtype=tf.float32)

        self.output = self.forward_pass()
        self.rewards = tf.placeholder(shape=[None], dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        self.indicies = tf.range(0, tf.shape(self.output)[0]) * self.output_size + self.actions
        self.actionProb = tf.gather(tf.reshape(self.output, [-1]), self.indicies)

        self.loss = self.loss_function()
        self.optimizer = self.optimizer_function()

    def forward_pass(self):
        """
        Predicts a action given an game state using fully connected layers

        :return: the predicted label as a tensor
        """
        w1 = tf.Variable(tf.truncated_normal([self.input_size, self.input_size * self.output_size], stddev=0.01, dtype=tf.float32))
        b1 = tf.Variable(tf.truncated_normal([self.input_size * self.output_size], stddev=0.01, dtype=tf.float32))
        o1 = tf.nn.relu(tf.add(tf.matmul(self.input, w1), b1))

        w2 = tf.Variable(tf.truncated_normal([self.input_size * self.output_size, self.output_size], stddev=0.01, dtype=tf.float32))
        b2 = tf.Variable(tf.truncated_normal([self.output_size], stddev=0.01, dtype=tf.float32))
        o2 = tf.nn.softmax(tf.nn.sigmoid(tf.add(tf.matmul(o1, w2), b2)))

        return o2

    def loss_function(self):
        return -tf.reduce_mean(tf.log(self.actionProb) * self.rewards)
        # return tf.reduce_sum(tf.square(self.nextQ - self.qVal))

    def optimizer_function(self):
        # return tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
        return tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
