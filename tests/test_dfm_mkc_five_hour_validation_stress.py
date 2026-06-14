import json
from pathlib import Path

from stress.five_hour_validation_stress import OBJECT_ID, STATUS, run_stress


def test_five_hour_validation_stress_smoke(tmp_path: Path):
    report = tmp_path / "five_hour_stress.json"
    certificate = run_stress(
        duration_seconds=0.0,
        seed=20260614,
        report_path=report,
        min_cases=1,
        max_cases=1,
    )

    assert certificate["id"] == OBJECT_ID
    assert certificate["status"] == STATUS
    assert certificate["cases_completed"] == 1
    assert certificate["case_digest"]
    assert report.exists()

    saved = json.loads(report.read_text())
    assert saved["id"] == OBJECT_ID
    assert "theorem-level closure" in saved["does_not_prove"]
    assert "finite positive Hubble output" in saved["invariants_checked"]
