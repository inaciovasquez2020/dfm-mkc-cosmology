from src.inference.mcmc import SimpleMCMC

def loglike(p):
    return -0.5 * (p[0]**2)

def test_sampler_runs():
    sampler = SimpleMCMC(loglike, [0.1], [0.1])
    chain = sampler.sample(50)
    assert len(chain) == 50
