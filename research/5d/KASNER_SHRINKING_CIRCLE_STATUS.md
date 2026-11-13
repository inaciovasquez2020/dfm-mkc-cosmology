# Exact five-dimensional vacuum Kasner circle: shrinking compact radius

**STATUS (2026-11-13):** Classical exact vacuum construction **PROVED** by direct curvature and Einstein-frame algebra; independently reproduced in a bounded SymPy calculation; **LEAN_VERIFIED := NOT_RUN**, **5D NECESSITY := OPEN**, **NOVELTY := NONE**. This is a classic solution explicitly discussed by Chodos and Detweiler in 1980.

## Specified ansatz and complete power-law classification

On `t>0`, use 5D Einstein gravity with `Λ5=0` and no matter:

```text
ds5² = -dt² + t^(2p) (dx²+dy²+dz²) + t^(2q) dw²,
w ~ w + 2π,  p,q real.
```

The independent diagonal Ricci components are

```text
R_tt = -[3p(p-1)+q(q-1)]/t²,
R_ii = p(3p+q-1)t^(2p-2)  (for i=x,y,z),
R_ww = q(3p+q-1)t^(2q-2).
```

The completely static branch `p=q=0` is flat Minkowski times a static circle. For any **nonstatic** vacuum solution, at least one of `p,q` is nonzero, so `3p+q=1`; then `R_tt=0` is equivalent to `3p²+q²=1`. Eliminating `q` gives `6p(2p-1)=0`. Hence precisely two nonstatic branches:

- `(p,q)=(0,1)`: three static Jordan directions, expanding circle; local metric is flat Milne form (periodic identification requires separate global treatment).
- `(p,q)=(1/2,-1/2)`: three expanding Jordan directions, shrinking compact circle.

This **exhausts only the specified isotropic spatial, diagonal, homogeneous power-law vacuum ansatz**, not all time-dependent/warped 5D metrics.

## Explicit compactifying solution

```text
ds5²=-dt²+t(dx²+dy²+dz²)+t^(-1)dw².
```

Direct construction of the full 5D Levi–Civita connection and contraction confirms **all 25 Ricci tensor components vanish**. The nonzero curvature is not a coordinate artifact: the Kretschmann scalar is `R_ABCD R^ABCD=9/(2t⁴)`, diverging as `t→0+`. The circle radius is `b=t^(-1/2)`, which shrinks without settling at a positive constant.

With 4D Jordan metric `gJ=-dt²+t d\\vec x²`, define the 4D Einstein frame `gE=b gJ`, canonical scalar `phi=sqrt(3/2) log b`, and Einstein proper time `tau=(4/3)t^(3/4)` (choice of unit reference scale understood). Then

```text
aE=t^(1/4)=(3 tau/4)^(1/3)
HE=1/(3 tau)
phi_dot=-sqrt(2/3)/tau
3HE²=phi_dot²/2
HE_dot=-phi_dot²/2
phi_ddot+3HE phi_dot=0.
```

This is an exact four-dimensional *massless-scalar / stiff-fluid* cosmology with `aE∝tau^(1/3)`: expansion **decelerates**.

With a unit coordinate circle and the standard 5D zero-mode normalization, the first Einstein-frame KK mass is `m1,E=b^(-3/2)=t^(3/4)`. Consequently `m1,E/HE=4t^(3/2)→∞` at late time: the zero-mode truncation becomes parametrically better **relative to the Hubble curvature scale**. This is not stabilization, physical compactification selection, or a statement about all possible winding/string sectors; it does not establish a distinctive 5D observable.

For the other nonstatic branch `(0,1)`, `aE∝tau^(1/3)` too, but `m1,E/HE=2` is constant rather than diverging. The zero-exponent static flat branch has `H_E=0`, so no mass/Hubble ratio is claimed.

## Prior art and resulting research boundary

These exponents are explicitly given in Chodos and Detweiler, *Where has the fifth dimension gone?*, **Physical Review D 21**, 2167 (1980), DOI https://doi.org/10.1103/PhysRevD.21.2167. No novelty is asserted. Standard Kaluza–Klein Einstein-frame reduction gives the same massless scalar cosmology and demonstrates that 4D zero-mode observables can be duplicated by an ordinary 4D Einstein–scalar model. This is a useful verified comparison to the two prior examples:

