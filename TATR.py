# This function just makes a very standard gaussian data set centered
# at mu and with a standard deviation of sigma.
def gaussian (x, mu, sigma):
    piece1 = (x-mu)**2
    piece2 = 2*sigma**2
    return math.exp(-piece1/piece2)


 # This function corresponds to the function g in this paper:
# https://pubs.acs.org/doi/10.1021/acs.jpca.8b04455 (Eq. 5)
def g (dx, t, sigma):
    x = np.arange(-1, 1+dx, dx)
    v = []
    for i in x:
        v.append(gaussian(i, t, sigma))
    return np.asarray(v)

# This function is Eq. 5 from the paper referenced above
def TATR (dx, amps, sigma):
    tatr = np.zeros(len(np.arange(-1, 1+dx, dx)))
    for amp in amps:
        tatr += f(dx, amp, sigma)
    return tatr