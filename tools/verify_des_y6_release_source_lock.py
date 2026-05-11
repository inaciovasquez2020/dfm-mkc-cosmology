from pathlib import Path

p = Path("docs/status/DES_Y6_RELEASE_SOURCE_LOCK_2026_05_11.md")
s = p.read_text()

required = [
    "Status: AUTHENTIC_INPUT_PENDING / SOURCE_LOCKED",
    "Official DES release page",
    "Official source URL",
    "SHA256 checksums",
    "Frozen DFM-MKC parameter rules already present",
    "DFM-MKC superiority claim before authentic input",
    "final cosmological truth claim",
    "theorem-level URF cosmology closure claim",
]

for phrase in required:
    assert phrase in s

forbidden_positive_claims = [
    "DFM-MKC beats Lambda-CDM",
    "DFM-MKC proves final cosmological truth",
    "URF cosmology closure is proved",
    "DES Y6 authentic input materialized",
]

for phrase in forbidden_positive_claims:
    assert phrase not in s

print("DES Y6 release source lock verified.")
