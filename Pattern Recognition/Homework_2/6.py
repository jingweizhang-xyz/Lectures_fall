#!/usr/bin/python
# coding=utf-8
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as plt
import math

# constant values
gap = 0.4
EPS = 1e-9
all_k = [1, 3, 5]
c1 = np.array([
    [0.28, 1.31, -6.2],
    [0.07, 0.58, -0.78],
    [1.54, 2.01, -1.63],
    [-0.44, 1.18, -4.32],
    [-0.81, 0.21, 5.73],
    [1.52, 3.16, 2.77],
    [2.20, 2.42, -0.19],
    [0.91, 1.94, 6.21],
    [0.65, 1.93, 4.38],
    [-0.26, 0.82, -0.96]
])
c2 = np.array([
    [0.011, 1.03, -0.21],
    [1.27, 1.28, 0.08],
    [0.13, 3.12, 0.16],
    [-0.21, 1.23, -0.11],
    [-2.18, 1.39, -0.199],
    [0.34, 1.96, -0.16],
    [-1.38, 0.94, 0.45],
    [-0.12, 0.82, 0.17],
    [-1.44, 2.31, 0.14],
    [0.26, 1.94, 0.08]
])
c3 = np.array([
    [1.36, 2.17, 0.14],
    [1.41, 1.45, -0.38],
    [1.22, 0.99, 0.69],
    [2.46, 2.19, 1.31],
    [0.68, 0.79, 0.87],
    [2.51, 3.22, 1.35],
    [0.60, 2.44, 0.92],
    [0.64, 0.13, 0.97],
    [0.85, 0.58, 0.99],
    [0.66, 0.51, 0.88]
])


def dis(a, b):
    return np.sqrt(np.sum([(a[i] - b[i])**2 for i in range(len(a))]))

def getV(r, d):
    v = 0
    if d == 1:
        v = 2 * r
    elif d == 2:
        v = math.pi * r * r
    elif d == 3:
        v = 4.0 / 3.0 * math.pi * (r**3)
    return v

def knn_estimation(points, x, k):
    n = len(points)
    diss = [dis(x, p) for p in points]
    h = max(sorted(diss)[k - 1],EPS)
    v = getV(h, len(points[0]))
    p = k/n/v
    return p

# Problem a)
def problem_a():
    points = [[x[0]] for x in c3]
    x_min = np.min(points) - gap
    x_max = np.max(points) + gap
    x = np.linspace(x_min, x_max)
    ys = []
    for k in all_k:
        ys.append([knn_estimation(points, [xi], k) for xi in x])
    return x, ys

def problem_b():
    points = c2[:,(0,1)]
    d = 2
    points_x = []
    x_min = []
    x_max = []
    for i in range(d):
        points_x.append(points[:,0])
        x_min.append(np.min(points[i]) - gap)
        x_max.append(np.max(points[i]) + gap)

    single_x = []
    for i in range(d):
        single_x.append(np.linspace(x_min[i],x_max[i]))
    x = []
    for xi in single_x[0]:
        for yi in single_x[1]:
            x.append([xi,yi])

    ys = []
    for k in all_k:
        ys.append([knn_estimation(points, xi, k) for xi in x])
    return x, ys

lw = 2
colors = ['r','b','g']

if __name__ == '__main__':
    # Problem a
    x, ys = problem_a()
    plt.title('red for k=1, blue for k=3, green for k=5')
    for i in range(len(ys)):
        plt.plot(x,ys[i],color=colors[i],
            linewidth=lw, label=("k="+str(all_k[i])))
    plt.show()

    # Problem b
    x, ys = problem_b()
    x_1 = [xi[0] for xi in x]
    x_2 = [xi[1] for xi in x]
    for i in range(3):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x_1, x_2, ys[i], cmap=cm.jet, linewidth=0.2)
        plt.show()

