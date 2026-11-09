# Diamond–graphite scalar charge: microscopic EFT derivation and a conditional fifth-force constraint

Date: 2026-11-08. Scope: a **new conditional low-energy EFT**, not the canonical DFM-MKC V1 action. No user repository was edited. This note's Python audit is `research/conditional_eft/diamond_graphite_20261108/diamond_graphite_charge_constrain.py`; its JSON receipt is located alongside the script in the same repository directory.

## 0. Canonical-action boundary

The visible sector in canonical DFM-MKC V1 is `L_vis(psi,g)` with **no direct phi or theta coupling** (repo: `inaciovasquez2020/dfm-mkc-cosmology`, remote `f14063bff4f11ee94ed3780c7765937da828cda3`, `docs/status/DFM_MKC_MATTER_COUPLING_RULE_V1_2026_05_27.md`). Holding the metric fixed, scalar derivative of visible mass is zero. The canonical action cannot produce an independent diamond-versus-graphite fifth force. Ordinary gravity from all stress-energy is unaffected by this statement.

## 1. Model and operator basis

Take a weak, canonically normalized scalar `chi`, define `varphi=(chi-chi0)/M_P`, `M_P^{-2}=8*pi*G` and `mu_chi >=0`. Specify the **low-energy** parameterized matter theory `L_SM(psi,g; alpha_EM(varphi),Lambda_QCD(varphi), mhat(varphi),deltam(varphi),me(varphi))`. Couplings `d_i=(partial/partial varphi) ln p_i |_{varphi=0}` are defined at specified renormalization scales. This is equivalent to linear couplings of `varphi` to gauge kinetic, gluon trace-anomaly, and renormalized fermion mass operators, with mixing under RG flow. It is not a free-standing claim of UV completeness, and is not an extension automatically supplied by DFM-MKC V1.

This standard five-component basis is `(d_g,d_mhat,d_deltam,d_me,d_alpha)`. `d_C=(d/dvarphi) ln m_C` is **not** a sixth independent constant; it is the corresponding carbon atomic mass response inferred from the same operator basis. At leading hadronic order, `d_C=d_g + (d_mhat-d_g) Q_mhat^C + (d_deltam-d_g) Q_deltam^C + (d_me-d_g) Q_me^C + d_alpha Q_alpha^C`, with hadronic response factors `Q_i` from the Damour–Donoghue formalism and convention-dependent renormalization matching. Hence ordinary atomic/nuclear material responses are not carbon-exclusive.

## 2. Exact first-derivative identity (T=0)

For equal-isotope bulk allotropes at fixed external pressure `p_ext=0`, with per-atom mass-energy `E_X=m_C+eps_X`, `q_X=(m_C'+eps_X')/(m_C+eps_X)` (`'` denotes partial_varphi), the exact difference is

`Delta q = [m_C*(eps_D'-eps_G') - m_C'*(eps_D-eps_G) + eps_G*eps_D'-eps_D*eps_G'] / [(m_C+eps_D)*(m_C+eps_G)]`.

Proof: combine the fractions. At finite temperature, coupling to an environment requires specifying the thermodynamic ensemble and energy exchange; the zero-temperature result is the cleanest statement. Feynman–Hellmann makes `eps'_X` an expectation value of the specified microscopic operator derivatives, not of the label sp2/sp3.

## 3. Controlled Coulomb + harmonic-phonon approximation

For fixed carbon isotope composition, ignoring small relativistic corrections, electron recoil, anharmonic terms, and additional short-distance operators, Coulomb similarity yields electronic cohesive energies proportional to `m_e alpha_EM^2`. The equilibrium lattice length scales like `(m_e alpha_EM)^(-1)` and the phonon force-constant scales as `m_e^3 alpha_EM^4`, so zero-point vibrational energies scale as `m_e^(3/2) alpha_EM^2 m_C^(-1/2)`.

