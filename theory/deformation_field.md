## Covariant DFM–MKC FLRW Reduction

Use the spatially flat FLRW convention

\[
ds^2=-dt^2+a(t)^2d\mathbf{x}^2,
\qquad
H=\frac{\dot a}{a},
\]

with homogeneous fields

\[
\phi=\phi(t),
\qquad
\theta=\theta(t).
\]

For

\[
\mathcal L_{\mathrm{DFM\text{-}MKC}
}
=
-\frac{\alpha}{2}(\nabla\phi)^2
-\frac{\beta}{2}\phi^2(\nabla\theta)^2
-U(\phi),
\]

the homogeneous dark-sector density and pressure are

\[
\rho_{\mathrm{DFM\text{-}MKC}
}
=
\frac{\alpha}{2}\dot\phi^2
+
\frac{\beta}{2}\phi^2\dot\theta^2
+
U(\phi),
\]

\[
p_{\mathrm{DFM\text{-}MKC}
}
=
\frac{\alpha}{2}\dot\phi^2
+
\frac{\beta}{2}\phi^2\dot\theta^2
-
U(\phi).
\]

The spatially flat background equations are

\[
H^2
=
\frac{\Lambda}{3}
+
\frac{8\pi G}{3}
\left(
\rho_{\mathrm{vis}}
+
\rho_{\mathrm{DFM\text{-}MKC}
}
\right),
\]

\[
\dot H
=
-4\pi G
\left(
\rho_{\mathrm{vis}}
+
p_{\mathrm{vis}}
+
\alpha\dot\phi^2
+
\beta\phi^2\dot\theta^2
\right),
\]

\[
\alpha
\left(
\ddot\phi+3H\dot\phi
\right)
-
\beta\phi\dot\theta^2
+
U'(\phi)
=
0,
\]

and

\[
\frac{d}{dt}
\left(
a^3\beta\phi^2\dot\theta
\right)
=
0.
\]

Hence

\[
Q_\theta
=
a^3\beta\phi^2\dot\theta
\]

is conserved. Wherever \(\beta\phi\neq0\),

\[
\dot\theta
=
\frac{Q_\theta}{a^3\beta\phi^2},
\]

so the phase can be eliminated:

\[
\rho_{\mathrm{DFM\text{-}MKC}
}
=
\frac{\alpha}{2}\dot\phi^2
+
\frac{Q_\theta^2}{2\beta a^6\phi^2}
+
U(\phi),
\]

\[
\alpha
\left(
\ddot\phi+3H\dot\phi
\right)
-
\frac{Q_\theta^2}{\beta a^6\phi^3}
+
U'(\phi)
=
0.
\]

## Implementation boundary

`solver/background_solver.py` is a legacy two-variable toy system.

Its variables `Phi`, `alpha`, and `beta` are not identified with the
action variables \(\phi\), \(\alpha\), and \(\beta\). In particular, its
initial condition gives `Phi` the scaling of \(H^2\), and its right-hand
side is independent of `beta`.

Therefore that solver must not be described as an implementation of the
covariant DFM–MKC FLRW equations until it is replaced by an evolution
system for

\[
(a,H,\phi,\dot\phi,\theta,\dot\theta)
\]

or by the charge-reduced system

\[
(a,H,\phi,\dot\phi,Q_\theta).
\]

## Conditional dust-plus-radiation charge-reduced IVP

This section adds a background-fluid assumption that is not derived from
the metric-only matter-coupling rule.

Assume the visible background contains noninteracting pressureless matter
and radiation:

\[
\rho_{\mathrm{vis}}=\rho_m+\rho_r,
\qquad
p_{\mathrm{vis}}=\frac{\rho_r}{3},
\]

\[
\dot\rho_m=-3H\rho_m,
\qquad
\dot\rho_r=-4H\rho_r.
\]

Use

\[
v=\dot\phi
\]

and

\[
U(\phi)
=
\rho_\star
+
\frac12m_\phi^2\phi^2
+
\frac14\lambda_\phi\phi^4,
\]

so that

\[
U'(\phi)
=
m_\phi^2\phi
+
\lambda_\phi\phi^3.
\]

For fixed conserved phase charge \(Q_\theta\), define

\[
\rho_{\mathrm{DFM\text{-}MKC}
}
=
\frac{\alpha}{2}v^2
+
\frac{Q_\theta^2}{2\beta a^6\phi^2}
+
U(\phi).
\]

The conditional state vector is

\[
x=(a,\phi,v,\rho_m,\rho_r),
\]

with evolution equations

\[
\dot a=aH,
\]

\[
\dot\phi=v,
\]

\[
\dot v
=
-3Hv
+
\frac{Q_\theta^2}{\alpha\beta a^6\phi^3}
-
\frac{U'(\phi)}{\alpha},
\]

\[
\dot\rho_m=-3H\rho_m,
\qquad
\dot\rho_r=-4H\rho_r.
\]

Choose the expanding Friedmann branch

\[
H
=
+\sqrt{
\frac{\Lambda}{3}
+
\frac{8\pi G}{3}
\left(
\rho_m+\rho_r
+
\frac{\alpha}{2}v^2
+
\frac{Q_\theta^2}{2\beta a^6\phi^2}
+
U(\phi)
\right)
}.
\]

The admissible domain is

\[
a>0,
\qquad
\alpha>0,
\qquad
\beta>0,
\qquad
\phi\neq0,
\]

together with nonnegative matter and radiation densities and a
nonnegative Friedmann radicand.

Initial data

\[
(a_0,\phi_0,v_0,\rho_{m0},\rho_{r0})
\]

must satisfy that domain, and \(H_0\) is determined by the positive
Friedmann branch rather than supplied independently.

For this conditional system,

\[
\rho_{\mathrm{tot}}
=
\rho_m+\rho_r+\rho_{\mathrm{DFM\text{-}MKC},
}
\]

\[
p_{\mathrm{tot}}
=
\frac{\rho_r}{3}
+
\frac{\alpha}{2}v^2
+
\frac{Q_\theta^2}{2\beta a^6\phi^2}
-
U(\phi),
\]

and the evolution equations imply

\[
\dot\rho_{\mathrm{tot}}
+
3H
\left(
\rho_{\mathrm{tot}}+p_{\mathrm{tot}}
\right)
=
0.
\]

Consequently, differentiating the Friedmann constraint gives

\[
\dot H
=
-4\pi G
\left(
\rho_{\mathrm{tot}}+p_{\mathrm{tot}}
\right).
\]

### Conditional boundary

The dust-plus-radiation decomposition, separate component conservation,
expanding Friedmann branch, and initial-data domain are additional
background-model assumptions. They are not derived from
\(L_{\mathrm{vis}}\) or from the existing metric-only coupling artifact.
