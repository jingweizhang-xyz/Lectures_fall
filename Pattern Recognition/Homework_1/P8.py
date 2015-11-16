#!/usr/bin/python3
# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# constant values
sample_1 = np.array([
    [0.42, -0.087, 0.58],
    [-0.2, -3.3, -3.4],
    [1.3, -0.32, 1.7],
    [0.39, 0.71, 0.23],
    [-1.6, -5.3, -0.15],
    [-0.029, 0.89, -4.7],
    [-0.23, 1.9, 2.2],
    [0.27, -0.3, -0.87],
    [-1.9, 0.76, -2.1],
    [0.87, -1.0, -2.6]
])
sample_2 = np.array([
    [-0.4, 0.58, 0.089],
    [-0.31, 0.27, -0.04],
    [0.38, 0.055, -0.035],
    [-0.15, 0.53, 0.011],
    [-0.35, 0.47, 0.034],
    [0.17, 0.69, 0.1],
    [-0.011, 0.55, -0.18],
    [-0.27, 0.61, 0.12],
    [-0.065, 0.49, 0.0012],
    [-0.12, 0.054, -0.063]
])
sample_3 = np.array([
    [0.83, 1.6, -0.014],
    [1.1, 1.6, 0.48],
    [-0.44, -0.41, 0.32],
    [0.047, -0.45, 1.4],
    [0.28, 0.35, 3.1],
    [-0.39, 0.48, 0.11],
    [0.34, -0.079, 0.14],
    [-0.3, -0.22, 2.2],
    [1.1, 1.2, -0.46],
    [0.18, -0.11, -0.49]
])
samples = [sample_1, sample_2, sample_3]

# Problem a)
def calc_MLE_1D(sample, i):
    l = []
    for x in sample:
        l.append(x[i])
    mean = np.mean(l)
    sigma = np.std(l)
    return mean, sigma


def solve_a():
    l = [0, 1, 2]
    sample = samples[0]
    for j in l:
        mean, sigma = calc_MLE_1D(sample, j)
        # print("\tomega1: X" + str(j + 1) +
        #       ": mu = " + ("%.3f" % mean) + ", sigma^2 = " + ("%.3f" % sigma**2))
        print("\tomega1: X" + str(j + 1) +
              ": mu = " + str(mean) + ", sigma^2 = " + str(sigma**2))
    print()

# compute mean \u and covarient matrix \Sigma
def calc_MLE_Above_1D(l):
    mean = np.mean(l, axis=0)
    d = len(l[0])
    Sigma = np.zeros((d, d))
    for x in l:
        v = np.matrix([x - mean])
        Sigma += v.T.dot(v)
    Sigma /= len(l)
    return mean, Sigma

# Problem b)
def solve_b():
    for i in range(3):
        for j in range(i+1, 3):
            l = [[x[i],x[j]] for x in sample_1]
            mean, Sigma = calc_MLE_Above_1D(l)
            print("For X"+str(i+1)+" and X"+str(j+1)+":")
            print("mu =",mean)
            print("Sigma=\n",Sigma)
    print()

# Problem c)
def solve_c():
    mean, Sigma = calc_MLE_Above_1D(sample_1)
    print("mu =",mean)
    print("Sigma=\n",Sigma)

# Problem d)
def solve_d():
    l = [0, 1, 2]
    sample = samples[1]
    ans = []
    for j in l:
        mean, sigma = calc_MLE_1D(sample, j)
        ans.append([mean, sigma])
    mu = [mean for mean, sigma in ans]
    sigma_2 = [sigma*sigma for mean, sigma in ans]
    print("mu:", mu)
    print("sigma^2 1,2,3:",sigma_2)
    print()

if __name__ == '__main__':
    print("Problem a):")
    solve_a()

    print("Problem b):")
    solve_b()
    
    print("Problem c):")
    solve_c()

    print("Problem d):")
    solve_d()


    # print(type(samples[]))
