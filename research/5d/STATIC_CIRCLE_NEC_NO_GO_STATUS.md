# Null energy obstruction for static unwarped dS4 × S1 in 5D Einstein gravity

**STATUS:** PROVED under explicit assumptions; finite rational sanity tests COMPUTATION_PASS in a Python stdlib script. **NOVELTY:** NOT CLAIMED. **LEAN_VERIFIED:** NOT_RUN. **PHYSICAL 5D:** OPEN.

## Theorem (special-case NEC no-go)

Let a 5-dimensional Lorentzian manifold have exact product metric

```text
ds5² = g4(x) + b² dw²,  b>0 constant,  w mod 2π,
Ric4 = 3k*g4.
```

Assume the five-dimensional Einstein equations

```text
Ric5_AB - (R5/2)g5_AB + Lambda5*g5_AB = kappa5²*T_AB,
kappa5² > 0.
```

If the stress tensor satisfies the 5D null energy condition `T_AB V^A V^B >= 0` for every 5D null vector, then **k<=0**. In particular, *no unwarped static-radius de Sitter × circle product exists with NEC-satisfying 5D matter in standard Einstein gravity*.

**Proof:** At each point choose a unit 4D future-timelike vector `u` and the circle unit vector `e_w = b^{-1}∂_w`. Their sum `V=u+e_w` is 5D null. Product geometry gives `Ric5(u,u)=-3k` and `Ric5(e_w,e_w)=0`, with mixed components zero. Contracting the 5D Einstein equation with `V`, both the scalar-curvature and cosmological terms drop out because `g5(V,V)=0`. Therefore

```text
kappa5²*T(V,V) = Ric5(V,V) = -3k.
```

The NEC implies `-3k>=0`, hence `k<=0`. This does not require a particular matter species, nor even a separate scalar winding ansatz. The general statement is local and can fail if **any specified assumption** changes: varying/warped circle, different 4D curvature, higher-curvature gravity, sources violating NEC, or modified field equations.

A canonical scalar with winding around the compact circle has `T(V,V)=q²/(2b²)>0`; consequently `k=-kappa5² q²/(6b²)<0` for nonzero winding. This explains why the exactly verified Einstein–axion circle in [Cosmology PR #336](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/336) is AdS rather than dS without relying on its full potential calculation.

A deliberately **unphysical**, wrong-sign kinetic scalar provides an adversarial check. With `kappa5²=1`, `b²=1`, `q²=2`, and a ghost scalar one gets `k=1/3` and `Lambda5=3/2` satisfying the product background equations **while violating NEC**. Therefore this is specifically an NEC obstruction and must not be presented as an unconditional no-go across arbitrary sources.

## Connection to the EGB branch

[Cosmology PR #337](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/337) adds a Gauss–Bonnet term and explicitly leaves the Einstein equations used above. Its de Sitter product has a negative high-circle-momentum tensor coefficient in the unrestricted classical model. The NEC theorem does **not** establish that result; it provides a distinct standard-Einstein boundary and identifies where any alternative construction must change an assumption.

## Existing literature / novelty

This is a minimal special case of well-known constraints on de Sitter compactifications. See Das, Haque and Underwood, *Constraints and horizons for de Sitter with extra dimensions*, **Phys. Rev. D 100**, 046013 (2019), DOI https://doi.org/10.1103/PhysRevD.100.046013, which treats static extra dimensions, warping and NEC constraints; and Faruk, *Deriving the Gibbons-Maldacena-Nunez no-go theorem from the Raychaudhuri equation*, **Phys. Rev. D 109**, L061902 (2024), DOI https://doi.org/10.1103/PhysRevD.109.L061902. Related work includes Russo and Townsend, *Time-dependent compactification to de Sitter space: a no-go theorem*, JHEP 06 (2019) 097. These are stronger/differently conditioned results; this note does not assert a new no-go theorem.

## Verification and status

```bash
python3 -B research/5d/static_circle_nec_no_go_exact.py
```

The Python 3 stdlib certificate checks the null contraction for rational positive/zero/negative curvature, several positive circle radii, canonical winding stress, and a wrong-sign counterexample. Its test suite is corroboration of the short tensor proof, **not** proof of unrestricted physical compactification scenarios. The workflow should run at exact PR HEAD. Do not claim PASS if assertions are disabled, a test fails or a timeout occurs. Source branch preserved; no Mac local working tree was inspected.

**Next mathematically decisive construction:** derive an explicit 5D action and stress tensor which has positive dS curvature, healthy kinetic signatures, an acceptable radion/KK spectrum, and a distinct 4D prediction. **Current exact-blocking condition:** a strictly static, unwarped circle in Einstein gravity with 5D NEC matter cannot work. Do not force Poincaré, biological or finite-model-theory repositories into this requirement.
