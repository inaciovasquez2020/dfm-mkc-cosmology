# DFM-CDM minimal circular solution receipt

Status: `DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_2026_07_21`

Classification: `conditional_numerical_background_calibration_solution`

Conditional: `true`

## Fixed branch

The receipt fixes

\[
\alpha=\beta=1,\qquad
v_i=0,\qquad
\rho_\star=0,\qquad
\lambda_\phi=0,\qquad
Q_\theta>0,
\]

and imposes the initial circular-force equation.

The calibrated vector, ordered as

\[
(\phi_i,v_i,\rho_\star,m_\phi^2,\lambda_\phi,Q_\theta),
\]

is

\[
(0.06404492230824137,\ 0,\ 0,\ 256.0366189147147,\ 0,\
0.048621919894669685).
\]

## Calibration residuals

The six augmented residuals are

\[
(-4.440892098500626\times10^{-16},
7.216449660063518\times10^{-16},
0,0,0,
-1.4210854715202004\times10^{-14}).
\]

The maximum absolute augmented residual is

\[
1.4210854715202004\times10^{-14}.
\]

The omitted dependent diagnostic is

\[
F_H=-1.1102230246251565\times10^{-16}.
\]

## Local structure

The full six-parameter augmented Jacobian has rank six. Its raw condition
number is approximately \(3.73\times10^6\), reflecting the different
parameter scales.

Across nine finite-difference scales, the observed rank remains six and the
smallest singular value changes by a factor of only
`1.0000248460669445`.

In the two log coordinates used by the reduced solve,

\[
(\log\phi_i,\log Q_\theta),
\]

the minimum tested absolute determinant is `0.3794387547618709`, the maximum
condition number is `13.120237940984913`, and the smallest singular value
changes by a factor of only `1.000000500330148`.

## Boundary

This receipt establishes a conditional numerical background-calibration
solution only.

Growth likelihood remains blocked.

It does not construct the growth observable forward model, evaluate a
likelihood, or establish observational validation.

Weakest missing object:
`growth_observable_forward_model_and_likelihood_evaluation_from_the_converged_background`.
