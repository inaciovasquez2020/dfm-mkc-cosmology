# FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL

Status: `SUPPLIED_CANDIDATE_DYNAMICAL_CORE_ONLY_NO_VALIDATION`

Model: `MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1`

## Primitive fields

- `g_munu`
- `Phi`
- `psi_b`
- `psi_c`
- `psi_r`
- `T_b_munu`
- `T_c_munu`
- `T_r_munu`
- `T_Phi_munu`
- `T_int_munu`

## Action functional

`S = Integral sqrt(-g)[(M_Pl^2/2)R - 1/2 g^{mu nu} nabla_mu Phi nabla_nu Phi - V0 exp(-lambda Phi/M_Pl)] + S_b[g,psi_b] + S_r[g,psi_r] + S_c[A(Phi)^2 g,psi_c]`

with:

`A(Phi)=exp(beta Phi/M_Pl)`

## Closed equations

- `G_munu = M_Pl^{-2}(T_b_munu + T_r_munu + T_c_munu + T_Phi_munu)`
- `Box Phi - dV/dPhi = -(beta/M_Pl) T_c`
- `nabla^mu T_c_munu = (beta/M_Pl) T_c nabla_nu Phi`
- `nabla^mu T_Phi_munu = -(beta/M_Pl) T_c nabla_nu Phi`
- `nabla^mu(T_b_munu + T_r_munu + T_c_munu + T_Phi_munu)=0`

## FLRW reduction

- `H^2=(1/(3M_Pl^2))(rho_b+rho_r+rho_c+rho_Phi)`
- `dot(H)=-(1/(2M_Pl^2))(rho_b+rho_c+4rho_r/3+dot(Phi)^2)`
- `dot(rho_b)+3H rho_b=0`
- `dot(rho_r)+4H rho_r=0`
- `dot(rho_c)+3H rho_c=-(beta/M_Pl)rho_c dot(Phi)`
- `ddot(Phi)+3H dot(Phi)-(lambda/M_Pl)V0 exp(-lambda Phi/M_Pl)=(beta/M_Pl)rho_c`

## Observable prediction map

- `H(z)`
- `D_C(z)`
- `D_A(z)`
- `D_L(z)`
- BAO vector: `D_M(z)/r_d`, `H(z)r_d`, `D_V(z)/r_d`
- CMB/ACT compressed vector: `R`, `ell_A`, `omega_b`, `omega_c`
- SNe/DES vector: `mu(z)`
- growth observable with `G_eff=G(1+2beta^2)`
- score rule: `chi2_total=chi2_BAO+chi2_CMB_compressed+chi2_SNe+chi2_growth`

## Lambda-CDM embedding

`beta=0`, `lambda=0`, `dot_Phi_i=0`, and constant `V0` recover background Lambda-CDM with `Lambda_eff=V0/M_Pl^2`.

## Does not prove

- DFM-MKC validation
- Lambda-CDM failure
- dark matter resolution
- dark energy resolution
- gravity closure
- empirical validation
- P vs NP
- any Clay problem

## Next admissible object

`COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE`
