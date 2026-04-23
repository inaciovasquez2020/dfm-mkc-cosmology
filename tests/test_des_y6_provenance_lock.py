import json
import hashlib
from pathlib import Path

FILES = [
    Path("public_data/des_y6/y6_3x2pt_summary.csv"),
    Path("public_data/des_y6/y6_covariance.csv"),
]

def _fingerprint(path: Path):
    data = path.read_bytes()
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "rows": len(data.decode("utf-8", errors="ignore").splitlines()),
    }

def test_des_y6_export_recipe_exists():
    p = Path("docs/data/DES_Y6_EXPORT_RECIPE.md")
    s = p.read_text(encoding="utf-8")
    assert "Status: Closed" in s
    assert "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/" in s
    assert "https://dev.des.ncsa.illinois.edu/" in s

def test_des_y6_fingerprints_match_frozen_artifact():
    frozen = json.loads(
        Path("artifacts/data/des_y6_fingerprints.json").read_text(encoding="utf-8")
    )
    current = {str(path): _fingerprint(path) for path in FILES}
    assert current == frozen