Define `Delta E0=(eps_D-eps_G)`, `Delta Ezp=(eps_zp,D-eps_zp,G)`, and `Delta Eel=Delta E0-Delta Ezp`. Then

`Delta q ~= ((d_me+2 d_alpha-d_C)*Delta Eel + (1.5 d_me+2 d_alpha-1.5 d_C)*Delta Ezp)/(m_C)`

`       = ((d_me-d_C)*(Delta E0+Delta Ezp/2) + 2*d_alpha*Delta E0)/m_C`.

All quantities above are mass energies (c=1); in SI use `m_C c^2` in the denominator. Controlled error is of order `|eps|^2/m_C^2` plus **unquantified** relativistic, finite-T, electron-recoil, higher-operator, and material-quality errors. It is not valid to infer a full uncertainty from thermodynamic energy ranges alone.

Special universal-rescaling counterexample: when `d_me=d_C`, `d_alpha=0`, all electronic and zero-point energies scale with `d_C`, so `q_D=q_G=d_C` exactly in this scaling model even though `Delta E0 !=0`.

## 4. Numerical sensitivity coefficients (conditional)

Popov, Görne, Tchougréeff, Dronskowski, PCCP (2019) give estimates for `Delta E0` in `[1.39,1.55] kJ/mol`, `Delta Ezp` in `[0.77,1.15] kJ/mol`, for `E_D-E_G` at zero temperature; these are not statistical intervals and their electronic-energy separation is theory-dependent. Earlier calculations disagree about even the sign of electronic-only energy. Ideal ^12C molar mass `0.012 kg/mol`, `c=299792458 m/s`, yields `m_C c^2=1.078506214484e12 kJ/mol`. Within this approximation,

`Delta q ~= A_m*(d_me-d_C)+ A_alpha*d_alpha`, where

`A_m in [1.645794875e-12,1.970317808e-12]`

`A_alpha in [2.577639297e-12,2.874345978e-12]`.

Signs of `d_i`, and cancellations, remain unknown. `Delta q` is not an observed nonzero value. These sensitivity coefficients are not bounds valid for arbitrary additional operators or condensed-matter corrections.

## 5. Fifth-force normalization and experimental constraint

For scalar charge `q_X=partial ln M_X/partial (chi/M_P)` and scalar mass `mu`, weak-field potential is `V=-G M_S M_X/r [1+2 q_S q_X e^(-mu r)]` for point masses, under unscreened weak coupling. Leading Eötvös signal for test bodies D, G in source S is `eta_DG ~= 2 q_S Delta q (1+mu r)e^(-mu r)` (up to a very small common-denominator correction); real extended source form factors matter for finite range.

MICROSCOPE final Ti–Pt measurement: `eta=(-1.5 +/-2.3_stat +/-1.5_syst)*1e-15` (1 sigma). A deliberately conservative 2 sigma absolute envelope assuming independent Gaussian stat and syst components is `eta_env= (1.5 + 2*sqrt(2.3^2+1.5^2))*1e-15 = 6.991812e-15`. It is *not* an official likelihood interval.

The direct constraint is on `|q_Earth (q_Ti-q_Pt)|`, multiplied by the Yukawa factor. Without source charge, range and EFT couplings specified, no numerical bound on `|Delta q_DG|` follows from MICROSCOPE. In particular, multi-operator cancellations can make `q_Ti-q_Pt=0` without setting `Delta q_DG=0`.

### Illustrative one-operator result

Set `d_g=d_mhat=d_deltam=d_me=0`, only `d_alpha` nonzero **at a fixed low-energy scale**; the known electromagnetic self-energy contribution to `d_C` is small but nonzero. Assume `mu r <<1`, no screening, and use simplified Damour/Donoghue dilaton charge factors from Cyncynates & Simon (2025) Table 1 (Pt–Ti ordering, both charge differences negative): `Q'_e(Earth)=1.90e-3` (their illustrative Earth composition), `|Q'_e(Pt-Ti)|=1.94e-3` (Ti/Pt alloys). The charge-prime factors ignore small element-dependent offsets and RG mixing: this is an illustrative, order-of-magnitude bound, **not a global experimental analysis**.

