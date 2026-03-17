import numpy as np

class AdaptiveMCMC:

    def __init__(self,loglike,params,step):
        self.loglike = loglike
        self.params = np.array(params)
        self.step = np.array(step)

    def sample(self,nsteps=1000):

        chain=[]
        current_ll=self.loglike(self.params)

        for i in range(nsteps):

            proposal=self.params+np.random.normal(scale=self.step)
            prop_ll=self.loglike(proposal)

            if np.log(np.random.rand()) < prop_ll-current_ll:
                self.params=proposal
                current_ll=prop_ll

            if i%50==0:
                self.step*=1.01

            chain.append(self.params.copy())

        return np.array(chain)
