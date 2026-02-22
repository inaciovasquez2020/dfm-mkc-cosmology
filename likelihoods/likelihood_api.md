Likelihood API

Inputs
Dataset must be provided as CSV in data/
User supplies file paths and columns

Required model functions
H_of_z(z, theta)
dL_of_z(z, theta)
Optional
dA_of_z(z, theta)
chi_of_z(z, theta)

Supernova likelihood
mu_model(z) = 5 log10(dL(z)) + M
chi2 = sum_i ((mu_i - mu_model(z_i))/sigma_i)^2
M is nuisance parameter analytically or numerically marginalized

BAO likelihood (generic)
Use supplied observable columns, e.g.
DV_over_rd(z) or DM_over_rd(z) or DH_over_rd(z)
Compute model values from H(z), chi(z) and a supplied rd

CMB distance priors (optional)
Use compressed parameters provided by the user
