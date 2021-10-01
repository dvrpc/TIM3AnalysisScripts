import numpy as np
from scipy.integrate import simps

coeffs = [-5.5792234783907, -5.5792234783907, -2.6717848972856, -0.6405686607330]
def get_util(d):
    global coeffs
    if d < 0.1:
        return coeffs[0]*d
    elif d < 0.35:
        return coeffs[0] + coeffs[1]*(d-0.1)
    elif d < 1:
        return coeffs[0] + 0.25*coeffs[1] + coeffs[2]*(d-0.35)
    else:
        return coeffs[0] + 0.25*coeffs[1] + 0.65*coeffs[2] + coeffs[3]*(d-1)
get_util = np.vectorize(get_util)

max_dist = 10
step = 0.01
d = np.arange(0, max_dist + step, step)

U = get_util(d)

atl = simps(d*np.exp(U), d) / simps(np.exp(U), d)
print(10*atl)