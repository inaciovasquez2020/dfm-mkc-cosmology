import numpy as np

def covariant_derivative(v, Gamma):
    n = len(v)
    nabla_v = np.zeros_like(v)

    for i in range(n):
        correction = 0.0
        for j in range(n):
            correction += Gamma[i, j, i] * v[j]

        nabla_v[i] = v[i] + correction

    return nabla_v
