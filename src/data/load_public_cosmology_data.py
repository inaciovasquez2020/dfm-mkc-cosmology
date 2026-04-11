from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPECTED = {
    "desi_dr2": [
        ROOT / "public_data" / "desi_dr2" / "cobaya" / "base" / "desi-bao-all" / "chain.1.txt",
        ROOT / "public_data" / "desi_dr2" / "iminuit" / "base" / "desi-bao-all" / "bestfit.minimum.txt",
    ],
    "des_y6": [
        ROOT / "public_data" / "des_y6" / "y6_3x2pt_summary.csv",
        ROOT / "public_data" / "des_y6" / "y6_covariance.csv",
    ],
    "planck": [
        ROOT / "public_data" / "planck" / "planck_2018_baseline_params.csv",
    ],
}

def _is_synthetic(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        head = path.read_text(errors="ignore")[:4096]
    except Exception:
        return False
    return "SYNTHETIC_PLACEHOLDER" in head

def dataset_status() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for name, files in EXPECTED.items():
        missing = [str(p.relative_to(ROOT)) for p in files if not p.exists()]
        synthetic = [str(p.relative_to(ROOT)) for p in files if p.exists() and _is_synthetic(p)]
        out[name] = {
            "present": len(missing) == 0 and len(synthetic) == 0,
            "synthetic_present": len(missing) == 0 and len(synthetic) > 0,
            "missing": missing,
            "synthetic_files": synthetic,
        }
    return out

def require_dataset(name: str) -> list[Path]:
    status = dataset_status()
    if name not in status:
        raise KeyError(name)
    if status[name]["missing"] or status[name]["synthetic_files"]:
        parts: list[str] = []
        if status[name]["missing"]:
            parts.append("missing:\n" + "\n".join(status[name]["missing"]))
        if status[name]["synthetic_files"]:
            parts.append("synthetic:\n" + "\n".join(status[name]["synthetic_files"]))
        raise FileNotFoundError(f"dataset {name} is not real-data ready:\n" + "\n".join(parts))
    return EXPECTED[name]

if __name__ == "__main__":
    print(json.dumps(dataset_status(), indent=2, sort_keys=True))
