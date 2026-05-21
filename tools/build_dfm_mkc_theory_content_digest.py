from pathlib import Path
import hashlib
import json

ROOT = Path.cwd()

FILES = [
    "README.md",
    "STATUS.md",
    "registry_id.txt",
    "verification_audit.log",
    "mkc_solver.py",
    "dfm_mkc/model.py",
    "dfm_mkc/constants.py",
    "dfm_mkc/likelihoods.py",
    "theory/deformation_field.md",
    "theory/friedmann.md",
    "theory/geometry.md",
    "theory/interpretation.md",
    "theory/limits.md",
    "theory/observables.md",
    "theory/parameters.md",
    "theory/priors.md",
    "theory/redshift_dynamics.md",
    "perturbations/linear_scalar.md",
    "solver/background_solver.py",
    "solver/distances.py",
    "solver/lcdm_compare.py",
    "solver/scan.py",
    "src/models/dfm_mkc.py",
    "numerics/background_equations.md",
    "numerics/class_interface.md",
    "numerics/interface_notes.md",
    "likelihoods/likelihood_api.md",
    "data/des_y6/AUTHENTIC_INPUT_MANIFEST.json",
    "models",
]

items = []

for rel in FILES:
    path = ROOT / rel
    if not path.exists() or not path.is_file():
        items.append({"path": rel, "exists": False})
        continue

    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")

    items.append({
        "path": rel,
        "exists": True,
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "content_excerpt": text[:4000],
        "truncated": len(text) > 4000,
    })

out = ROOT / "artifacts/repo_intake/dfm_mkc_theory_content_digest_2026_05_21.json"
out.write_text(json.dumps({
    "artifact": "DFM_MKC_THEORY_CONTENT_DIGEST_2026_05_21",
    "status": "THEORY_CONTENT_DIGEST_CREATED",
    "repository": "dfm-mkc-cosmology",
    "boundary": [
        "content digest only",
        "no DFM-MKC proof",
        "no Lambda-CDM failure claim",
        "no ACT/DES holdout survival claim",
        "no final cosmological truth claim"
    ],
    "items": items,
}, indent=2, sort_keys=True) + "\n")

print(out)
