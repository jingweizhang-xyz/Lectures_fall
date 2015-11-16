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