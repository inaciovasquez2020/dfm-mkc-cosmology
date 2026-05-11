from pathlib import Path

p = Path("docs/status/DES_Y6_DOWNLOADED_SOURCE_CLASSIFICATION_2026_05_11.md")
s = p.read_text()

required = [
    "MACHINE_READABLE_OBJECTS_FOUND / AUTHENTIC_DES_Y6_3X2PT_RELEASE_VECTOR_NOT_IDENTIFIED",
    "repos/2pt_pipeline/pipeline/3x2pt_test.fits",
    "repos/2pt_pipeline/pipeline/cosm4blinding_FORTESTING.npz",
    "repos/y6kp-ggl-measurements/plots/ggl_terms/sim_y6.fits",
    "Test/example artifact, not an authentic DES Y6 release data vector.",
    "Simulation/plot-support artifact, not an authenticated DES Y6 public release likelihood/data-vector capture.",
    "No DES Y6 public release 3x2pt likelihood/data-vector ingestion claim.",
    "No DES Y6 BAO likelihood ingestion claim.",
    "No DFM-MKC superiority claim.",
    "No S8-tension resolution claim.",
    "No final cosmological truth claim.",
    "No theorem-level URF cosmology closure claim.",
]

for token in required:
    assert token in s, token

forbidden_positive_claims = [
    "DFM-MKC is superior",
    "S8 tension is resolved",
    "Final cosmological truth is established.",
    "URF cosmology closure is proved.",
    "DES Y6 likelihood ingested.",
    "Authentic DES Y6 release data vector captured.",
]

for token in forbidden_positive_claims:
    assert token not in s, token

print("DES Y6 downloaded source classification verified.")
