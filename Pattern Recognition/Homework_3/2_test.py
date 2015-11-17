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
omega4 = np.array([
                    [-2.0, 8.4],
                    [-8.9, 0.2],
                    [-4.2, 7.7],
                    [-8.5, -3.2],
                    [-6.7, -4.0],
                    [-0.5, -9.2],
                    [-5.3, -6.7],
                    [-8.7, -6.4],
                    [-7.1, -9.7],
                    [-8.0, -6.3]
                    ]) 
origin = [0,0,0]

def eta(k):
    return 0.5

def rand_start(n):
    return [np.random.uniform() for i in range(n)]

def get_init_b(n):
    return [0.1 for i in range(n)]

def Ho_Kashyap(s1, s2, a_start, b_start, k_max, b_min):
    s = [[1,x[0],x[1]] for x in s1]
    s.extend([[-1,-x[0],-x[1]] for x in s2])
    Y = np.matrix(s)
    Y_inv = np.linalg.pinv(Y)
    a = np.matrix(a_start).T
    b = np.matrix(b_start).T
    all_e = []
    split_able = False
    for k in range(1, k_max+1):
        # inpu = input("interation")
        e = Y * a - b
        # all_e.append((e.T * e)[0,0])
        # print(cnt)
        if(np.max(np.abs(e)) < b_min):
            split_able = True
            break
        e_plus = e
        e_plus[e < 0] = 0
        b = b + (2 * eta(k)) * e_plus
        a = Y_inv * b
    print(split_able)
    return [a[0,0],a[1,0],a[2,0]]

if __name__ == '__main__':
    k_max = 10000
    start_a = rand_start(3)
    start_b = get_init_b(len(omega1)+len(omega3))
    b_min = 1E-5
    # omega 1 and omega 3
    a = ll_E_1 = Ho_Kashyap(omega1, omega3,
        start_a, start_b, k_max, b_min)
    print(a)
    x = np.linspace(-10, 10)
    print(x)
    y = [-(a[1] * xi + a[0]) / a[2] for xi in x]
    print(y)
    x_1 = [x[0] for x in omega1]
    y_1 = [x[1] for x in omega1]

    x_2 = [x[0] for x in omega3]
    y_2 = [x[1] for x in omega3]

    plt.scatter(x_1, y_1, color='r')
    plt.scatter(x_2, y_2, color='b')
    plt.plot(x, y, color='g')
    plt.show()