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
            grad = (g[min(i+1,n-1), j] - g[max(i-1,0), j])
            conn = 0.0
            for k in range(n):
                conn += Gamma[i, j, k] * g[k, j]

            res[i, j] = grad + conn

    return res


def gamma_update_from_metric(g, Gamma, lr=0.1):
    res = metric_compatibility_residual(g, Gamma)
    n = g.shape[0]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                Gamma[i, j, k] -= lr * res[i, j]

    return Gamma


def covariant_derivative_full(v, Gamma):
    return covariant_derivative(v, Gamma)


def riemann_tensor(v, Gamma):
    """
    Discrete commutator of covariant derivatives:
    R(v) = ∇(∇v) - ∇(∇v) with swapped directions approximated via index shift
    """
    n = len(v)

    nabla_v = covariant_derivative(v, Gamma)

    # second derivative
    nabla_nabla_v = covariant_derivative(nabla_v, Gamma)

    # curvature proxy as commutator structure
    R = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            R[i, j] = nabla_nabla_v[i] - nabla_nabla_v[j]

    return R
