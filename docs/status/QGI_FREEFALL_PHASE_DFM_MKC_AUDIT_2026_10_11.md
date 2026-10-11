# Quantum Galileo Interferometer: DFM–MKC prediction audit

**Status:** `STANDARD_COUPLING_REDUCED; LOCAL_METRIC_PREDICTION_OPEN`  
**Date:** 2026-10-11  
**Purpose:** Determine whether the 2026 quantum free-fall phase measurement currently distinguishes the repository's DFM–MKC model from standard gravity.

## 1. Experimental benchmark

O. Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12 (2026), DOI [10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).

The Quantum Galileo Interferometer (QGI) compares an ultracold rubidium matter-wave arm held approximately stationary in the laboratory frame with an arm undergoing ballistic free fall, then measures the relative phase after recombination. The reported phase follows the predicted cubic dependence on free-fall time and agrees with the equivalence-principle prediction in the regime tested.

The result is a test of quantum matter-wave phase in a gravitational field. It is not a demonstration of a complete quantum-gravity theory, nor does it establish that gravity itself is quantized.

## 2. What the repository's V1 action says

The closed-action artifact `artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json` specifies

\[
S=\int d^4x\sqrt{-g}\left[
\frac{R-2\Lambda}{16\pi G}
-\frac{\alpha}{2}(\nabla\phi)^2
-\frac{\beta}{2}\phi^2(\nabla\theta)^2
-U(\phi)+\mathcal L_{\rm vis}
\right]+S_{\rm GHY},
\]

with \(U(\phi)=\rho_*+\tfrac12m_\phi^2\phi^2+\tfrac14\lambda_\phi\phi^4\). The field-equation artifact gives the metric equation sourced by visible and DFM–MKC stress-energy.

The matter-coupling artifact `artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json` specifies **metric-only minimal coupling** for visible matter and photons:
- freely falling massive test bodies follow metric geodesics;
- photons follow null geodesics;
- there is no direct V1 coupling of visible matter or photons to \(\phi\) or \(\theta\);
- no equivalence-principle violation term or direct dark-sector exchange is introduced.

Consequently, the current V1 coupling rule does not predict a new composition-dependent QGI phase or an anomalous direct scalar force. Any difference from the standard prediction would have to arise through a different solved metric sourced by the DFM–MKC stress-energy, not through a new direct matter-wave coupling.

## 3. Standard phase and the missing model-specific quantity

In the coordinate and phase convention of the cited treatment, the standard reference phase is

\[
\Delta\phi_{\rm std}(T,z)
=\frac{m}{\hbar}\left(\frac{g^2T^3}{6}+gzT\right).
\]

The sign of a relative phase depends on arm and pulse conventions, so a quantitative comparison must reproduce the experiment's complete sequence. The (T^3) dependence is the characteristic free-fall term.

For a weak-field description in which a candidate solution induces a potential correction \(\delta\Phi\), a potential-only contribution would be

\[
\delta\phi_{\rm pot}
=-\frac{m}{\hbar}\int_0^{\mathcal T}
\left[\delta\Phi(x_{\rm fall}(t),t)
-\delta\Phi(x_{\rm ref}(t),t)\right]dt,
\]

where \(\mathcal T\) is the full evolution interval. This is only a conditional formula, not a computed DFM–MKC prediction. It excludes other metric, kinetic, internal-state, and pulse contributions unless their absence is derived.

The repository's present artifacts do not supply a solved, weak-field Earth-plus-apparatus metric for the DFM–MKC fields with boundary conditions matched to the QGI geometry. Without that solution, \(\delta\Phi\), the phase correction, and any numerical bound on model parameters are undetermined.

## 4. Keep the two actions distinct

The separate generalized-Proca L4 audit dated 2026-10-10 records an explicit L4 completion of an action containing a scalar-dependent curvature coefficient and a vector background. That completion changes the action and is **not** established to be dynamically equivalent to the canonical DFM–MKC V1 action written above. Its results must not be inserted into this QGI comparison as if they described the same theory.

## 5. Finding and stop boundary

**Finding:** Under the current V1 matter-coupling rule, QGI is a relevant consistency benchmark but not yet a discriminating test of DFM–MKC. The model preserves universal metric coupling at the stated interface level; a distinct predicted phase requires solving the local metric first.

**Not established:**
- a QGI phase shift specific to DFM–MKC;
- a numerical constraint on \(\alpha,\beta,m_\phi^2,\lambda_\phi,\rho_*\);
- a violation of the equivalence principle;
- a new quantum-gravity law or experimentally observed deviation from standard gravity.

**Next mathematical step:** Derive or identify a well-posed weak-field solution of the *same* V1 action around an Earth-like source, with explicit scalar/phase boundary conditions. Then derive the phase along the QGI arms and compare the predicted residual with the published uncertainty and systematic-error budget. If the local solution reduces to the standard metric within the measured regime, record that null result and stop; do not introduce a fitted correction.

## References

1. Dobkowski et al., *Science Advances* (2026), [doi:10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).
2. [DFM–MKC closed action functional V1](../artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json).
3. [DFM–MKC field equations V1](../artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json).
4. [DFM–MKC matter-coupling rule V1](../artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json).
5. [Generalized-Proca L4 scalar perturbation boundary, 2026-10-10](status/GENERALIZED_PROCA_L4_SCALAR_PERTURBATION_BOUNDARY_2026_10_10.md).
