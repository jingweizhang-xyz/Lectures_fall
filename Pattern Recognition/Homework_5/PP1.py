#!/usr/bin/python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

Sigma = [[1, 0], [0, 1]]
gen_means = [[1, -1], [5.5, -4.5], [1, 4], [6, 4.5], [9, 0]]
EPS = 1E-4

def gen_points():
    x, y = [],[]
    for mean in gen_means:
        x[len(x):len(x)], y[len(y):len(y)] = np.random.multivariate_normal(mean, Sigma, 200).T
    return x,y

def get_samples(x, y):
    samples = []
    for i in range(len(x)):
        samples.append([x[i], y[i]])
    return samples

def get_rand_mean(x, y, size):
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    means = np.random.random((size, 2))
    # print(means)
    for xy in means:
        xy[0] = (x_max - x_min) * xy[0] + x_min
        xy[1] = (y_max - y_min) * xy[1] + y_min
    return means

def vector_add(a, b):
    c = []
    c[0:0] = a
    for i in range(len(a)):
        c[i] += b[i]
    return c

def vector_add_inplace(a, b):
    for i in range(len(a)):
        a[i] += b[i]
    return a

def vector_sub(a, b):
    c = []
    c[0:0] = a
    for i in range(len(a)):
        c[i] -= b[i]
    return c

def k_means(samples, means):
    # print(sums, cnt)
    changed = True
    # str = ""
    while changed:
        sums = []
        for i in range(len(means)):
            sums.append([0, 0])
        cnt = [0] * len(means)
        for sample in samples:
            mi = 0
            min_l = 1E10
            for i in range(len(means)):
                dif = np.array(vector_sub(sample, means[i]))
                l = np.sqrt(dif.dot(dif))
                if l < min_l:
                    mi = i
                    min_l = l
            vector_add_inplace(sums[mi], sample)
            cnt[mi] += 1
        changed = False
        print("cnt:", cnt)
        # print("sum:", np.array(sums))
        for i in range(len(means)):
            if cnt[i] > 0:
                for j in range(len(sums[i])):
                    sums[i][j] /= cnt[i]
            if np.max(np.abs(vector_sub(means[i], sums[i]))) > EPS:
                changed = True
            means[i] = sums[i]
        # print("means:", np.array(means))
    return means

def rand_k_mins(x, y, samples, times):
    for cnt in range(times):
        means = get_rand_mean(x, y, 5)
        print(means)
        new_means = k_means(samples, means)
        print(new_means)

if __name__ == '__main__':
    x, y = gen_points()
    # plt.scatter(x, y)
    # plt.show()
    samples = get_samples(x, y)
    rand_k_mins(x, y, samples, 1)
    # means = gen_means
    # new_means = k_means(samples, means)
    # print(new_means)
    plt.scatter(x, y)
    plt.show()
    