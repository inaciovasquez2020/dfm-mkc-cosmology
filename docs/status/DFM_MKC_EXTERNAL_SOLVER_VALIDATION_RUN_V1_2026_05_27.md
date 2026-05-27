DFM-MKC External Solver Validation Run V1 — 2026-05-27
Status: EXTERNAL_SOLVER_VALIDATION_RUN_GATE_SUPPLIED_NO_EXTERNAL_EXECUTION
This supplies DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1 as an importable validation-run gate surface.
Code file:
src/dfm_mkc_solver/external_solver_validation_run_v1.py
Entrypoints:
validate_external_solver_binding
validate_external_solver_run_record
run_external_solver_validation_gate
Boundary:
Does not prove DFM-MKC trusted external solver execution.
Does not prove DFM-MKC numerical prediction vector.
Does not prove DFM-MKC data comparison run.
Does not prove DFM-MKC likelihood improvement.
Does not prove DFM-MKC empirical validation.
Does not prove Lambda-CDM failure.
Does not prove dark matter replacement.
Does not prove dark matter is liquid.
Does not prove dark matter is solid.
Does not prove dark matter is a phase.
Does not prove CMB fit.
Does not prove ACT fit.
Does not prove Planck fit.
Does not prove DESI fit.
Does not prove BAO fit.
Does not prove weak lensing fit.
Does not prove matter power spectrum fit.
Does not prove gravity closure.
Does not prove Chronos-RR.
Does not prove unrestricted H4.1/FGL.
Does not prove P vs NP.
Does not prove any Clay problem.
Next admissible step: supply DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1 only after a real external solver execution is run, validated, and hash-locked.
