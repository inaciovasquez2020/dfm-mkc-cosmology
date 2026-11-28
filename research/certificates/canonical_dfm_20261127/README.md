# Canonical quadratic charged-field: finite-interval dust bound and DESI DR2 continuation

Base repository: inaciovasquez2020/dfm-mkc-cosmology, ea4f548e5c9b3160ea0a4dde76cab74be6a4964f. Source calibration: artifacts/dfm_mkc/dfm_cdm_minimal_circular_solution_receipt_2026_07_21.json. BAO measurements and covariance transcribed from CobayaSampler/bao_data revision bb0c1c9009dc76d1391300e169e8df38fd1096db, desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt (blob SHAs 8aff444fdb42c0946342aa0011ab287eda097c4c and fd8e5697ab61379b07b52efb781ea6713417a4d9). Original row order preserved.

## Analytic result (PROVED, not Lean verified)

Assume a>0, H=dot a/a>=0 is differentiable and nonincreasing, m>0, and a nonzero complex homogeneous quadratic field obeys ddot psi+3H dot psi+m^2 psi=0. Set rho=(|dot psi|^2+m^2|psi|^2)/2, p=(|dot psi|^2-m^2|psi|^2)/2, E=a^3 rho, J=a^3 Re(conj(psi) dot psi), Q=a^3 Im(conj(psi) dot psi). Direct differentiation yields dot E=-3Ha^3p, dot J=2a^3p, dot Q=0. Thus I=E+(3/2)HJ obeys dot I=(3/2)dot H J. The elementary inequality (|dot psi|-m|psi|)^2>=0 gives E>=m sqrt(J^2+Q^2)>=m|J|, and E>=m|Q|. In particular circular initial conditions with radial velocity zero and angular frequency m attain E=m|Q| exactly. This lower bound persists through evolution.

Put epsilon=3H/(2m). On any interval [s,t] with epsilon(s)<1, (1-epsilon)E<=I<=(1+epsilon)E and I>0. Since |dot I/I|<=|dot epsilon|/(1-epsilon), integration with nonincreasing epsilon proves

    (1-eps_s)/(1-eps_t) <= I(t)/I(s) <= (1-eps_t)/(1-eps_s).

Combining the pointwise inequalities yields the finite-interval dust-energy bound

    (1-eps_s)^2/[(1-eps_t)(1+eps_t)] <= E(t)/E(s)
      <= (1-eps_t)(1+eps_s)/[(1-eps_s)(1-eps_t)]
      = (1+eps_s)/(1-eps_s).

Consequently, E(t)/E(s) approaches 1 uniformly over such intervals as sup H/m tends to zero. The bound is not a perturbation or growth theorem. In the repository's flat FLRW system the nonincreasing H hypothesis follows from nonnegative dust and radiation densities and canonical positive kinetic terms via the Raychaudhuri equation. The estimate is only on intervals where epsilon<1. For the backward comparison in verify.py the code uses the exact present-day I/E ratio rather than bounding that endpoint.

## Numerical result (COMPUTATION_PASS_SCOPED)

Run `python verify.py` with NumPy 2.3.5 and SciPy 1.17.0. The fixed July 21 numerical candidate is continued in Cartesian complex-field variables from N=-0.1 both backward to -log(3.33) and forward to zero, without refitting any field parameters. The original density and pressure residuals and charge are checked. Two independent ODE algorithms (DOP853 and RK45) and full-covariance solves are compared; 4001 background samples check the analytic inequalities. The dimensionless distance amplitude A=c/(H0 r_d) is profiled independently for each model. The matched flat LCDM comparison fixes the same baryon, CDM, radiation and Lambda fractions; no free matter-fraction fit. For the canonical model, chi2=24.82312712; matched LCDM chi2=13.66528429; difference=11.15784283. This is a fixed-candidate late-time test, not a rejection of the canonical model family. No early-time sound horizon calculation, perturbation/growth likelihood, parameter inference or joint observational fit. No claim of physical novelty. Full repo CI and Lean NOT_RUN. No Codex or Claude. Remote main unmodified.
