# External Gravity–Magnetism Evidence Record — 2026-10-29

Status: `OBSERVATIONAL_INPUTS_RECORDED_MODEL_LINK_UNDERIVED`

## Scope

This record preserves two independent empirical sources and audits whether the Saleh Theory article supplies a derivation that can be constrained by MICROSCOPE. It is an evidence ledger, not a validation of a new gravity theory.

## A. NIST torsion-balance determination of G

**Final journal source**

- Schlamminger et al., “Redetermination of the gravitational constant with the BIPM torsion balance at NIST,” *Metrologia* 63, 025012 (published 2026-04-16).
- DOI: https://doi.org/10.1088/1681-7575/ae570f
- Final journal result: `G = (6.67387 ± 0.00038) × 10^-11 m^3 kg^-1 s^-2`
- Relative standard uncertainty: `5.7 × 10^-5`.

**Metadata discrepancy**

The NIST publication landing-page abstract has also displayed `(6.67366 ± 0.00020) × 10^-11 m^3 kg^-1 s^-2`, which conflicts with the final journal article's abstract and conclusion. The difference between central values is `2.1 × 10^-15 m^3 kg^-1 s^-2`. The final journal article is the reporting authority for this record. The cause of the inconsistent landing-page abstract is not established.

NIST landing page: https://www.nist.gov/publications/redetermination-gravitational-constant-bipm-torsion-balance-nist

Interpretation boundary: this is a torsion-balance determination and replication/reproducibility result. It is not evidence of temporal or spatial variation of G, nor evidence that gravity is electromagnetic.

Do not overwrite the repository's CODATA constant input with this measurement. The CODATA reference and this specific experimental determination are different evidence objects.

## B. BlackTHUNDER / J0148-4214

**Primary source**

“BlackTHUNDER: Evidence of three massive black holes in a z ∼ 5 galaxy,” *Astronomy & Astrophysics* 712, A80 (2026).

- DOI: https://doi.org/10.1051/0004-6361/202557419
- Instrument/data: JWST/NIRSpec integral-field spectroscopy.
- Reported redshift: `z = 5.0167`.
- Broad Hα FWHM range: `430–2920 km/s`.
- Two central broad-line regions: projected separation `190 ± 40 pc`.
- Third broad-line region: projected offset about `1.7 kpc`.
- Single-epoch virial black-hole mass estimates:
  - Primary: `log10(M/M_solar) = 7.9 ± 0.4`.
  - Secondary: `log10(M/M_solar) = 5.8 ± 0.5`.
  - Third/off-nuclear: `log10(M/M_solar) = 6.3 ± 0.5`.

**Limitations to retain with any reuse**

1. Three accreting black holes is the authors' favored interpretation of spatially distinct broad Hα emission, not direct imaging of three event horizons.
2. The paper discusses alternatives including supernovae, shocks, winds, and massive stars; the favored interpretation remains an inference from spectroscopy and modeling.
3. Masses use single-epoch virial scaling relations; systematic uncertainty may exceed the formal quoted fitting uncertainty.
4. Separations are projected, not full three-dimensional distances. The central separation is inferred from channel maps/centroid analysis, and the paper notes possible underestimation of its uncertainty by roughly 10–20 pc in mock tests.
5. Merger times and gravitational-wave detectability are model-dependent projections, not observations.
6. A single candidate system does not establish the population frequency of black-hole triplets.

## C. Saleh Theory gravity–magnetism article: formalization boundary

Source: https://saleh-theory.com/Article/new-discoveries-regarding-gravity-and-magnetism-in-the-universe-2026

The article describes gravitational and magnetic fluxes as chain-like, interwoven photons and proposes that their density/configuration structures space and guides matter. The article does not provide a quantitative constitutive law connecting the proposed photon chains to a measurable magnetic field, magnetic energy, gravitational acceleration, or equivalence-principle violation.

Therefore a derivation of magnetic energy from the proposed mechanism is currently unavailable.

### Standard electromagnetic definition (not a derivation of Saleh Theory)

For a magnetic field in vacuum, define the field energy in a region V as

`U_B = ∫_V B²/(2 μ_0) dV`

where `B` is the magnetic flux density and `μ_0` is the vacuum permeability. This is standard electromagnetic field energy. It does not establish that the article's photon chains generate that energy or that this energy couples anomalously to gravity.

A microscopic photon model would need, at minimum, a defined photon/field state, an energy-density relation, a mapping to the classical field `B`, and a coupling law respecting energy-momentum conservation. These inputs are absent from the cited article.

## D. Conditional phenomenological test, not source-derived

As a deliberately separate test ansatz, define

`f_B = U_B/(m c²)`

and hypothesize

`a = g (1 + α f_B)`.

For two test bodies, at first order in small `α f_B`,

`η_AB = 2(a_A-a_B)/(a_A+a_B) ≈ α(f_{B,A}-f_{B,B})`.

This ansatz is falsifiable but is not derived from the Saleh article. The article does not determine `α`, the relevant magnetic-energy definition, or whether internal, externally applied, or proposed photon-chain energy is meant.

## E. MICROSCOPE constraint and why no numerical α bound is recorded

Primary source: Touboul et al., “MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle,” *Physical Review Letters* 129, 121102 (2022), DOI https://doi.org/10.1103/PhysRevLett.129.121102

For titanium/platinum-alloy test masses, the reported Eötvös ratio is

`η(Ti,Pt) = [-1.5 ± 2.3 (stat) ± 1.5 (syst)] × 10^-15`

with quoted uncertainties at 1σ. MICROSCOPE compared collocated test masses of different compositions in free fall around Earth using differential electrostatic accelerometers.

This is a stringent weak-equivalence-principle constraint. It is not, by itself, a direct measurement of a magnetic-energy coupling. The published result does not supply the model-specific values of `f_{B,Ti}` and `f_{B,Pt}`, nor establish that the proposed photon-chain coupling acts on the masses in the assumed form.

Consequently, the only conditional relation available under the ansatz is

`η(Ti,Pt) ≈ α (f_{B,Ti} - f_{B,Pt})`.

No numerical bound on `α` is asserted. A bound requires a derived coupling law, a defensible calculation of the relevant magnetic-energy fractions for the actual test masses, and confirmation that the experimental observable constrains that coupling rather than another composition-dependent effect.

## Status ledger

- `NIST_FINAL_G_VALUE := RECORDED_FROM_FINAL_JOURNAL`
- `NIST_LANDING_PAGE_DISCREPANCY := RECORDED_CAUSE_UNRESOLVED`
- `BLACKTHUNDER_PRIMARY_MEASUREMENTS := RECORDED_WITH_LIMITATIONS`
- `SALEH_PHOTON_TO_FIELD_ENERGY_DERIVATION := MISSING`
- `PHENOMENOLOGICAL_ALPHA_ANSATZ := CONDITIONAL_NOT_SOURCE_DERIVED`
- `MICROSCOPE_APPLICABILITY_TO_MAGNETIC_COUPLING := NOT_ESTABLISHED`
- `NUMERICAL_ALPHA_BOUND := NOT_COMPUTED`

## Boundaries

This record does not establish a new gravitational theory, a photon-chain mechanism, variation of G, a violation of general relativity, a violation of the equivalence principle, or an empirical validation of Saleh Theory. No numerical coupling limit is admissible until the missing model-to-observable map and test-body energy fractions are supplied.
