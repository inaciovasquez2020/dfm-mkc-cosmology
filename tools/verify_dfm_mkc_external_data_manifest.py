#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_external_data_manifest_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_EXTERNAL_DATA_MANIFEST_2026_05_21.md"

EXPECTED_STATUS = "EXTERNAL_DATA_MANIFEST_CONSOLIDATED_TARGET_ONLY"
EXPECTED_SOURCE_IDS = {
    "DES_SN5YR_0_DATA",
    "DES_Y3_MAGNIFICATION_SYSTEMATICS",
    "PANTHEON_PLUS_SHOES_1_DATA",
}
EXPECTED_BOUNDARY = [
    "Manifest only.",
    "Does not import numerical data vectors.",
    "Does not validate external payloads.",
    "Does not supply DFM equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply frozen DFM predictions.",
    "Does not execute any likelihood.",
    "Does not produce empirical evidence.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
]
EXPECTED_DOES_NOT_PROVE = {
    "DFM",
    "Lambda-CDM failure",
    "CDM replacement",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return json.loads(path.read_text())

def require_repo_paths(data: dict) -> None:
    for source in data["registered_sources"]:
        path = ROOT / source["path"]
        assert path.exists(), f"missing registered source pointer: {path}"
    target_path = ROOT / data["registered_target"]["path"]
    assert target_path.exists(), f"missing registered target: {target_path}"

def verify_artifact(data: dict) -> None:
    assert data["artifact"] == "DFM_MKC_EXTERNAL_DATA_MANIFEST"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "source_manifest_only"
    assert data["registered_source_count"] == 3
    assert data["frozen_prediction_target_registered"] is True
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["root_blocker"] == "DFM_FROZEN_PREDICTION_MAP_NOT_SUPPLIED"

    ids = {source["id"] for source in data["registered_sources"]}
    assert EXPECTED_SOURCE_IDS == ids

    for source in data["registered_sources"]:
        assert source["status"] == "registered_pointer_only"

    target = data["registered_target"]
    assert target["id"] == "DFM_MKC_FROZEN_PREDICTION_MAP_TARGET"
    assert target["status"] == "FROZEN_PREDICTION_MAP_TARGET_ONLY_PREDICTIONS_NOT_SUPPLIED"

    boundary = "\n".join(data["boundary"])
    for token in EXPECTED_BOUNDARY:
        assert token in boundary

    does_not_prove = set(data["does_not_prove"])
    assert EXPECTED_DOES_NOT_PROVE <= does_not_prove

    assert "DESI DR2 BAO products" in data["required_unregistered_sources"]

def verify_doc() -> None:
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")
    doc = DOC.read_text()
    assert EXPECTED_STATUS in doc
    assert "DFM_FROZEN_PREDICTION_MAP_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    require_repo_paths(data)
    verify_doc()
    print("DFM-MKC external data manifest verification OK.")
    print(f"Status: {data['status']}")
    print(f"Registered sources: {data['registered_source_count']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
