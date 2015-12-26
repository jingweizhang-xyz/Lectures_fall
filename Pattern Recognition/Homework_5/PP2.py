#!/usr/bin/python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

data_file_path = './PP2.data'
sigma2 = 1**2
k_nearest = 5
k_eigen_vectors = 2
EPS = 1E-9
num_of_clusters = 2


def get_samples():
    samples = []
    with open(data_file_path, mode="r") as in_file:
        for line in in_file:
            row = line.split()
            xs = [float(a) for a in row]
            samples.append(xs)
    return samples

def get_wij(pa, pb):
    d2 = np.sum([(pa[i] - pb[i])**2 for i in range(len(pa))])
    return np.exp(-d2 / 2 / sigma2)

def get_wij(d2):
    return np.exp(-d2 / 2 / sigma2)

def build_graph(samples):
    S = np.asarray(samples)
    N = len(samples)
    G = np.zeros([N, N])
    dis = np.zeros(N)
    for r in range(N):
        for c in range(N):
            if r == c:
                dis[c] = 0
            else:
                v = np.subtract(S[r], S[c])
                dis[c] = np.sum([x**2 for x in v])
        indexes = np.argsort(dis)
        # print(indexes[0:k+1])
        # print(dis[0:11])
        # input()
        k = k_nearest
        for i in indexes[1:k+1]:
            G[r][i] = get_wij(dis[i])
    return G

def compute_L_sym(W):
    W_mat = np.asmatrix(W)
    W_mat = (W_mat.T + W) / 2
    D_half_rev = np.asmatrix(np.zeros(W.shape))
    # print(D_half_rev)
    for r in range(len(D_half_rev)):
        s = np.sum(W_mat[r])
        # print(D_half_rev[r, r])
        D_half_rev[r, r] = 1 / np.sqrt(s)
    # print(D_half_rev)
    I = np.identity(len(W_mat))
    L_sym = I - D_half_rev * W_mat * D_half_rev
    return L_sym

def normalize(v):
    s = v * v.T
    v /= np.sqrt(s)
    return v

def compute_Accu(omega):
    dic = {}
    for i in range(num_of_clusters):
        dic[i] = 0
    for i in range(0, 100):
        dic[omega[i]] += 1
    n1 = max(dic.items(), key=lambda x: x[1])
    for i in range(num_of_clusters):
        dic[i] = 0
    for i in range(100, 200):
        dic[omega[i]] += 1
    n2 = max(dic.items(), key=lambda x: x[1])
    Accu = (n1[1] + n2[1]) / 200
    print(n1, n2, Accu)
    return Accu

def spectral_clustering(W):
    L_s = compute_L_sym(W)
    w, v = LA.eigh(L_s)
    f = 0  # first none-zero eigen column
    while np.abs(w[f]) < EPS:
        f += 1
    U = v[:, f:f + k_eigen_vectors]
    # Normalizing
    for row in U:
        normalize(row)
    # print("U: ", U)
    Accu = 0
    for cnt in range(5):
        omega = k_means(U, num_of_clusters)
        t = compute_Accu(omega)
        Accu = max(Accu, t)
    return Accu

def dis2(a, b):
    d = np.subtract(a, b)
    return d * d.T

def k_means(samples, clusters):
    N = clusters
    S = np.asmatrix(samples)
    means = 2 * np.random.random(S.shape[1] * N) - 1
    means = means.reshape([clusters, S.shape[1]])
    # print("initial means: ", means)
    changed = True
    omega = np.zeros(S.shape[0])
    while changed:
        changed = False
        sums = np.asmatrix(np.zeros(means.shape))
        cnt = np.zeros(means.shape[0])
        for s_i in range(len(S)):
            x = S[s_i]
            mean_i = np.argmin([dis2(x, mean) for mean in means])
            np.add(sums[mean_i], x, sums[mean_i])
            omega[s_i] = mean_i
            cnt[mean_i] += 1
        # print("cnt: ", cnt)
        for i in range(len(sums)):
            sums[i] /= cnt[i]
            diff = np.subtract(sums[i], means[i])
            if np.max(np.abs(diff)) > EPS:
                changed = True
            means[i] = sums[i]
        # print(means)
        # input()
    return omega

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

if __name__ == '__main__':
    samples = get_samples()
    # When sigma changes
    Accu = []
    x = []
    for sig in frange(1, 10, 0.5):
        x.append(sig)
        sigma2 = sig**2
        W = build_graph(samples)
        Accu.append(spectral_clustering(W))
    plt.plot(x, Accu)
    plt.show()
    # When k changes
    Accu = []
    x = []
    sigma2 = 1
    for k in range(1, 200, 10):
        x.append(k)
        k_nearest = k
        W = build_graph(samples)
        Accu.append(spectral_clustering(W))
    plt.plot(x, Accu)
    plt.show()
    # Accu = spectral_clustering(W)
    # print(Accu)
