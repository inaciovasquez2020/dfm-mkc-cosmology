# COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE

Status: `SOLVER_INTERFACE_ONLY_NO_EXECUTED_VALIDATION`

Depends on:

- `FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL`
- `MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1`

## Parameter vector

| Symbol | Meaning | Units | Prior | Range | Status |
|---|---|---|---|---|---|
| `H0` | present Hubble parameter | km s^-1 Mpc^-1 | uniform | `[40,100]` | free |
| `Omega_b0` | baryon fraction | dimensionless | uniform | `[0.01,0.12]` | free/external |
| `Omega_c0` | coupled cold dark-sector fraction | dimensionless | uniform | `[0,0.6]` | free |
| `Omega_r0` | radiation fraction | dimensionless | fixed/external | `[0,0.001]` | fixed/external |
| `V0` | scalar potential amplitude | critical-density units | log-uniform | `[1e-8,10]` | free |
| `lambda` | exponential-potential slope | dimensionless | uniform | `[0,10]` | free |
| `beta` | dark-sector conformal coupling | dimensionless | uniform | `[-2,2]` | free |
| `Phi_i` | initial scalar value | M_Pl | uniform | `[-10,10]` | free |
| `dot_Phi_i` | initial scalar velocity | M_Pl H0 | uniform | `[-10,10]` | free |

## Solver interface

Independent variable:

`N = ln(a)`

State vector:

`y = (a, Phi, dot_Phi, rho_b, rho_c, rho_r)`

Required RHS outputs:

- `dPhi_dN`
- `ddot_Phi_dN`
- `drho_b_dN`
- `drho_c_dN`
- `drho_r_dN`
- `H_of_N`

Constraint surface:

- `H^2=(1/(3M_Pl^2))(rho_b+rho_r+rho_c+0.5 dot_Phi^2+V0 exp(-lambda Phi/M_Pl))`
- `rho_b>=0`
- `rho_c>=0`
- `rho_r>=0`
- `H>0`
- `V0>0`

Lambda-CDM limit:

`beta=0`, `lambda=0`, `dot_Phi_i=0`, `V0=constant`

## Observable interface

- `H(z)`
- `D_C(z)`
- `D_A(z)`
- `D_L(z)`
- `D_M(z)/r_d`
- `H(z) r_d`
- `D_V(z)/r_d`
- `R`
- `ell_A`
- `omega_b`
- `omega_c`
- `mu(z)`
- `f_sigma8(z)`

Score rule:

`chi2_total=chi2_BAO+chi2_CMB_compressed+chi2_SNe+chi2_growth`

Likelihood rule:

`logL(theta)=-(1/2)chi2_total(theta)`

## Does not prove

- DFM-MKC validation
- Lambda-CDM failure
- dark matter resolution
- dark energy resolution
- gravity closure
- empirical validation
- ACT validation
- DESI validation
- DES validation
- P vs NP
- any Clay problem

## Next admissible object

`EXECUTABLE_DFM_BACKGROUND_SOLVER_WITH_SYNTHETIC_SANITY_CHECK`
