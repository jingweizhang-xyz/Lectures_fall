#!/usr/bin/python
# coding=utf-8 

import numpy as np
import matplotlib.pyplot as plt

# constant values
N = 10000
X_L = -1.0/2
X_R = 1.0/2
orgin = [0, 0, 0]

def phi(x,xi,h):
    for i in range(len(x)):
        if np.abs((x[i] - xi[i]) / h) > 1.0 / 2:
            return 0
    else:
        return 1

# Problem a)
def gen_uniform_dis():
    l = np.random.uniform(low = X_L,high = X_R, size=(N,3))
    return l

# Problem b)
def parzen_window_estimation(points, w_size):
    h = w_size
    n = len(points)
    kn = np.sum([phi(orgin, x, h) for x in points])
    p = kn / n / (h**len(points[0]))
    return p

def parzen_window(points):
    x = np.linspace(0.01, 1)
    y = [parzen_window_estimation(points, w) for w in x]
    return x,y

# Problem c)
def window_estimation(points, n):
    h = np.max([np.max([np.abs(x) for x in points[i]]) for i in range(n)])
    # h = h * 2
    kn = np.sum([phi(orgin, points[i], h) for i in range(n)])
    p = kn / n / (h**len(points[0]))
    return p

def window(points, step):
    x = [i for i in range(1,N,step)]
    y = [window_estimation(points,i) for i in x]
    return x,y

# Problem d)
def gen_gaussian_dis():
    l = np.random.normal(0,1, size=(N,3))
    return l

if __name__ == '__main__':
    # Problem a
    ud_points = gen_uniform_dis()
    # Problem b
    x,y = parzen_window(ud_points)
    line, = plt.plot(x,y)
    plt.show()
    # Problem c
    x, y = window(ud_points, 200)
    line, = plt.plot(x,y)
    plt.show()
    # Problem d
    norm_points = gen_gaussian_dis()
    x,y = parzen_window(norm_points)
    line, = plt.plot(x,y)
    plt.show()
    x, y = window(norm_points, 200)
    line, = plt.plot(x,y)
    plt.show()

