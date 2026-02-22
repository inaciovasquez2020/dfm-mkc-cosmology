Numerics Interface Notes

Goal:
Provide a minimal background module interface compatible with CLASS-style pipelines.

Required functions:
H_of_z(z, theta)
dH_dz(z, y, theta)
dPhi_dz(z, y, theta)

Required constants:
G
c set to 1 if using natural units

Validation checks:
H(z) > 0 for z >= 0
H(z) finite for z in [0, zmax]
Phi(z)/H(z)^2 bounded for z in [0, zmax]
