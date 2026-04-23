# DES Y6 Export Recipe

Status: Closed

## Official source surfaces
- https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/
- https://dev.des.ncsa.illinois.edu/

## Canonical repository targets
- public_data/des_y6/y6_3x2pt_summary.csv
- public_data/des_y6/y6_covariance.csv

## Reproducible export procedure
1. Verify that both official public source surfaces above are live.
2. Obtain the DES Year 6 cosmology export corresponding to the committed repository pair:
   - y6_3x2pt_summary.csv
   - y6_covariance.csv
3. Install those two files verbatim at the canonical repository targets listed above.
4. Regenerate `artifacts/data/des_y6_fingerprints.json` from the installed files.
5. Require `tests/test_des_y6_provenance_lock.py` to pass.
6. Require full repository tests and certificate verification to pass.
7. Retag `real-data-freeze-2026-04-23` at the merged `main` HEAD.
