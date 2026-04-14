# Y6 Export Contract Lock

## Status
Conditional.

## Canonical Y6 Source Surfaces
- DES Y6 cosmology results and release surface
- NCSA Y6A2 release surface
- Official query/export surfaces serving DES Y6 public data products

## Contract Revision
The repository no longer requires that the two remaining DES Y6 objects be obtained only via fixed direct-download CSV URLs.
They may instead be supplied by a reproducible official export recipe from an official DES Y6 public access surface, provided the exported files are stored canonically at:

- public_data/des_y6/y6_3x2pt_summary.csv
- public_data/des_y6/y6_covariance.csv

## Acceptance Criteria
A DES Y6 replacement is admissible iff all of the following hold:
1. The source surface is official for DES Y6 public data access.
2. The export recipe is reproducible.
3. The resulting files are stored at the canonical repository paths.
4. The resulting files contain no SYNTHETIC_PLACEHOLDER marker.
5. The repository status remains Conditional until both canonical files are present as authentic public-data replacements.

## Remaining Open Objects
- public_data/des_y6/y6_3x2pt_summary.csv
- public_data/des_y6/y6_covariance.csv
