#!/usr/bin/python3
# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt

# Samples
omega1 = np.array([
    [1.58, 2.32, -5.8],
    [0.67, 1.58, -4.78],
    [1.04, 1.01, -3.63],
    [-1.49, 2.18, -3.39],
    [-0.41, 1.21, -4.73],
    [1.39, 3.16, 2.87],
    [1.20, 1.40, -1.89],
    [-0.92, 1.44, -3.22],
    [0.45, 1.33, -4.38],
    [-0.76, 0.84, -1.96]
])
omega2 = np.array([
    [0.21, 0.03, -2.21],
    [0.37, 0.28, -1.8],
    [0.18, 1.22, 0.16],
    [-0.24, 0.93, -1.01],
    [-1.18, 0.39, -0.39],
    [0.74, 0.96, -1.16],
    [-0.38, 1.94, -0.48],
    [0.02, 0.72, -0.17],
    [0.44, 1.31, -0.14],
    [0.46, 1.49, 0.68]
])
omega3 = np.array([
    [-1.54, 1.71, 0.64],
    [5.41, 3.45, -1.33],
    [1.55, 0.99, 2.69],
    [1.86, 3.19, 1.51],
    [1.68, 1.70, -0.87],
    [3.51, -0.22, -1.39],
    [1.40, -0.44, 0.92],
    [0.44, 0.83, 1.97],
    [0.25, 0.68, -0.99],
    [0.66, -0.45, 0.08]
])


# Constants
sita = 1.5  # When J(w) < sita, training stops.
w_0 = 10  # The initial weight is a uniform U(-w_0,w_0)


def init_all_sample():
    s = []
    for x in omega1:
        s.append([x, [1, 0, 0]])
    for x in omega2:
        s.append([x, [0, 1, 0]])
    for x in omega3:
        s.append([x, [0, 0, 1]])
    return s

def init_network(d, n_h, c):
    w_ih = np.random.uniform(-w_0, w_0, (d, n_h))
    # print(w_ih)
    w_hj = np.random.uniform(-w_0, w_0, (n_h, c))
    # print(w_hj)
    return w_ih, w_hj



if __name__ == '__main__':
    # print(init_all_sample())
    init_network(3, 4, 3)
