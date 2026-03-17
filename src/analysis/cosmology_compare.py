import numpy as np

def compare_models(models,z):

    results = {}

    for name,model in models.items():
        Hz = [model.H(zi) for zi in z]
        results[name] = np.array(Hz)

    return results
