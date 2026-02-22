CLASS Background C Module Scaffold

Goal
Provide a minimal C callable background that returns H(z) and optionally Phi(z) for integration into a CLASS-style pipeline.

Interface provided here
A standalone C ODE integrator is not included
This scaffold defines data structures and function signatures
It is intended to be wired into CLASS background.c as a custom model

Expected integration points in CLASS
background_init
background_solve
background_at_z

Required outputs
H(z)
Optionally rho_tot(z) and Phi(z)
