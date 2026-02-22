CLASS Interface Stub

Goal
Expose a background module returning H(z) and derived distances for the deformation model.

Inputs
theta = (H0, Omega_m0, Omega_r0, Omega_Lambda0, alpha, beta)

Background ODEs
Use redshift-form system to integrate y(z) = [H(z), Phi(z)] with initial conditions at z = 0.

Required callable surfaces
H_of_z(z, theta)
background_table(z_array, theta) returning arrays for H, Phi, chi, dL, dA

Derived distances
chi(z) = integral_0^z dz'/H(z')
dL(z) = (1+z) chi(z)
dA(z) = chi(z)/(1+z)

Validation
H(z) > 0 on integration domain
finite H(z) and bounded Phi(z)/H(z)^2 on integration domain
