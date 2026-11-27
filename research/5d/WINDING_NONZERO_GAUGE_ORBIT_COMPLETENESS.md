# Complete nonzero Fourier gauge-orbit coordinates

**Scope:** classical linearized off-shell gauge quotient around a fixed constant-radius product background, not a physical spectrum. **Result:** PROVED by explicit inverse gauge transformation. **Lean:** NOT_RUN. **Novelty:** not claimed.

## Hypotheses

Use the conventions of [PR #344](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/344): product metric g4 + b² dw², b>0 constant, background winding chi=q w, torsion-free Levi-Civita connection of g4, and one smooth Fourier perturbation level n != 0, k=i n. Work with complex Fourier coefficients (real fields pair n and -n). Let r=delta g_ww/(2b²), B_mu=delta g_mu w/b², h_mu nu=delta g_mu nu, theta=delta chi. Set D(v)_mu nu=nabla_mu v_nu+nabla_nu v_mu and Hess(r)_mu nu=nabla_mu nabla_nu r. Gauge parameters are a=xi^w and c_mu=xi_mu.

The linearized action of the additive gauge group is

    r' = r+k a
    theta' = theta+q a
    B' = B+d a+(k/b²)c
    h' = h+D(c).

No field equation, background stationarity or dynamical constraint is assumed for this kinematic statement.

## Theorem (complete and unique slice)

Define

    Z = theta-q r/k,
    H = h-(b²/k) D(B)+(2b²/k²) Hess(r).

Both are invariant: the change in Z cancels directly; the change in H is D(c)-(b²/k)(2 Hess(a)+(k/b²)D(c))+(2b²/k²)k Hess(a)=0. Here D(d a)=2 Hess(a) for the torsion-free connection.

Choose

    a = -r/k,
    c = -(b²/k)(B-d r/k).

Then r'=0 and B'=0. By the same formula h'=H and theta'=Z. If a gauge transformation preserves r=B=0, k a=0 forces a=0, then (k/b²)c=0 forces c=0. The slice is unique. Every smooth pair (H,Z) is realized by (h,theta,B,r)=(H,Z,0,0). Hence the gauge orbit set is in bijection with smooth symmetric tensors and scalars: two configurations are equivalent iff H and Z agree. For real perturbations the normalizing map commutes with Fourier conjugation because k(-n)=conjugate(k(n)), and b,q are real.

The linear gauge-fixing operator mapping (a,c) to (delta r,delta B) is block triangular with diagonal k and (k/b²)Id_4. It has the explicit inverse displayed above (with the sign reversed to prescribe rather than cancel variations). Its inverse requires no four-dimensional Green function. This does not evaluate a functional ghost determinant or authorize a gauge-fixed action off a stationary background.

There are 16 complex off-shell field components and five gauge functions per nonzero Fourier coefficient, leaving eleven off-shell components, not eleven physical polarizations. At n=0 the construction is singular and PR #344's distinct Stückelberg analysis applies.

## Validation and boundary

Run `python3 -B research/5d/winding_nonzero_gauge_orbit_exact.py` with standard-library Python. The finite rational jet audit tests invariance, normalization, orbit representatives and inverse parameter recovery; the universal proof is the algebra above. k is a nonzero formal rational parameter in tests, and the identities are rational identities valid also at k=i n. This is supporting finite evidence, not a substitute for proof.

Prior art: the metric-sector construction is standard KK Stückelberg reduction; see *The dimensional reduction of linearized spin-2 theories invariant under transverse diffeomorphisms*, https://doi.org/10.1140/epjc/s10052-021-09297-0 (arXiv:2010.12051). This note integrates the winding scalar into the orbit quotient using the repository conventions, without novelty claim.

**OPEN:** derive the coupled quadratic Hessian on a specified stationary background, eliminate dynamical constraints, compute kinetic signs, eigenvalues and renormalized full determinant including gauge fixing and ghosts. Neither a stable physical 5D vacuum nor a Chronos observable transfer follows from gauge-orbit completeness.
