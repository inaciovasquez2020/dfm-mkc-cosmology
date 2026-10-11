# DFM–MKC harmonic-phase branch: equations and asymptotic obstruction

**Date:** 2026-10-11  
**Status:** DERIVED_REDUCTION; ASYMPTOTICALLY_FLAT_DOUBLE_WELL_BRANCH_OBSTRUCTED  
**Scope:** Canonical minimally coupled DFM–MKC V1 action only. This note does not transfer results from the separate generalized-Proca L4 completion.

## 1. Question

The canonical V1 dark-sector action is

\[
S_{\rm DFM}=\int d^4x\sqrt{-g}\left[
-\frac{\alpha}{2}(\nabla\phi)^2
-\frac{\beta}{2}\phi^2(\nabla\theta)^2
-U(\phi)\right],
\quad
U(\phi)=\rho_*+\frac12m_\phi^2\phi^2+\frac14\lambda_\phi\phi^4,
\]

with \(\alpha,\beta>0\), \(\lambda_\phi\ge0\), and \(m_\phi^2\in\mathbb R\). The metric sector is Einstein gravity with bare cosmological constant \(\Lambda\).

A static radial phase \(\theta=\theta(r)\) has a conserved radial flux and is singular at a regular center when that flux is nonzero and \(\phi(0)\ne0\). The distinct stationary ansatz

\[
\theta(t,r)=\omega t,\qquad \phi(t,r)=\phi(r)
\]

has time-dependent phase but time-independent stress-energy. It is the amplitude-phase form of the harmonic complex-scalar ansatz used in standard boson-star models. This is a valid ansatz to test, not evidence that a solution exists.

## 2. Reduced field equations

Use areal-radius coordinates

\[
ds^2=-e^{2\nu(r)}dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f(r)=1-\frac{2GM(r)}r.
\]

Then \((\nabla\theta)^2=-\omega^2e^{-2\nu}\), and the phase equation

\[
\nabla_\mu(\beta\phi^2\nabla^\mu\theta)=0
\]

is identically satisfied for time-independent \(\phi,\nu,f\) and constant \(\omega\).

The amplitude equation is

\[
\boxed{
\alpha\left[f\phi''+
\left(\frac{f'}2+f\nu'+\frac{2f}{r}\right)\phi'\right]
+\beta\omega^2e^{-2\nu}\phi-U'(\phi)=0.}
\]

This sign follows directly from \(\alpha\Box\phi-\beta\phi(\nabla\theta)^2-U'(\phi)=0\).

For a self-consistent asymptotically flat calculation, tune the constant vacuum offset so that the asymptotic vacuum has zero effective cosmological constant. In the double-well analysis below, define

\[
V(\phi)=U(\phi)-U(v)=\frac{\lambda_\phi}{4}(\phi^2-v^2)^2,
\qquad \Lambda_{\rm eff}=\Lambda+8\pi G U(v)=0.
\]

The radial equations then use this shifted potential \(V\), not \(U\):

\[
\rho=\frac{\alpha f}{2}\phi'^2+
\frac{\beta\omega^2e^{-2\nu}}2\phi^2+V(\phi),
\quad
p_r=\frac{\alpha f}{2}\phi'^2+
\frac{\beta\omega^2e^{-2\nu}}2\phi^2-V(\phi),
\]

\[
\boxed{M'=4\pi r^2\rho,\qquad
\nu'=\frac{G\left(M+4\pi r^3p_r\right)}{r^2f}.}
\]

These Einstein equations apply in the convention \(\Lambda_{\rm eff}=0\) with the vacuum offset absorbed consistently. If a different asymptotic vacuum is chosen, the cosmological constant and potential offset must be retuned together; one must not keep these equations unchanged while changing the vacuum subtraction.

The temporal phase carries a conserved Noether charge; it is not the nonzero radial flux \(Q\) of the static radial-phase ansatz. No claim of stability follows from these reduced equations.

## 3. Boundary test in the double-well regime

Let \(m_\phi^2<0\), \(\lambda_\phi>0\), and

\[
v^2=-\frac{m_\phi^2}{\lambda_\phi}.
\]

The proposed localized, asymptotically flat configuration would normally require a regular center,

\[
M(0)=0,\quad \phi'(0)=0,\quad e^{\nu(0)}\in(0,\infty),\quad f(0)=1,
\]

and a finite-mass asymptotic vacuum.

There are two natural asymptotic amplitude candidates, and both expose a problem for \(\omega\ne0\):

1. **Approach the double-well vacuum \(\phi\to\pm v\).** The phase contribution to \(\rho\) tends to \(\frac12\beta\omega^2v^2e^{-2\nu_\infty}\), which is nonzero when \(\omega v\ne0\). It therefore does not describe a localized finite-mass perturbation of an asymptotically flat vacuum. The amplitude equation also cannot approach a constant nonzero \(v\): its asymptotic algebraic residual contains \(\beta\omega^2e^{-2\nu_\infty}v\ne0\), since \(V'(v)=0\).

2. **Approach \(\phi\to0\).** With the vacuum subtraction fixed at \(v\), \(V(0)=\lambda_\phi v^4/4>0\), so \(\phi=0\) does not share the same asymptotically flat vacuum. Even if one separately retunes the constant vacuum term to cancel the energy at \(\phi=0\), linearizing the amplitude equation in an asymptotically flat region with \(\nu\to0\), \(f\to1\), gives

\[
\phi''+\frac2r\phi'+k^2\phi\simeq0,\qquad
k^2=\frac{\beta\omega^2-m_\phi^2}{\alpha}>0.
\]

The leading radial modes are oscillatory, proportional to \(\sin(kr)/r\) and \(\cos(kr)/r\), not exponentially decaying localized modes. Moreover, \(\phi=0\) is not a minimum of the double-well potential.

Consequently, under the canonical V1 action and the stated double-well signs, the usual regular-center, finite-mass, asymptotically flat harmonic-phase soliton is obstructed by its asymptotics. This is a branch-specific obstruction, not a theorem excluding all stationary DFM–MKC solutions.

## 4. What is and is not established

**Derived here**
- The harmonic-phase ansatz gives stationary stress-energy while satisfying the phase equation.
- Its coupled spherical Einstein–amplitude equations are given above, with the vacuum offset handled consistently.
- For \(m_\phi^2<0,\lambda_\phi>0\), neither \(\phi\to\pm v\) nor the linearized \(\phi\to0\) branch provides the standard asymptotically flat, localized tail when \(\omega\ne0\).

**Not established**
- Existence or nonexistence in asymptotically de Sitter/anti-de Sitter geometry, with a horizon, with additional matter, or for time-dependent amplitudes.
- Stability, a new compact object, a curvature-energy bound, or a new observable.
- Any equivalence between this canonical V1 branch and the repository's separate generalized-Proca L4 completion.

**Stop rule:** do not numerically shoot the asymptotically flat double-well harmonic-phase branch under these assumptions. First specify a different asymptotic geometry or a different allowed potential regime, then derive its boundary conditions before numerical work.

## References

1. S. Liebling and C. Palenzuela, [Dynamical Boson Stars, Living Reviews in Relativity](https://doi.org/10.1007/S41114-017-0007-Y), for the standard harmonic ansatz and the distinction between time-dependent scalar fields and stationary stress-energy.
2. [Canonical DFM–MKC closed action functional V1](../../artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json).
3. [Canonical DFM–MKC field equations V1](../../artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json).

This is a mathematical reduction and conditional asymptotic obstruction only; it does not promote the model's empirical status.
