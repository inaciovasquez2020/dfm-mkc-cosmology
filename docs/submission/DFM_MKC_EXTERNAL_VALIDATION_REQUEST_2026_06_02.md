# DFM-MKC Cosmology — External Validation Request

## Request

Please independently validate the DFM-MKC cosmology repository as a reproducible conditional inference surface.

## Repository State To Validate

- post-closure external-validation packet present
- real-data readiness lock present
- paper-facing inference packet present
- no-overclaim boundary present
- targeted verifier passing

## Requested Checks

1. Clone the repository from `main`.
2. Reconstruct the documented environment.
3. Verify public-data artifact paths.
4. Run the declared verification scripts.
5. Run the declared comparison path where the local environment permits.
6. Report any missing local, package, data, or likelihood dependency.
7. Report whether the declared conditional inference surface is reproducible.

## Required Report Fields

- validator name or institution
- date
- commit hash
- operating system
- Python version
- package manager
- data artifacts checked
- commands run
- passing checks
- failing checks
- missing dependencies
- reproducibility conclusion
- interpretation boundary

## Boundary

A successful external validation report verifies reproducibility only.

It does not by itself establish a unique cosmological interpretation.