- Positive-`Λ5` [expanding-circle solution #335](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/335) accelerates in 4D but its KK modes become **less** heavy relative to `H_E`.
- The `Λ5=0` compactifying Kasner circle here makes KK modes increasingly heavy relative to `H_E`, but the expansion **decelerates**.
- The [Einstein–winding fixed-radius AdS example #336](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/336) has a positive restricted radion mass but negative 4D curvature.
- The [EGB–winding dS product #337](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/337) is an exact background with a negative high-KK tensor principal coefficient in its classical model.
- The [static-circle NEC theorem #338](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/338) excludes a NEC-respecting unwarped static dS product in standard Einstein gravity.

The benchmark **does not close** the global 5D dynamics, radion stabilization, 4D event-first Chronos measure transfer, or a predictive difference from a matched 4D model.

Run at the exact revision with existing SymPy, avoiding optimized Python:

```bash
python3 -B research/5d/kasner_shrinking_circle_exact_audit.py
```

Source script independently verifies two nonstatic branches, 25-component Ricci zero, Einstein-frame Friedmann/Klein–Gordon equations, deceleration, Kretschmann value, the KK/Hubble ratios and a nonvacuum negative-control exponent. A timeout or missing SymPy is **INCOMPLETE**, never PASS. Local Mac branch and worktree not inspected.


## New: five-dimensional NEC power-law acceleration obstruction (2026-11-13)

**PROVED under stated hypotheses.** This is a narrow special-case consequence of classical higher-dimensional no-go results, **not a new general theorem**. Let the same diagonal homogeneous metric have arbitrary positive 3-space expansion exponent `p>0` and *shrinking* circle exponent `q<0`; allow an arbitrary source, cosmological constant and positive gravitational coupling, but require standard 5D Einstein equations and the five-dimensional null energy condition (NEC).

For the null vectors consisting of one unit timelike vector plus a unit 3-space or circle vector, direct Ricci contraction gives

```text
t² Ric5(V_circle,V_circle) = -3 p (p-q-1)
t² Ric5(V_space,V_space)  = 2p+q+pq-q².
```

The cosmological and metric-scalar terms vanish in null contractions of Einstein's equations. Therefore NEC forces `p(p-q-1)<=0`. Since `p>0`, this is `p<=1+q<1`; in particular `q>-1`. The four-dimensional Einstein proper time is `tau=t^(1+q/2)/(1+q/2)`; the reduced scale factor is `aE=t^(p+q/2)`. If the Einstein-frame universe is expanding, its power-law index is `n=(p+q/2)/(1+q/2)`. Because `q>-1`, its denominator is positive; `p<1` implies **n<1**, so acceleration is impossible. (If `n<=0`, it is not an expanding solution.) Thus there is no expanding, accelerating 4D Einstein-frame power-law with a shrinking circle and 5D NEC in this ansatz.

**Independent exact bounded adversarial check:** `research/5d/shrinking_circle_nec_power_law_audit.py` enumerates 512 rational pairs `p=i/8` (`1<=i<=32`), `q=j/8` (`-16<=j<=-1`), evaluates both NEC contractions, and checks none of the 16 NEC-admissible pairs accelerates. A deliberately accelerating `p=3/2, q=-1/4` negative control fails circle NEC; the exact vacuum Kasner pair `p=1/2,q=-1/2` saturates both conditions. These finite counts challenge the symbolic theorem but do not prove unrestricted metrics.

**Prior art:** Wesley, *Oxidised cosmic acceleration*, JCAP 01 (2009) 041, DOI https://doi.org/10.1088/1475-7516/2009/01/041, proves substantially broader no-go/e-fold bounds for dynamical extra dimensions under stated energy conditions. This elementary power-law consequence is not claimed novel. Other potential loopholes—non-power-law transients, warping, extra stresses violating NEC, and modified gravity—remain outside this theorem. This result rules out **one exact combination of desired features**; it does not imply that all 5D accelerating cosmologies are impossible, nor that a KK origin could be inferred from 4D event data.

**Verification:** run `python3 -B research/5d/shrinking_circle_nec_power_law_audit.py` and the existing exact Kasner script at the same exact HEAD; CI must report both green before promotion. No Lean theorem is claimed.
