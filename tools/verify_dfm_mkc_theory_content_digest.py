from pathlib import Path
import json

p = Path("artifacts/repo_intake/dfm_mkc_theory_content_digest_2026_05_21.json")
data = json.loads(p.read_text())

assert data["status"] == "THEORY_CONTENT_DIGEST_CREATED"
paths = {item["path"] for item in data["items"] if item.get("exists")}
for required in [
    "dfm_mkc/model.py",
    "dfm_mkc/constants.py",
    "mkc_solver.py",
    "theory/friedmann.md",
    "theory/parameters.md",
    "perturbations/linear_scalar.md",
    "src/models/dfm_mkc.py",
    "numerics/background_equations.md",
    "data/des_y6/AUTHENTIC_INPUT_MANIFEST.json",
]:
    assert required in paths, required

for token in [
    "content digest only",
    "no DFM-MKC proof",
    "no Lambda-CDM failure claim",
    "no ACT/DES holdout survival claim",
]:
    assert token in data["boundary"], token

print("DFM-MKC theory content digest verified.")
