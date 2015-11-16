'''
Created on 2015-9-21

@author: wty
'''

import numpy as np
import matplotlib.pyplot as plt
import math

def p(x, mu, sigma):
    return 1 / (math.sqrt(2 * math.pi) * sigma) * math.exp(-1 / 2 * ((x - mu) / sigma) ** 2)

if __name__ == '__main__':
#     x1 = np.matrix([[0, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 1]])
#     x2 = np.matrix([[1, 1, 1], [0, 1, 0], [0, 1, 1], [0, 0, 1]])
    x = [0.6, 0.1, 0.9, 1.1]
    mu = [0, 0.5, 1]
    sigma = [1, 1, 1]
    P = [0, 1/2, 1/4, 1/4]
    ans = [[0 for i in range(len(mu) + 1)] for i in range(len(x) + 1)]
    for i in range(len(x)):
        xi = x[i]
        for j in range(len(mu)):
            mui = mu[j]
            sigmai = sigma[j]
            ans[i + 1][j + 1] = p(xi, mui, sigmai)
            print("%.4f"%ans[i + 1][j + 1], end=' ')
        print()
    P1 = ans[1][1]*ans[2][2]*ans[3][2]*ans[4][3] 
    print("P(X|omega): ", P1)
    P1 = P1* P[1] * P[2] * P[2] * P[3]
    print("P(X|omega)P(omega): ",P1)
    print()
    sum = 0
    for j1 in range(1, 4):
        for j2 in range(1, 4):
            for j3 in range(1, 4):
                for j4 in range(1, 4):
                    sum += ans[1][j1] * ans[2][j2] * ans[3][j3] * ans[4][j4] \
                        * P[j1] * P[j2] * P[j3] * P[j4]
    print("P(X)",sum)
    PX = sum
    P_p = P1/sum
    print("P(omega|X): ",P_p)
#     for i in range(1, 5):
#         for j in range(1, 4):
#             print("%.3f" % (ans[i][j] * P[j]), end=' & ')
#         print()
#     print(ans[1][1] * ans[2][1] * ans[3][1] * ans[4][1] * P[1] * P[1] * P[1] * P[1])