Then `eta_TiPt ~=2*(1.90e-3)*(1.94e-3)*d_alpha^2`, so `|d_alpha| <= 3.08e-5` under these restrictive assumptions. The material coefficient gives `|Delta q_DG| <= approximately 8.85e-17`, and corresponding `|eta_DG| <= approximately 1.04e-23` toward the same Earth model. The small `Q_alpha^C*d_alpha` correction reduces the value slightly, so the estimate is conservative within this approximate model. **Do not interpret this as a model-independent 95% exclusion.** If the scalar range is short, screening occurs, or couplings cancel, this bound does not apply.

### Explicit cancellation counterexample

With two nonzero low-energy couplings `d_me` and `d_alpha`, the MICROSCOPE test combination can be cancelled, using the same published approximate charge factors: `DeltaQme(Pt-Ti)=-3.13e-5`, `DeltaQalpha(Pt-Ti)=-1.94e-3`. These signs are taken together from the published Pt–Ti row: electron-mass charge difference −3.13×10⁻⁵ and electromagnetic charge difference −1.94×10⁻³. Reversing just one sign would not follow that convention and would invalidate the cancellation. Setting `d_me/d_alpha=-61.98083067` gives `Delta q_TiPt=0`. Yet `A_m*(d_me-d_C)+A_alpha*d_alpha` is generically **nonzero**, for example about `-1e-10*d_alpha` neglecting the small atomic `d_C` response. Scaling both couplings by any sufficiently small nonzero factor keeps the cancellation and EFT perturbativity. Therefore MICROSCOPE **alone cannot constrain an unrestricted operator-basis structural charge**. Other composition pairs, clocks, source geometries, ranges, and a joint likelihood are needed.

## 6. Verification and status

The accompanying standard-library Python script checks the exact common-denominator identity on 9,375 rational tuples, universal-rescaling cancellation on 375 tuples, numeric coefficient intervals, conservative illustrative MICROSCOPE bound, and a nontrivial Ti–Pt null-direction example: 9,750 exact rational-grid equality assertions and 3 additional Decimal assertions (9,753 assertions total); the 3 derived bound quantities are calculations, not independently asserted checks. No ab-initio electronic structure or phonon spectra were computed. The canonical V1 action was not modified.

`EXACT_IDENTITY := PROVED (cross-multiplication)`;
`FINITE_AUDIT := COMPUTATION_PASS`;
`MATERIAL_SENSITIVITY := CONDITIONAL`;
`ONE_OPERATOR_LONG_RANGE_BOUND := CONDITIONAL`;
`FULL_FIVE_OPERATOR_DELTA_Q_BOUND := OPEN`;
`CARBON_SPECIFIC_FIFTH_FORCE := NOT_ESTABLISHED`;
`USER_REPO_CHANGES := NOTE_AND_RECEIPT_UPDATED_IN_PR_334`.

## Primary sources

- Damour & Donoghue, *Equivalence principle violations and couplings of a light dilaton*, Phys. Rev. D 82, 084033 (2010), https://doi.org/10.1103/PhysRevD.82.084033 .
- Popov et al., *Relative stability of diamond and graphite as seen through bonds and hybridizations*, Phys. Chem. Chem. Phys. 21, 10961–10969 (2019), https://doi.org/10.1039/C8CP07592A .
- Touboul et al., *MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle*, Phys. Rev. Lett. 129, 121102 (2022), https://doi.org/10.1103/PhysRevLett.129.121102 .
- Cyncynates & Simon, *Minimal targets for dilaton direct detection*, Phys. Rev. D 112, 055002 (2025), https://doi.org/10.1103/8mc9-6cmr . (Table I values; simplified charge-prime convention.)
