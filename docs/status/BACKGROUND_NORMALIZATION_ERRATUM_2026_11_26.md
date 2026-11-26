# Background equations and normalization audit

Paper derivation; no empirical or Lean verification.

The earlier fluid manuscripts now retain the interacting cold-matter solution explicitly in Friedmann's equation and distinguish uncoupled constant-w from the cosmological constant limit.

Separate scalar solver (scripts/dfm_background_solver.py): in the default constant-field, zero-coupling limit its analytic H_dimensionless^2 at N=0 is (3*(Omega_b0+Omega_c0+Omega_r0)+V0)/3 = 160018/300000 = 0.533393333.... With H_dimensionless=H/H0 and the displayed Omega values interpreted as present fractions, the required potential is V0=3*(1-Omega_b0-Omega_c0-Omega_r0)=2.09973, not 0.69991. The existing synthetic sanity check uses the same expression as the solver and does not independently check H/H0=1. In the coupled case rho_c(N)=rho_c(N_i) exp(-3*(N-N_i)-beta*(Phi(N)-Phi(N_i))); the initialization at N_i does not generally fix the present cold-matter fraction.

The inspected natural-unit parameter table concerns a distinct scalar-vector action and does not settle this solver's dimensionless convention. H0 is not used in the inspected scalar RHS. Preserve historical outputs and code until a convention is explicitly fixed and a separately normalized solver/test is validated. The other solver/background_solver.py is a distinct IVP; no equivalence assumed. No numerical run, no artifact regeneration, no physical-model promotion.
