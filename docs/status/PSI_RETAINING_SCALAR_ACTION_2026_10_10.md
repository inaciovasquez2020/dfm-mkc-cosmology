# Psi-retaining scalar quadratic action — 2026-10-10

Status: `SYMBOLIC_DERIVATION_ADDED; CI_VALIDATION_PENDING`

## Model and perturbation ansatz

The derivation reuses `tools/audit_generalized_proca_l4_scalar_sector_v1.py`'s explicit model completion:
- a separate scalar-tensor term (F(\phi)R/2);
- the linear generalized-Proca (L_4) completion (G_4(X)=-\xi X/2), (G_{4X}=-\xi/2);
- the same scalar potential, vector mass function, Maxwell term, and scalar kinetic term.

The new script `tools/derive_psi_retaining_scalar_action_v1.py` changes the spatial metric to
[
h_{ij}=a(t)^2(1-2\epsilon\psi(t,z))\delta_{ij},
]
retains the lapse-like perturbation (\Phi), scalar shift (\beta), scalar fluctuation (\sigma), and vector perturbations (u,\chi), and uses the spatial scalar-shear gauge (E=0). It expands the covariant action through order (\epsilon^2), Fourier-reduces the quadratic Lagrangian, derives the six Euler–Lagrange equations, and computes the kinetic and candidate-auxiliary Hessians.

## What this supplies

- A reproducible symbolic construction of the ψ-retaining quadratic action for this explicit model completion.
- The full six-field linearized Euler–Lagrange system, conditional on the chosen background satisfying its zeroth-order equations.
- The (\Phi,\beta,u) variations identified as constraint candidates; their status must be checked using the full equations and background equations, not inferred from Hessian rank alone.

## What remains unproved

- The output is not yet a reduced, independently checked set of explicit constraint solutions.
- The background equations have not been substituted into the perturbation system here.
- No physical scalar degree-of-freedom count, kinetic-sign/gradient-stability result, or new cosmological effect follows from this derivation alone.
- The equivalence of this explicit completion to any broader intended action remains conditional on the model definition.

## Next structural boundary

Run the new CI verifier. If it passes, substitute the background equations, solve the linear constraints without dividing by unverified factors, and compute the reduced kinetic/gradient matrices. Stop at the first singular branch or unproved denominator.
