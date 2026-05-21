# DFM-MKC Dynamical Core v1 Scaffold

Status: `SCAFFOLD_ONLY_DYNAMICAL_CORE_NOT_SUPPLIED`

This object records the weakest admissible next container for a DFM-MKC dynamical core.

It records repository evidence already present, including:

- `artifacts/repo_intake/dfm_mkc_theory_content_digest_2026_05_21.json`
- `src/cosmology/observables/distances.py`
- `theory/deformation_field.md`
- `theory/parameters.md`
- `numerics/background_equations.md`
- `config/dfm_mkc_parameter_freeze.json`
- `dfm_mkc/model.py`
- `src/models/dfm_mkc.py`
- `mkc_solver.py`

The observable distance layer supplies:

- `comoving_distance(model, z)`
- `luminosity_distance(model, z)`
- `angular_diameter_distance(model, z)`

It depends on:

- `model.H(z)`

Missing objects remain:

- `ActionFunctional_or_PrimitiveClosedFormFieldEquations`
- `MatterCouplingRule`
- `DarkSectorCouplingRule`
- `SourceTerms`
- `BoundaryConditions`
- `ExhaustiveParameterTable`
- `FrozenPredictionVector`
- `ACT_DES_HoldoutData`
- `ResidualEvaluationResult`
- `IndependentReplicationResult`

Does not prove:

- DFM-MKC
- Lambda-CDM failure
- ACT/DES holdout survival
- independent empirical validation
- dark-energy resolution
- dark-matter resolution
- Nobel-level physical discovery
- any Clay problem
