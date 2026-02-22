Background Equations Numerical Scaffold

State:
y(z) = [H(z), Phi(z)]

Inputs:
theta = (H0, Omega_m0, Omega_r0, Omega_Lambda0, alpha, beta)

Auxiliary:
rho_i(z) = rho_i0 (1+z)^(3(1+w_i))
p_i(z) = w_i rho_i(z)
rho(z) = sum_i rho_i(z)
p(z) = sum_i p_i(z)

Constraint:
H(z)^2 = (8πG/3) rho(z) + Phi(z)

ODE form:
dH/dz = f_H(H, Phi, z; theta)
dPhi/dz = f_Phi(H, Phi, z; theta)

Initial conditions:
H(0) = H0
Phi(0) = H0^2 Omega_Phi0
Omega_Phi0 = 1 - (Omega_m0 + Omega_r0 + Omega_Lambda0)

Output targets:
H(z)
chi(z) = ∫_0^z dz'/H(z')
dL(z) = (1+z) chi(z)
dA(z) = chi(z)/(1+z)
