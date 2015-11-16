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
