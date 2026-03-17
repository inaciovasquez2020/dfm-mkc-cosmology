import numpy as np

def fisher_matrix(loglike,params,eps=1e-4):

    params = np.array(params)
    n = len(params)
    F = np.zeros((n,n))

    for i in range(n):
        for j in range(n):

            p1 = params.copy()
            p2 = params.copy()

            p1[i] += eps
            p2[j] += eps

            d1 = loglike(p1) - loglike(params)
            d2 = loglike(p2) - loglike(params)

            F[i,j] = d1*d2/(eps**2)

    return F
