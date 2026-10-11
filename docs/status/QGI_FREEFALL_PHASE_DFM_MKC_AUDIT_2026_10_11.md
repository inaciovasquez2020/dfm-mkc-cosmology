# Quantum Galileo Interferometer: DFM–MKC prediction audit

**Status:** `STANDARD_COUPLING_REDUCED; LOCAL_METRIC_PREDICTION_OPEN`  
**Date:** 2026-10-11  
**Purpose:** Determine whether the 2026 quantum free-fall phase measurement currently distinguishes the repository's DFM–MKC model from standard gravity.

## 1. Experimental benchmark

O. Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12 (2026), DOI [10.1126/sciadv.aec8045](https://doi.org/10.1126/sciadv.aec8045).

The Quantum Galileo Interferometer (QGI) compares an ultracold rubidium matter-wave arm held approximately stationary in the laboratory frame with an arm undergoing ballistic free fall, then measures the relative phase after recombination. The reported phase agrees with the predicted quantum free-fall phase in the tested low-energy regime [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/) and [Oxford research summary](https://www.physics.ox.ac.uk/news/scientists-observe-einsteins-gravity-quantum-world).

The result is a test of quantum matter-wave phase in a gravitational field. The authors describe it as a test of the interface between quantum theory and gravity; it does not demonstrate a unified quantum-gravity theory or establish that gravity itself is quantized [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/).

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

### Exact constant-field null branch

The V1 equations also permit an exact special branch:
\[
\phi=0,\qquad \theta=\theta_0\text{ (constant)}.
\]
For the specified potential, \(U'(0)=0\) and \(U(0)=\rho_*\), so the scalar-amplitude equation is satisfied and the phase equation is identically satisfied. The dark-sector stress tensor reduces to
\[
T^{\rm DFM\text{-}MKC}_{\mu\nu}=-\rho_* g_{\mu\nu}.
\]
Substitution into the metric equation gives
\[
G_{\mu\nu}+\Lambda_{\rm eff}g_{\mu\nu}
=8\pi G T^{\rm vis}_{\mu\nu},\qquad
\Lambda_{\rm eff}=\Lambda+8\pi G\rho_*.
\]
Thus, on this branch, the exterior metric of a static spherical source is the usual Schwarzschild–de Sitter form (with the effective cosmological constant). The QGI phase is the standard metric-gravity phase after using the local metric and calibrated apparatus parameters; there is no additional DFM–MKC phase term on this branch. This is an exact **conditional null result**, not a statement that every nonconstant-field solution is equivalent to standard gravity. Stability or dynamical selection of this branch is not established.

Consequently, the current V1 coupling rule does not predict a new composition-dependent QGI phase or an anomalous direct scalar force. Any difference from the standard prediction would have to arise through a different solved metric sourced by the DFM–MKC stress-energy, not through a new direct matter-wave coupling.

## 3. Standard phase and the missing model-specific quantity

### Source equation and convention

The primary paper gives the gauge phase relating the Newtonian/laboratory and freely falling wavefunctions as
\[
\varphi_{\rm gauge}(z,t)=\frac{m}{\hbar}\left(-\frac{g^2t^3}{6}-gzt\right),
\]
in its stated convention (Eq. 1). For the idealized symmetric ballistic segment with endpoints at times \(\pm T\), it then gives the relative ballistic phase \(\varphi_{\rm ballistic}=-mg^2T^3/(3\hbar)\) (Eq. 2). The actual QGI observable includes the apparatus' magnetic-gradient kicks and pulse timing; the paper's full interferometer expression must be used for quantitative comparison. Source: [Dobkowski et al., primary paper, Eqs. (1)–(4)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/). The cubic time dependence is the characteristic free-fall signature. The earlier shorthand \(m(g^2T^3/6+gzT)/\hbar\) is the magnitude of the gauge-phase terms under a sign convention, not the complete measured QGI phase, and should not be labeled the experimental observable.

### Conditional potential-only correction derived here

If the same theory yields a nonrelativistic Hamiltonian \(H=p^2/(2m)+m\Phi(x,t)\), the potential contribution to the phase along one arm is \(-\hbar^{-1}\int m\Phi\,dt\). Subtracting the reference arm gives
\[
\delta\phi_{\rm pot}
=-\frac{m}{\hbar}\int_0^{\mathcal T}
\left[\delta\Phi(x_{\rm fall}(t),t)
-\delta\Phi(x_{\rm ref}(t),t)\right]dt.
\]
This expression is derived from the stated Hamiltonian, not quoted as an equation from the QGI paper. It is only a conditional potential contribution, not a computed DFM–MKC prediction; kinetic, metric, internal-state, and pulse contributions must be included unless shown negligible.

The repository's present artifacts do not supply a solved, weak-field Earth-plus-apparatus metric for the DFM–MKC fields with boundary conditions matched to the QGI geometry. Without that solution, \(\delta\Phi\), the phase correction, and any numerical bound on model parameters are undetermined.

## 4. Keep the two actions distinct

The separate generalized-Proca L4 audit dated 2026-10-10 records an explicit L4 completion of an action containing a scalar-dependent curvature coefficient and a vector background. That completion changes the action and is **not** established to be dynamically equivalent to the canonical DFM–MKC V1 action written above. Its results must not be inserted into this QGI comparison as if they described the same theory.

## 5. Finding and stop boundary

**Finding:** The exact constant-field branch predicts no QGI deviation beyond the standard metric-gravity phase, with the vacuum offset absorbed into an effective cosmological constant. The general nonconstant-field model is not yet a discriminating QGI prediction because its local Earth-plus-apparatus metric has not been solved.

**Not established:**
- a nonzero QGI phase shift for general nonconstant DFM–MKC field configurations;
- a numerical constraint on \(\alpha,\beta,m_\phi^2,\lambda_\phi,\rho_*\);
- a violation of the equivalence principle;
- a new quantum-gravity law or experimentally observed deviation from standard gravity.

**Next mathematical step:** Determine whether the nonconstant-field branch admits a regular, stable, weak-field Earth-source solution under explicit boundary conditions. If it does, derive the QGI phase from that metric and compare the predicted residual with the published uncertainty and systematic-error budget. Do not transfer results from the separate generalized-Proca completion or fit a correction to the measurement.

## References

1. O. Dobkowski et al., “Observation of the quantum phase of free fall and the consistency with the equivalence principle,” *Science Advances* 12(36), eaec8045 (2026), [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537235/), [DOI](https://doi.org/10.1126/sciadv.aec8045). The gauge phase and idealized ballistic phase are Eqs. (1)–(2); the apparatus-specific phase is developed later in the article and its supplement.
2. University of Oxford, [research summary](https://www.physics.ox.ac.uk/news/scientists-observe-einsteins-gravity-quantum-world), corroborating the experimental setup and stated limits.
3. [DFM–MKC closed action functional V1](../artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json).
4. [DFM–MKC field equations V1](../artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json).
5. [DFM–MKC matter-coupling rule V1](../artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json).
6. [Generalized-Proca L4 scalar perturbation boundary, 2026-10-10](status/GENERALIZED_PROCA_L4_SCALAR_PERTURBATION_BOUNDARY_2026_10_10.md).
