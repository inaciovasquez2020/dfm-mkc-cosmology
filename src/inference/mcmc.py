import numpy as np

class SimpleMCMC:
    """
    Minimal Metropolis–Hastings sampler.
    """

    def __init__(self, loglike, initial_params, step_sizes):
        self.loglike = loglike
        self.params = np.array(initial_params, dtype=float)
        self.step = np.array(step_sizes, dtype=float)

    def sample(self, nsteps=1000):
        chain = []
        current_ll = self.loglike(self.params)

        for _ in range(nsteps):
            proposal = self.params + np.random.normal(scale=self.step)
            prop_ll = self.loglike(proposal)

            accept = np.log(np.random.rand()) < prop_ll - current_ll

            if accept:
                self.params = proposal
                current_ll = prop_ll

            chain.append(self.params.copy())

        return np.array(chain)
