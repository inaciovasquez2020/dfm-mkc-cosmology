import numpy as np

def generate_mock(model,z,sigma):

    Hz = np.array([model.H(zi) for zi in z])
    noise = np.random.normal(scale=sigma,size=len(z))

    return Hz + noise
