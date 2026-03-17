class SurveySpec:

    def __init__(self,name,z_min,z_max,n_points,sigma):
        self.name = name
        self.z_min = z_min
        self.z_max = z_max
        self.n_points = n_points
        self.sigma = sigma

    def redshift_grid(self):
        import numpy as np
        return np.linspace(self.z_min,self.z_max,self.n_points)
