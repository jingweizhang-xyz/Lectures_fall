#!/usr/bin/python3
# coding=utf-8

import math
import copy
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
eta = 1  # Learning rate
M_bach = 40  # Max training passes of batch BP
M_single = M_bach * 30  # Max training passes of single BP


def trans(layer, x):
    return {
        1: np.tanh(x),  # Hyperbolic function
        2: 1 / (1 + np.exp(-x)),  # sigmoid
        3: x,
    }[layer]


def trans_prime(layer, y):
    return {
        1: 1 - y**2,  # Hyperbolic function
        2: y * (1 - y),  # sigmoid
        3: 1,
    }[layer]


def init_all_sample():
    s = []
    for x in omega1:
        s.append([x, [1, 0, 0]])
    for x in omega2:
        s.append([x, [0, 1, 0]])
    for x in omega3:
        s.append([x, [0, 0, 1]])
    return s


def init_network(n_h):
    d = 3
    c = 3
    w_ih = np.random.uniform(-w_0, w_0, (d, n_h))
    w_hj = np.random.uniform(-w_0, w_0, (n_h, c))
    w_jo = np.identity(3)  # out
    w_xi = np.identity(3)  # in
    ws = [w_xi, w_ih, w_hj, w_jo]
    # print(ws)
    return ws


def get_net_output(sample, ws):
    out = []
    out.append(sample[0])  # initial x
    for k in range(1, len(ws)):
        w = ws[k]
        y = []
        for j in range(len(w[0])):
            s = 0
            x = out[len(out) - 1]
            for i in range(len(x)):
                s += w[i][j] * x[i]
            s = trans(k, s)
            y.append(s)
        out.append(np.array(y))
    return out


def judge_function(samples, ws):
    s = 0
    for sample in samples:
        out = get_net_output(sample, ws)
        t = sample[1]
        z = out[-1]
        delta = t - z
        s += np.sum([x**2 for x in delta])
    return s / 2


def batch_BP(samples, ws, ws_org):
    J = []
    J.append(judge_function(samples, ws))
    for cnt in range(M_bach):
        dws = []
        for w in ws:
            l = (len(w), len(w[0]))
            dws.append(np.zeros(l))
        for k in range(30):
            delta = []
            sample = samples[k % len(samples)]
            t = sample[1]
            out = get_net_output(sample, ws_org)
            z = out[-1]
            delta.append(t - z)
            for layer in range(len(ws) - 2, 0, -1):
                w = ws[layer]
                w_right = ws[layer + 1]
                delta_now = []
                for j in range(len(w[0])):
                    l = [w_right[j][c] * delta[-1][c]
                         for c in range(len(delta[-1]))]
                    sum_right = np.sum(l)
                    delta_now.append(
                        trans_prime(layer, out[layer][j]) * sum_right)
                    for i in range(len(w)):
                        dws[layer][i][j] += eta * \
                            out[layer - 1][i] * delta_now[j]
                delta.append(delta_now)
        for layer in range(len(ws) - 2, 0, -1):
            w = ws[layer]
            for j in range(len(w[0])):
                for i in range(len(w)):
                    w[i][j] += dws[layer][i][j]
        # judge function
        J.append(judge_function(samples, ws))
    return J


def single_sample_BP(samples, ws, ws_org):
    # M_single = 1
    J = []
    J.append(judge_function(samples, ws))
    for k in range(M_single):
        delta = []
        sample = samples[k % len(samples)]
        t = sample[1]
        out = get_net_output(sample, ws_org)
        z = out[-1]
        delta.append(t - z)
        for layer in range(len(ws) - 2, 0, -1):
            w = ws[layer]
            w_right = ws[layer + 1]
            delta_now = []
            for j in range(len(w[0])):
                l = [w_right[j][c] * delta[-1][c]
                     for c in range(len(delta[-1]))]
                sum_right = np.sum(l)
                delta_now.append(trans_prime(layer, out[layer][j]) * sum_right)
                for i in range(len(w)):
                    dw_ij = eta * out[layer - 1][i] * delta_now[j]
                    w[i][j] += dw_ij
            delta.append(delta_now)
        # judge function
        J.append(judge_function(samples, ws))
    return J

if __name__ == '__main__':
    # ws = init_network(20)
    ws = init_network(4)
    ss = init_all_sample()
    colors = [0,'r','b','g','y']
    for i in range(1,5):
        eta = i * 0.3
        Js_batch = batch_BP(ss, copy.deepcopy(ws), ws)
        label = "eta=" + ('%.2f' % eta)
        plt.plot(Js_batch,color=colors[i], label=label)
    plt.title("Judging Function Values(batch BP)")
    plt.legend()
    plt.show()

    for i in range(1,5):
        eta = i * 0.3
        Js_batch = single_sample_BP(ss, copy.deepcopy(ws), ws)
        label = "eta=" + ('%.2f' % eta)
        plt.plot(Js_batch,color=colors[i], label=label)
    plt.title("Judging Function Values(single sample BP)")
    plt.legend()
    plt.show()
