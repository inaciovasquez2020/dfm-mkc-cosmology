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


def metric_compatibility_residual(g, Gamma):
    n = g.shape[0]
    res = np.zeros_like(g)

    for i in range(n):
        for j in range(n):
            grad = 0.0
            for k in range(n):
                grad += (g[i+1 if i+1<n else i, j] - g[i-1 if i-1>=0 else i, j])
            conn = 0.0
            for k in range(n):
                conn += Gamma[i, j, k] * g[k, j]

            res[i, j] = grad + conn

    return res


def gamma_update_from_metric(g, Gamma, lr=0.1):
    """
    Projection step enforcing ∇g ≈ 0
    """
    res = metric_compatibility_residual(g, Gamma)
    n = g.shape[0]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                Gamma[i, j, k] -= lr * res[i, j]

    return Gamma
