# Psi-retaining scalar quadratic action — 2026-10-10

Status: `SYMBOLIC_DERIVATION_MERGED; PR_HEAD_CI_PASSED; CONSTRAINT_REDUCTION_OPEN`

## Model and perturbation ansatz

The derivation reuses `tools/audit_generalized_proca_l4_scalar_sector_v1.py`'s explicit model completion:
- a separate scalar-tensor term (F(\phi)R/2);
- the linear generalized-Proca (L_4) completion (G_4(X)=-\xi X/2), (G_{4X}=-\xi/2);
- the same scalar potential, vector mass function, Maxwell term, and scalar kinetic term.

The script `tools/derive_psi_retaining_scalar_action_v1.py` retains the spatial-curvature perturbation in
\[
h_{ij}=a(t)^2(1-2\epsilon\psi(t,z))\delta_{ij},
\]
retains the lapse-like perturbation (\Phi), scalar shift (\beta), scalar fluctuation (\sigma), and vector perturbations (u,\chi), and uses the spatial scalar-shear gauge (E=0). It expands the covariant action through order \(\epsilon^2\), Fourier-reduces the quadratic Lagrangian, derives the six Euler–Lagrange equations, and computes the kinetic and candidate-auxiliary Hessians.

## What is verified

- A reproducible symbolic construction of the \(\psi\)-retaining quadratic action for this explicit model completion.
- The six-field Euler–Lagrange system is generated for \((\Phi,\psi,\beta,\sigma,u,\chi)\).
- The PR-head `cosmology-check` and `CI` workflows passed for PR #303. The separate Lean CI job was disabled, not verified.
- The \((\Phi,\beta,u)\) variations are constraint candidates; their status must be checked using the full equations and background equations, not inferred from Hessian rank alone.

## What remains unproved

- The background equations have not been substituted into the perturbation system.
- No explicit, independently checked solution of the full linear constraint system has been produced.
- No physical scalar degree-of-freedom count, kinetic-sign/gradient-stability result, or new cosmological effect follows from this derivation alone.
- The equivalence of this explicit completion to any broader intended action remains conditional on the model definition.

## Next structural boundary

Derive the background-reduced linear constraints for the same explicit action. Substitute only verified background equations, solve for constraint variables without dividing by unverified factors, and record singular branches explicitly. Only after this reduction, compute the reduced kinetic/gradient matrices. Stop at the first unresolved denominator or branch.
