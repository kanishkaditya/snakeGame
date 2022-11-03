import tensorflow as tf
import numpy as np


def forward(weights, observation):
    #print(len(weights),len(observation))
    #z1 = np.matmul(observation, weights[0:768].reshape(32, 24)) + weights[768:800]
    #output1 = tf.relu(z1)
    z1 = np.matmul(observation, weights[0:224].reshape(28, 8)) + weights[224:232]
    output1 = tf.nn.relu(z1)

    z2 = np.matmul(output1, weights[232:264].reshape(8, 4)) + weights[264:268]
    output = tf.nn.sigmoid(z2)

    # z3 = np.matmul(output2, weights[832:880].reshape(12, 4)) + weights[880:884]

    # output = tf.nn.softmax(z3)

    return np.argmax(output)
