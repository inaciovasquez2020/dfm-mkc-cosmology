from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "docs/status/DES_Y6_REAL_DATA_MATERIALIZATION_FRONTIER_2026_05_10.md",
    ROOT / "public_data/des_y6/y6_3x2pt_summary.csv",
    ROOT / "public_data/des_y6/y6_covariance.csv",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("missing files:")
    print("\n".join(missing))
    sys.exit(1)

summary = (ROOT / "public_data/des_y6/y6_3x2pt_summary.csv").read_text(errors="ignore")
cov = (ROOT / "public_data/des_y6/y6_covariance.csv").read_text(errors="ignore")
doc = (ROOT / "docs/status/DES_Y6_REAL_DATA_MATERIALIZATION_FRONTIER_2026_05_10.md").read_text()

assert "FRONTIER_OPEN" in doc
assert "AuthenticDESY6Materialization" in doc
assert "SYNTHETIC_PLACEHOLDER" not in summary
assert "SYNTHETIC_PLACEHOLDER" not in cov
assert "<html>" not in summary.lower()
assert "<html>" not in cov.lower()
assert "404 Not Found" not in summary
assert "404 Not Found" not in cov

print("DES Y6 real-data materialization frontier verified.")
