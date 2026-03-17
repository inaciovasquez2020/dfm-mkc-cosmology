import numpy as np

def load_hubble_data(path):
    """
    Load H(z) dataset.
    File format: z, H(z), sigma
    """
    data = np.loadtxt(path)
    z = data[:,0]
    H = data[:,1]
    err = data[:,2]
    return z, H, err
