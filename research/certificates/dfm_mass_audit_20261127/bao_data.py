import json, numpy as np, scipy
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, differential_evolution
from scipy.linalg import cho_factor, cho_solve
from scipy.stats import chi2
z=np.array([.295,.51,.51,.706,.706,.934,.934,1.321,1.321,1.484,1.484,2.33,2.33])
y=np.array([7.94167639,13.58758434,21.86294686,17.35069094,19.45534918,21.57563956,17.64149464,27.60085612,14.17602155,30.51190063,12.81699964,8.631545674846294,38.988973961958784])
kind=['DV','DM','DH','DM','DH','DM','DH','DM','DH','DM','DH','DH','DM']
C=np.zeros((13,13)); C[0,0]=5.78998687e-3
for j,(a,b,c) in enumerate([(2.83473742e-2,-3.26062007e-2,1.83928040e-1),(3.23752442e-2,-2.37445646e-2,1.11469198e-1),(2.61732816e-2,-1.12938006e-2,4.04183878e-2),(1.05336516e-1,-2.90308418e-2,5.04233092e-2),(5.83020277e-1,-1.95215562e-1,2.68336193e-1),(1.02136194e-2,-2.31395216e-2,2.82685779e-1)]):
 i=1+2*j; C[i:i+2,i:i+2]=[[a,b],[b,c]]
assert np.array_equal(C,C.T); F=cho_factor(C); w=lambda x:cho_solve(F,x)
