# Exceptional-branch cubic obstruction: bounded certificate

**Status:** symbolic identity independently derived; repository CI has not yet executed this new test.

## Branch and source convention

Use the audited completed action
\[
\mathcal L=\sqrt{-g}\left[\left(\frac{F(\phi)}2+G_4(X_A)\right)R
-\frac{\xi}{2}D_4-\frac14F_{\mu\nu}F^{\mu\nu}+\cdots\right],
\qquad G_4=-\frac{\xi X_A}{2},\quad X_A=-\frac12A_\mu A^\mu.
\]
The exceptional locus is \(\xi=-1/2, M_2=b_0^2/4\), with \(\phi=0\) and vanishing mass/potential constants as in the source audit.

## Restricted static test

Restrict to
\[
ds^2=-dt^2+h(z)(dx^2+dy^2+dz^2),\quad
h=1-2\epsilon p(z),\quad
A_\mu=(b_0[1+\epsilon p(z)],0,0,0).
\]
On this subspace, \(R_{tt}=0\), \(D_4=0\),
\[
R=-\frac{2h''}{h^2}+\frac{3(h')^2}{2h^3},\qquad
F_{\mu\nu}F^{\mu\nu}=-\frac{2(A_0')^2}{h}.
\]
Expanding the restricted density through cubic order gives
\[
\mathcal L_3=\frac{b_0^2}{2}\left(6p^2p''+11p(p')^2\right).
\]
Modulo a periodic boundary term, this is equivalent to
\[
\mathcal L_3\simeq-\frac{b_0^2}{2}p(p')^2.
\]

For the leading candidate direction \(\delta_1p=f\), corresponding to \(\delta_1\psi=f,\delta_1u=b_0f\), take
\[
p=A\cos(qz),\qquad f=\cos(2qz),\qquad q>0.
\]
The exact integrated cubic variation is
\[
\boxed{\int_0^{2\pi/q}\delta_1\mathcal L_3\,dz
=-\frac{3\pi}{4}b_0^2A^2q\ne0.}
\]
This value is obtained by differentiating the cubic density with respect to \(p,p',p''\), then substituting the mode triad and integrating over a period. The accompanying executable symbolic test checks the expansion and integral.

## What this establishes—and what it does not

The chosen static mode with \(u=b_0p\), and \(\Phi=\beta=\chi=\sigma=0\), lies in the null sector of the displayed quadratic equations on this exceptional branch: the \(\Phi,\beta\) rows vanish because \(C=2M_2+b_0^2\xi=0\); the \(u,\psi\) rows are dependent; and the \(\chi\) row vanishes for the static profile.

On a periodic domain, a regular second-order correction contributes \(\delta_2S_2\) proportional to the quadratic equations of motion plus boundary terms. Thus the nonzero residual obstructs this particular leading null direction from extending as a regular nonlinear symmetry through cubic order, **provided the restricted action and perturbation parametrization match the intended full action**.

It does **not** prove that no other nonlinear symmetry exists, count physical degrees of freedom, establish hyperbolicity, or settle the full Einstein–Rosen/spiderweb framework. The action completion and the static restricted ansatz remain explicit scope conditions.
