#!/usr/bin/python3
# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt

# constant values
omega1 = np.array([
                    [0.1, 1.1],
                    [6.8, 7.1],
                    [-3.5, -4.1],
                    [2.0, 2.7],
                    [4.1, 2.8],
                    [3.1, 5.0],
                    [-0.8, -1.3],
                    [0.9, 1.2],
                    [5.0, 6.4],
                    [3.9, 4.0]
                    ])
omega2 = np.array([
                    [7.1, 4.2],
                    [-1.4, -4.3],
                    [4.5, 0.0],
                    [6.3, 1.6],
                    [4.2, 1.9],
                    [1.4, -3.2],
                    [2.4, -4.0],
                    [2.5, -6.1],
                    [8.4, 3.7],
                    [4.1, -2.2]
                    ])
omega3 = np.array([
                    [-3.0, -2.9],
                    [0.5, 8.7],
                    [2.9, 2.1],
                    [-0.1, 5.2],
                    [-4.0, 2.2],
                    [-1.3, 3.7],
                    [-3.4, 6.2],
                    [-4.1, 3.4],
                    [-5.1, 1.6],
                    [1.9, 5.1]
                    ])
origin = [0,0,0]

def eta(k):
    return 1

def batch_perception(a, b, start_a):
    s = [[1,x[0],x[1]] for x in a]
    s.extend([[-1,-x[0],-x[1]] for x in b])
    s = np.array(s)
    a = start_a
    Y = s[np.inner(a,s) <= 0]
    iter_cnt = 0
    while(len(Y) > 0):
        iter_cnt += 1
        a += eta(iter_cnt) * np.sum(Y, axis=0)
        Y = s[np.inner(a,s) <= 0]
    return a,iter_cnt

if __name__ == '__main__':
    # Problem a)
    a_a, cnt_a = batch_perception(omega1, omega2, origin)
    print(a_a,cnt_a)

    # Problem b)
    a_b, cnt_b = batch_perception(omega3, omega2, origin)
    print(a_b,cnt_b)