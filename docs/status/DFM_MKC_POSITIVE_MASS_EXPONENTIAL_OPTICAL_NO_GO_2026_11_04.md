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

## Repository dependencies

- [DFM–MKC V1 field equations](DFM_MKC_FIELD_EQUATIONS_V1_2026_05_27.md)
- [DFM–MKC V1 matter coupling](DFM_MKC_MATTER_COUPLING_RULE_V1_2026_05_27.md)
- [Existing spherical reduction and asymptotic obstruction](DFM_MKC_HARMONIC_PHASE_ASYMPTOTIC_BOUNDARY_2026_10_11.md)
- [Optical source map](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/main/docs/status/FINITE_CAPACITY_OPTICAL_METRIC_DEFLECTION_SOURCE_MAP_2026_05_23.md)

**NEXT_ACTIONS :=** Retain this conditional obstruction; do not integrate, ray-trace, or compare against GR for this branch.
