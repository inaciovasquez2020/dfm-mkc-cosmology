#!/usr/bin/env python3
from pathlib import Path

p = Path("docs/status/DES_Y6_BAO_SOURCE_PROBE_2026_05_11.md")
s = p.read_text()

required = [
    "Status: SOURCE_PROBED / DIRECT_DOWNLOAD_LINKS_NOT_EXPOSED",
    "DES Y6 BAO source path: /releases/y6a2/Y6bao",
    "Direct downloadable machine-readable files were not exposed",
    "No DES Y6 likelihood/data-vector ingestion has occurred",
    "No DFM-MKC superiority claim",
    "No final cosmological truth claim",
    "No theorem-level URF cosmology closure claim",
]

for token in required:
    assert token in s

forbidden = [
    "DES Y6 likelihood ingested",
    "DFM-MKC beats LCDM",
    "DFM-MKC is empirically confirmed",
    "final cosmological truth",
    "URF cosmology closure is proved",
]

for token in forbidden:
    assert token not in s

print("DES Y6 BAO source probe verified.")
