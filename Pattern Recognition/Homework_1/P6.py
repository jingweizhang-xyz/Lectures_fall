#!/usr/bin/python3
# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# constant values
X_MIN = -100
X_MAX = 100
N_MIN = 0 + 1
N_MAX = 1000

# Problem a)


def gen_uniform(xl, xr, n):
    return np.random.randint(xl, xr + 1, n)

# Problem b)


def gen_paramaters():
    xl = np.random.randint(X_MIN, X_MAX+1)
    xr = np.random.randint(X_MIN, X_MAX+1)
    if xl > xr:
        xl, xr = xr, xl
    n = np.random.randint(N_MIN, N_MAX+1)
    return xl, xr, n

# Problem c) and d)


def gen_rand_uniform(total_n):
    cnt = 0
    l = []
    while(cnt < total_n):
        xl, xr, n = gen_paramaters()
        if cnt + n > total_n:
            n = total_n - cnt
        l.extend(gen_uniform(xl, xr, n))
        cnt += n
    mean = np.mean(l)
    sigma = np.std(l)
    return l, mean, sigma

if __name__ == '__main__':
    l = [1e4,1e5,1e6]
    for N in l:
        l1, mean,sigma = gen_rand_uniform(N)
        count, bins, ignored = plt.hist(l1, X_MAX - X_MIN +1, normed = 1)
        y = mlab.normpdf(bins, mean, sigma)
        plt.plot(bins, y, 'r')
        plt.xlabel('X values')
        plt.ylabel('Probability')
        title_1 = r'$\mu=$'
        title_2 = r'$,\sigma=$'
        title = title_1+("%.2f" % mean)+title_2+("%.2f" % sigma)+", N="+("%d"%N)
        plt.title(title)
        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.show()
