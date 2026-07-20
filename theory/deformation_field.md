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
