#########################################################
## Stat 202A - Final Project
## Author: Jiayu Wu
## Date: 12/15/2017
## Description: This script implements a two layer neural network in Tensorflow
#########################################################

#############################################################
## INSTRUCTIONS: Please fill in the missing lines of code
## only where specified. Do not change function names,
## function inputs or outputs. You can add examples at the
## end of the script (in the "Optional examples" section) to
## double-check your work, but MAKE SURE TO COMMENT OUT ALL
## OF YOUR EXAMPLES BEFORE SUBMITTING.
##
## Very important: Do not use the function "os.chdir" anywhere
## in your code. If you do, I will be unable to grade your
## work since Python will attempt to change my working directory
## to one that does not exist.
#############################################################

############################################################################
## Implement a two layer neural network in Tensorflow to classify MNIST digits ##
############################################################################

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## Train a two layer neural network to classify the MNIST dataset ##
## Use Relu as the activation function for the first layer. Use Softmax as the activation function for the second layer##
## z=Relu(x*W1+b1) ##
## y=Softmax(z*W2+b2)##
# Use cross-entropy as the loss function#
# Tip: be careful when you initialize the weight and bias parameters.
## You only need to install the CPU version of Tensorflow on your laptop, which is much easier.
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"]=""

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

FLAGS = None


def main(_):
  # Import data
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
  
  # Create the model
  #######################
  ## FILL IN CODE HERE ##
  #######################
  num_hidden1 = 100
  num_hidden2 = 10
  x = tf.placeholder(tf.float32, [None, 784])
  W1 = tf.Variable(tf.random_uniform([784, num_hidden1],-0.01,0.01))
  b1 = tf.Variable(tf.random_normal_initializer()([num_hidden1]))
  W2 = tf.Variable(tf.random_uniform([num_hidden1, num_hidden2],-0.01,0.01))
  b2 = tf.Variable(tf.random_normal_initializer()([num_hidden2]))
  z = tf.nn.relu(tf.matmul(x, W1) + b1)
  y = tf.nn.softmax(tf.matmul(z, W2) + b2)
  
  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])

  cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    
  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  for _ in range(1000):
      batch_xs, batch_ys = mnist.train.next_batch(100)
      sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  
  # test trained model  
  correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
  sess.close()
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)




