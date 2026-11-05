# Conditional no-go: positive-mass exterior vs. exponential optical index

**Date:** 2026-11-04  
**Status:** \`CONDITIONAL_NO_GO\`  
**Model:** Canonical, minimally coupled DFM–MKC V1. This statement excludes a **restricted exterior branch only**. It is not a theorem of universal gravitational deflection, a rejection of all DFM–MKC solutions, or an empirical discovery.

## Target

The finite-capacity optical source map records

\[
n_{\mathrm{target}}(\rho)=1-\varepsilon e^{-\rho/R},
\quad 0<\varepsilon<1,\ R>0,\ \rho\ge\rho_0>0,
\]

where \(\rho\) is an asymptotically normalized isotropic radius.

## Hypotheses (independent of the target profile)

- Exterior visible stress-energy vanishes. Metric in areal radius \(r\):
  \[
  ds^2=-e^{2\nu(r)}dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,\qquad
  f(r)=1-\frac{2Gm(r)}r.
  \]
- Static amplitude \(\phi=\phi(r)\), constant phase \(\theta=\theta_0\); \(\alpha,\beta>0\), \(m_\phi^2>0\), \(\lambda_\phi\ge0\).
- Vacuum normalization \(\Lambda+8\pi G\rho_*=0\), so \(V(\phi)=\frac12m_\phi^2\phi^2+\frac14\lambda_\phi\phi^4\ge0\).
- Independent inner data: \(m(r_0)=m_0>0\), \(r_0>2Gm_0\), with finite \(\phi(r_0)=\phi_0\), \(\phi'(r_0)=\psi_0\).
- Hypothesize a smooth static exterior solution with \(f>0\), finite ADM mass, \(\nu(\infty)=0\), and \(\phi\to0\). Use the isotropic normalization \(\rho/r\to1\). No pointwise pressure-decay hypothesis is needed.

## Field equations and mass inequality

The canonical equations reduce on this branch to

\[
m'=4\pi r^2\left[\frac{\alpha f}{2}(\phi')^2+V(\phi)\right]\ge0,
\qquad
p_r=\frac{\alpha f}{2}(\phi')^2-V(\phi),
\]

\[
\nu'=\frac{G(m+4\pi r^3p_r)}{r^2f},
\]

\[
\alpha\left[f\phi''+\left(\frac{f'}2+f\nu'
+\frac{2f}{r}\right)\phi'\right]-V'(\phi)=0.
\]

The phase equation is identically satisfied. Thus

\[
M_{\rm ADM}=\lim_{r\to\infty}m(r)\ge m_0>0.
\]

## Integrated pressure-tail lemma (derived, not assumed)

Write \(K=\alpha f(\phi')^2/2\ge0\). As \(V\ge0\), the canonical scalar equations give \(\rho_{\rm scalar}=K+V\) and \(p_r=K-V\); hence \(|p_r|\le \rho_{\rm scalar}\). Finite ADM mass and \(m'=4\pi r^2\rho_{\rm scalar}\) yield

\[
\int_{r_0}^\infty s^2|p_r(s)|\,ds
\le\frac{M_{\rm ADM}-m_0}{4\pi}<\infty.
\]

Because \(m(s)\to M_{\rm ADM}\) and \(f(s)=1-2Gm(s)/s\to1\), for large \(s\) we have \(1/f(s)\le2\). Integrate the exact lapse equation with \(\nu(\infty)=0\):

\[
\nu(r)=-G\int_r^\infty\frac{m(s)}{s^2 f(s)}\,ds
-4\pi G\int_r^\infty\frac{s p_r(s)}{f(s)}\,ds.
\]

The first integral equals \(-GM_{\rm ADM}/r+o(r^{-1})\) after its negative sign. The second term satisfies

\[
\left|4\pi G\int_r^\infty\frac{s p_r(s)}{f(s)}\,ds\right|
\le\frac{8\pi G}{r}\int_r^\infty s^2|p_r(s)|\,ds
=o(r^{-1}).
\]

Therefore the exact coupled equations already imply

\[
\boxed{\nu(r)=-\frac{GM_{\rm ADM}}r+o(r^{-1}).}
\]

**SCOPE:** This proves the asymptotic expansion needed below; it does not assert the stronger pointwise limit \(r^3p_r(r)\to0\). The latter has been removed as an unnecessary hypothesis.

## Exact optical relation and contradiction

The isotropic-radius relation and optical index are

\[
\frac{d\rho}{\rho}=\frac{dr}{r\sqrt f},
\qquad n(\rho)=\frac{r(\rho)}{\rho}e^{-\nu(r(\rho))}.
\]

Under the stated asymptotics:

\[
f=1-\frac{2GM_{\rm ADM}}r+o(r^{-1}),\quad
\nu=-\frac{GM_{\rm ADM}}r+o(r^{-1}),
\]

which gives

\[
n(\rho)=1+\frac{2GM_{\rm ADM}}\rho+o(\rho^{-1}),
\quad
\lim_{\rho\to\infty}\rho[n(\rho)-1]=2GM_{\rm ADM}>0.
\]

But the target has

\[
\lim_{\rho\to\infty}\rho[n_{\rm target}(\rho)-1]=0.
\]

An exact match throughout the exterior would require \(M_{\rm ADM}=0\), contradicting \(M_{\rm ADM}\ge m_0>0\).

**RESULT := CONDITIONAL_NO_GO** for this asymptotically flat, positive-inner-mass, nonnegative-scalar-energy exterior branch.

**BOUNDARY :=** No conclusion about non-asymptotically flat or nonlocalized solutions, altered potentials, nonconstant phase, nonzero exterior visible sources, different optical profiles, or unrestricted DFM–MKC gravity. No ray tracing or general-relativity deflection comparison is authorized for this excluded branch. No new theorem-level physical claim is promoted.

## Separate finite-annulus compatibility check (not the global-tail theorem)

The January 19, 2026 [original finite-capacity optical essay](https://github.com/inaciovasquez2020/urf-textbook/blob/main/docs/essays/GRF_2026_FINITE_CAPACITY_SPACETIME_DEFLECTION.tex) uses the **one-function spatially flat** metric
\[
ds^2=-A(r)\,dt^2+dr^2+r^2d\Omega^2,\qquad
n_{\rm analog}(r)=A(r)^{-1/2},
\]
on a bounded annulus \(r_0\le r\le r_1<\infty\). In this ansatz \(r\) is both areal radius and a Euclidean isotropic radius, so its optical radial-coordinate interpretation is fixed.

**Conditional compatibility test:** Ask whether this *exact* one-function spacetime metric is simultaneously a solution of the canonical DFM–MKC V1 Einstein–scalar equations, with constant phase, no exterior visible matter, vacuum-normalized cosmological constant, \(m_\phi^2>0\), \(\lambda_\phi\ge0\), and \(\alpha>0\). This is a separate question from whether the analog refractive-index profile is mathematically realizable in an optical medium.

The general spherical metric has \(g_{rr}=1/f(r)\) and \(f=1-2Gm/r\). The one-function metric enforces \(f\equiv1\), hence \(m\equiv0\) and \(m'\equiv0\) on the annulus. Since
\[
m'=4\pi r^2\left[\frac{\alpha}{2}(\phi')^2+V(\phi)\right]=0,
\]
and both summands are nonnegative, \(\phi'=0\) and \(V(\phi)=0\). Because \(m_\phi^2>0\), \(\phi=0\), so \(p_r=0\). The exact lapse equation yields
\[
\nu'=\frac{G(m+4\pi r^3p_r)}{r^2 f}=0,
\qquad A(r)=e^{2\nu(r)}=\text{constant},
\qquad n_{\rm analog}'(r)=0.
\]
But the original example \(n_{\rm analog}(r)=1-\varepsilon e^{-r/R}\), with \(0<\varepsilon<1\), \(R>0\), has \(n_{\rm analog}'(r)=(\varepsilon/R)e^{-r/R}>0\) everywhere on the annulus. **Therefore that exact one-function metric cannot be a canonical constant-phase DFM–MKC V1 Einstein–scalar solution under these matter assumptions, even locally.**

**BOUNDARY:** This does **not** contradict the finite-annulus analog-optical construction itself, and does not exclude a two-function gravitational metric, other matter, altered scalar potential, nonconstant phase, or a local-to-global matching construction. The positive-inner-mass global-tail theorem above also remains logically separate.

## Draft clarification: radial null energy and two-function boundary data

**Status:** `CONDITIONAL_LOCAL_NEC_OBSTRUCTION; TWO_FUNCTION_EXISTENCE_OPEN`. This is a mathematical check of the *spacetime* interpretation of the January 19 optical analogue, not a claim that passive analogue optical media violate energy conditions.

For the exact one-function metric on `r_0 \le r \le r_1`, with `0<r_0<r_1<\infty`, set `c=1`, `n(r)=1-\varepsilon e^{-r/R}` (`0<\varepsilon<1,\ R>0`) and `N(r)=n(r)^{-1}`:
\[
ds^2=-N(r)^2dt^2+dr^2+r^2d\Omega^2.
\]
Direct calculation of the mixed Einstein tensor gives
\[
G^t{}_t=0,\qquad
G^r{}_r=\frac{2N'}{rN}
=-\frac{2\varepsilon e^{-r/R}}{Rr(1-\varepsilon e^{-r/R})}.
\]
For ordinary Einstein equations with the constant vacuum term absorbed into `\Lambda_{\rm eff}=0`, the orthonormal energy density and radial pressure are
\[
\rho_{\rm matter}=-\frac{G^t{}_t}{8\pi G}=0,\qquad
p_r=\frac{G^r{}_r}{8\pi G}
=-\frac{\varepsilon e^{-r/R}}{4\pi GRr(1-\varepsilon e^{-r/R})}<0.
\]
For the orthonormal radial null vector `k^{\hat a}=(1,1,0,0)`,
\[
T_{\hat a\hat b}k^{\hat a}k^{\hat b}
=\rho_{\rm matter}+p_r
=-\frac{\varepsilon e^{-r/R}}{4\pi GRr(1-\varepsilon e^{-r/R})}<0.
\]
Thus **the exact one-function spacetime metric violates the radial null energy condition at every point of the annulus**, independently of adding a cosmological-constant term (which drops out on null contraction). This is not a statement about an arbitrary two-function metric, modified field equations, or an optical material. For the canonical V1 constant-phase scalar with positive kinetic coupling, by contrast, `\rho_{\rm scalar}+p_r=\alpha f(\phi')^2\ge0` when `f>0`; hence it cannot source this exact one-function metric.

**Next mathematical problem (not solved here).** On the same finite areal-radius annulus, allow two independent metric functions:
\[
ds^2=-e^{2\nu(r)}dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,\quad
f(r)=1-\frac{2Gm(r)}r>0.
\]
Define an increasing isotropic radius by `d\log\rho/dr=1/(r\sqrt f)` and fix its multiplicative normalization through an asymptotically flat continuation (`\rho/r\to1`). The precise optical-profile constraint to test on the annulus is
\[
\frac{r(\rho)}{\rho}e^{-\nu(r(\rho))}
=1-\varepsilon e^{-\rho/R}.
\]
Do not substitute areal `r` for isotropic `\rho` when `f\ne1`. Seek `C^2` metric and scalar functions satisfying the **existing** canonical V1 Einstein--scalar equations and all of the following independent conditions: `r_0>2Gm(r_0)` with `m(r_0)=m_0>0`; finite `\nu(r_0),\phi(r_0),\phi'(r_0)`; `f>0` and `0<n<\infty` on the closed annulus; and a regular exterior continuation with `m(r)\to M_{\rm ADM}>0`, `\nu(r)\to0`, `\phi(r)\to0`. At `r_1`, require continuity of the induced metric and extrinsic curvature (no Israel thin shell), plus continuity of the scalar and its unit-normal derivative (no scalar surface source). In these areal coordinates this requires, in particular, matching `m,\nu,\nu',\phi,\sqrt f\,\phi'` across the interface, with a single time normalization. Test the energy conditions throughout. An exterior *continuation* may change the optical profile outside the annulus: the global exact-tail obstruction above remains unchanged.

**BOUNDARY:** No existence, admissible stress-energy, smooth matching, stability, numerical solution, or physical realization is asserted for this two-function boundary-value problem. Retain PR draft status and its documentation-only classification.

## Repository dependencies

- [DFM–MKC V1 field equations](DFM_MKC_FIELD_EQUATIONS_V1_2026_05_27.md)
- [DFM–MKC V1 matter coupling](DFM_MKC_MATTER_COUPLING_RULE_V1_2026_05_27.md)
- [Existing spherical reduction and asymptotic obstruction](DFM_MKC_HARMONIC_PHASE_ASYMPTOTIC_BOUNDARY_2026_10_11.md)
- [Optical source map](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/main/docs/status/FINITE_CAPACITY_OPTICAL_METRIC_DEFLECTION_SOURCE_MAP_2026_05_23.md)

**NEXT_ACTIONS :=** Retain this conditional obstruction; do not integrate, ray-trace, or compare against GR for this branch.
