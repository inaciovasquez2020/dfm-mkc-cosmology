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
            grad = g[min(i+1,n-1), j] - g[max(i-1,0), j]
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


def riemann_tensor(Gamma):
    """
    Rank-4 discrete Riemann tensor:
    R^i_{jkl} = Γ^i_{km} Γ^m_{lj} - Γ^i_{lm} Γ^m_{kj}
    + discrete directional difference correction
    """

    n = Gamma.shape[0]
    R = np.zeros((n, n, n, n))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):

                    quad = 0.0
                    for m in range(n):
                        quad += (
                            Gamma[i, k, m] * Gamma[m, l, j]
                            - Gamma[i, l, m] * Gamma[m, k, j]
                        )

                    # TRUE discrete directional correction (index-consistent)
                    dGamma = 0.0
                    for m in range(n):
                        dGamma += (
                            Gamma[i, k, m] - Gamma[i, l, m]
                        ) * Gamma[m, l, j]

                    R[i, j, k, l] = quad + dGamma

    return R
