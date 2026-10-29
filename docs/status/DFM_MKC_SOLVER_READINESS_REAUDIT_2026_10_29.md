# DFM-MKC Solver Readiness Re-audit — 2026-10-29

Status: `ACTION_AND_COVARIANT_FIELD_EQUATIONS_EXIST; COSMOLOGY_SOLVER_PARAMETER_BINDING_BLOCKED`

## Correction to the earlier blocker

The repository does contain the following objects on the audited branch:

- `artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json`
  - Git blob SHA: `e4b28e93e1afe8108cbd96e857187754fdedccb3`
  - Status recorded by source: `CONCRETE_ACTION_FUNCTIONAL_SUPPLIED_PHENOMENOLOGICAL_ONLY`
- `artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json`
  - Git blob SHA: `1c3f86071228a5bc19f3e3ba19c28ad571aea67e`
  - Status recorded by source: `CONCRETE_FIELD_EQUATIONS_DERIVED_PHENOMENOLOGICAL_ONLY`

The action is
`L = (R - 2 Lambda)/(16 pi G) - (alpha/2)(nabla phi)^2 - (beta/2) phi^2 (nabla theta)^2 - U(phi) + L_vis`,
with
`U(phi) = rho_star + (1/2) m_phi_squared phi^2 + (1/4) lambda_phi phi^4`.
The recorded dark-sector equations are
`alpha Box phi - beta phi (nabla theta)^2 - U_prime(phi) = 0`
and
`nabla_mu(beta phi^2 nabla^mu theta) = 0`,
coupled to Einstein's equation with the stated stress-energy tensor.

This corrects the older statement that no closed action/equation object exists. Their existence does not itself establish empirical validity, and the action is explicitly described as phenomenological.

## Parameter freeze is still absent for this action

The action's allowed parameters are `G, Lambda, alpha, beta, m_phi_squared, lambda_phi, rho_star`, with constraints but no fully frozen numerical cosmology parameter packet tied to a BAO/shear prediction.

The prior artifact `complete_dfm_parameter_prior_and_numerical_solver_interface_2026_05_22.json` instead lists `H0, Omega_b0, Omega_c0, Omega_r0, V0, lambda, beta, Phi_i, dot_Phi_i` and prior ranges. Those are not a mapping that identifies the action's `phi, theta, U(phi)` parameters with the solver variables and equations.

## Existing background script is not a solver for the canonical action above

`scripts/dfm_background_solver.py` integrates the state `(Phi, dot_Phi, rho_b, rho_c, rho_r)` with
`V(Phi) = V0 exp(-lam Phi)`
and explicit `beta rho_c` exchange terms. It has no structural phase `theta), no `phi^2 (nabla theta)^2` term, and its RHS is not shown to be reduced from the 2026-05-27 action/equations. Its existing run is a synthetic `lambda=beta=dot_Phi_i=0` limit check, not a numerical DFM-MKC cosmological prediction.

Therefore, reusing its synthetic parameter values or its Lambda-CDM limit as a frozen fit would silently change models. Do not use it to calculate the DESI vector or KiDS shear prediction.

## Data gate

DESI DR2 vector/covariance pins remain documented in `DESI_DR2_BAO_DATA_PIN_2026_10_29.md`. An independent download/hash run has not been completed: the independent raw-URL access path failed in this session, so the existing SHA-256 values remain based on the previous commit-pinned retrieval plus GitHub blob metadata.

KiDS-Legacy remains the selected weak-lensing release, but its 125 MB official archive was not downloaded and inspected. The vector/covariance bytes, dimensions, bin ordering, redshift distributions, and hashes are not yet pinned.

## Required next gate

1. Establish whether the 2026-05-27 amplitude-phase action is the intended cosmological model for this comparison, rather than the separate exponential-potential interacting-scalar core.
2. Derive and test the homogeneous FLRW reduction from the selected action, including phase dynamics and its stress-energy; identify physically justified numerical parameter values and initial conditions before freezing them.
3. Implement the resulting solver with numerical convergence and known-limit tests. Do not map parameters by name alone or add matter-exchange terms absent from the selected action.
4. Independently download and hash the pinned DESI files; download and inspect the official KiDS-Legacy archive and pin the exact vector, covariance, redshift distributions, ordering, and units.
5. Only then generate predictions, freeze shared likelihood/nuisance treatment and the ΛCDM baseline, and run the matched comparison.

## Claim boundary

No DFM-MKC BAO prediction vector, KiDS shear prediction, residual vector, chi-squared, likelihood ratio, or matched model comparison was produced by this audit. No empirical status is promoted.
