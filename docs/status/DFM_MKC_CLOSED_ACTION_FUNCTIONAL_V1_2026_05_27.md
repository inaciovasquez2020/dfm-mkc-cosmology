# DFM-MKC Closed Action Functional V1 — 2026-05-27

Status: `CONCRETE_ACTION_FUNCTIONAL_SUPPLIED_PHENOMENOLOGICAL_ONLY`

This file supplies `DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1`, the first concrete mathematical object required by the dark-sector closed-object target packet.

Source dependency:

`DFM_MKC_DARK_SECTOR_CLOSED_OBJECT_TARGET_PACKET_2026_05_27`

## Object type

Closed covariant action functional.

## Spacetime domain

Let `M` be a smooth oriented four-dimensional Lorentzian manifold, with boundary `partial M` allowed.

The metric is `g_{mu nu}` with signature `(-,+,+,+)`.

The invariant measure is:

```text
d^4x sqrt(-g)
Natural units are used:
c = hbar = 1
Field inventory
Geometric field:
g_{mu nu}
DFM-MKC dark-sector fields:
phi   : M -> R
theta : M -> R / 2pi Z
Visible-sector fields:
psi_vis
The visible sector appears only through:
L_vis(psi_vis, g)
in this V1 action.
Dynamical variables
g_{mu nu}
phi
theta
psi_vis
Allowed parameters
G                 > 0
Lambda            real
alpha             > 0
beta              > 0
m_phi_squared     real
lambda_phi        >= 0
rho_star          real
Potential
U(phi) = rho_star + (1/2) m_phi_squared phi^2 + (1/4) lambda_phi phi^4
Lagrangian density
L_total =
  (R - 2 Lambda)/(16 pi G)
  - (alpha/2) g^{mu nu} nabla_mu phi nabla_nu phi
  - (beta/2) phi^2 g^{mu nu} nabla_mu theta nabla_nu theta
  - U(phi)
  + L_vis(psi_vis, g)
Dark-sector part:
L_DFM_MKC =
  - (alpha/2) g^{mu nu} nabla_mu phi nabla_nu phi
  - (beta/2) phi^2 g^{mu nu} nabla_mu theta nabla_nu theta
  - U(phi)
Gravity part:
L_grav = (R - 2 Lambda)/(16 pi G)
Action integral
S_DFM_MKC_V1[g, phi, theta, psi_vis]
  =
  int_M d^4x sqrt(-g) L_total
  + S_GHY[g]
For nonempty boundary:
S_GHY[g] =
  (1/(8 pi G)) int_{partial M} d^3y sqrt(|h|) K
No post-hoc source terms are allowed in this V1 object.
Variation rules
Metric variation:
Vary g^{mu nu} with fixed induced boundary metric.
Rigidity-amplitude variation:
Vary phi with compact support or fixed boundary value.
Phase variation:
Vary theta as a periodic scalar with compact support or fixed boundary value.
Visible-sector variation:
Vary psi_vis according to L_vis.
The field-equation derivation is deferred to:
DFM_MKC_FIELD_EQUATIONS_V1
Boundary terms
Gravitational boundary:
Gibbons-Hawking-York term included.
Scalar boundary:
Dirichlet or compact-support variations for phi and theta.
No extra boundary sources are introduced.
Units and dimensions
[action]              = dimensionless
[Lagrangian density]  = mass^4
[phi]                 = mass
[theta]               = dimensionless
[alpha]               = dimensionless
[beta]                = dimensionless
[m_phi_squared]       = mass^2
[lambda_phi]          = dimensionless
[rho_star]            = mass^4
[G]                   = mass^-2
[Lambda]              = mass^2
Reduction to known limits
Limit:
phi = 0 and rho_star absorbed into Lambda
Result:
Einstein-Hilbert gravity with cosmological constant and visible matter.
Limit:
theta constant
Result:
Single real scalar rigidity-amplitude action minimally coupled to gravity.
Limit:
g_{mu nu} -> eta_{mu nu}
Result:
Flat-spacetime scalar amplitude-phase field theory with quartic potential.
Limit:
alpha = beta = 0 and U(phi) constant
Result:
No propagating DFM-MKC dark-sector degrees of freedom; only a vacuum-energy shift remains.
Acceptance result
This supplies the required closed action functional object:
DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1
The action is closed as a variational principle.
Field equations are derivable from this object without post-hoc terms, but the derivation itself is not claimed here.
Downstream objects still required
DFM_MKC_FIELD_EQUATIONS_V1
DFM_MKC_MATTER_COUPLING_RULE_V1
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
Boundary
Does not prove:
DFM-MKC field equations.
DFM-MKC matter coupling law.
DFM-MKC linear perturbation system.
DFM-MKC ACT Planck DESI prediction vector.
DFM-MKC empirical validation.
Lambda-CDM failure.
Dark matter replacement.
Dark matter is liquid.
Dark matter is solid.
Dark matter is a phase.
Dark energy resolution.
Dark matter resolution.
Gravity closure.
Chronos-RR.
Unrestricted H4.1/FGL.
P vs NP.
Any Clay problem.
Next admissible step
Derive DFM_MKC_FIELD_EQUATIONS_V1 from this action functional.
