from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPECTED = {
    "desi_dr2": [
        ROOT / "public_data" / "desi_dr2" / "bao_summary.csv",
        ROOT / "public_data" / "desi_dr2" / "cosmology_chains.csv",
    ],
    "des_y6": [
        ROOT / "public_data" / "des_y6" / "y6_3x2pt_summary.csv",
        ROOT / "public_data" / "des_y6" / "y6_covariance.csv",
    ],
    "planck": [
        ROOT / "public_data" / "planck" / "planck_2018_baseline_params.csv",
    ],
}

def dataset_status() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for name, files in EXPECTED.items():
        out[name] = {
            "present": all(p.exists() for p in files),
            "missing": [str(p.relative_to(ROOT)) for p in files if not p.exists()],
        }
    return out

def require_dataset(name: str) -> list[Path]:
    status = dataset_status()
    if name not in status:
        raise KeyError(name)
    if not status[name]["present"]:
        missing = "\n".join(status[name]["missing"])
        raise FileNotFoundError(f"missing public data files for {name}:\n{missing}")
    return EXPECTED[name]

if __name__ == "__main__":
    print(json.dumps(dataset_status(), indent=2, sort_keys=True))
