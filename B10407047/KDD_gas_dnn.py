import tensorflow as tf
import pandas as pd
import numpy as np

num_feat = 10  # every num_feat group the data
n_class = 1
class Neural_Network():
    def __init__(self):
        # self.train_indices = np.random.permutation(trainset_size // num_feat)  # generate random training-data index
        # self.test_indices = np.random.permutation(testset_size // num_feat)  # generate random testing-data index
        with tf.name_scope('inputs'):
            self.xs1 = tf.placeholder(tf.float32, [None, num_feat])
            self.xs2 = tf.placeholder(tf.float32, [None, num_feat])
            self.xs3 = tf.placeholder(tf.float32, [None, num_feat])
            self.xs4 = tf.placeholder(tf.float32, [None, num_feat])
            self.xs5 = tf.placeholder(tf.float32, [None, num_feat])
            # with tf.name_scope('batch_normalization'):
            #     self.xs1_tmp = self.batch_norm(self.xs1, num_feat)
            #     self.xs2_tmp = self.batch_norm(self.xs2, num_feat)
        with tf.name_scope('y_label'):
            self.ys = tf.placeholder(tf.float32, [None, n_class])
        with tf.name_scope('hyper_parameters'):
            self.keep_prob = tf.placeholder(tf.float32)
            self.learning_rate = tf.placeholder(tf.float32)
            self.state_flag = tf.placeholder(tf.int8)
        # with tf.variable_scope('nn_parameters'):
        #     self.nn_param()
        with tf.variable_scope('DNN'):
            self.DNN()
        with tf.name_scope('loss'):
            self.compute_cost()
        with tf.name_scope('train_optimizer'):
            self.train_op = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss)
        with tf.name_scope('prediction'):
            self.prediction = tf.nn.softmax(self.y)
        with tf.name_scope('accuracy'):
            self.compute_accu()

    def read_data(self):

    def DNN(self):

    def compute_cost(self):

    def compute_accu(self):

    def train(self):

    def test(self):

