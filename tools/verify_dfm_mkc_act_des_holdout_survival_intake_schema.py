import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_act_des_holdout_survival_intake_schema_2026_05_21.json"
SCHEMA = ROOT / "schemas/dfm_mkc_act_des_holdout_survival_intake_schema_v1.json"
DOC = ROOT / "docs/status/DFM_MKC_ACT_DES_HOLDOUT_SURVIVAL_INTAKE_SCHEMA_2026_05_21.md"

REQUIRED_FUTURE_EVIDENCE = [
    "ACT_HOLDOUT_SURVIVAL_REPORT",
    "DES_HOLDOUT_SURVIVAL_REPORT",
    "FROZEN_PREDICTION_VECTOR_BINDING",
    "PREDECLARED_EVALUATION_PROTOCOL",
    "RESIDUAL_OR_LIKELIHOOD_COMPARISON",
]

DOES_NOT_PROVE = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

DEPENDENCIES = [
    "artifacts/repo_intake/dfm_mkc_frozen_prediction_vector_intake_schema_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_boundary_conditions_intake_schema_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_full_closure_blocker_certificate_2026_05_21.json",
]

def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def main() -> None:
    artifact = load_json(ARTIFACT)
    schema = load_json(SCHEMA)
    doc = DOC.read_text()

    require(artifact["status"] == "INTAKE_SCHEMA_ONLY_NO_EVIDENCE_SUPPLIED", "bad artifact status")
    require(schema["status"] == "INTAKE_SCHEMA_ONLY_NO_EVIDENCE_SUPPLIED", "bad schema status")
    require(artifact["target_slot"] == "ACT_DES_HOLDOUT_SURVIVAL", "bad target slot")
    require(schema["target_slot"] == "ACT_DES_HOLDOUT_SURVIVAL", "bad schema target slot")
    require(artifact["schema"] == "schemas/dfm_mkc_act_des_holdout_survival_intake_schema_v1.json", "bad schema pointer")
    require(artifact["depends_on"] == DEPENDENCIES, "bad dependency list")
    require(artifact["required_future_evidence"] == REQUIRED_FUTURE_EVIDENCE, "bad artifact future evidence list")
    require(schema["required_future_evidence"] == REQUIRED_FUTURE_EVIDENCE, "bad schema future evidence list")
    require(artifact["evidence_supplied"] is False, "artifact must not supply evidence")
    require(schema["evidence_supplied"] is False, "schema must not supply evidence")
    require(artifact["slot_promoted"] is False, "artifact must not promote slot")
    require(schema["slot_promoted"] is False, "schema must not promote slot")
    require(artifact["does_not_prove"] == DOES_NOT_PROVE, "bad artifact boundary list")
    require(schema["does_not_prove"] == DOES_NOT_PROVE, "bad schema boundary list")

    for dep in DEPENDENCIES:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")
        require(dep in doc, f"doc missing dependency: {dep}")

    for item in REQUIRED_FUTURE_EVIDENCE:
        require(item in doc, f"doc missing required future evidence: {item}")

    for boundary in DOES_NOT_PROVE:
        require(boundary in doc, f"doc missing boundary: {boundary}")

    require("No evidence is supplied." in doc, "doc must say no evidence is supplied")
    require("No slot is promoted." in doc, "doc must say no slot is promoted")

    print("DFM-MKC ACT/DES holdout survival intake schema verification OK.")
    print("Status: INTAKE_SCHEMA_ONLY_NO_EVIDENCE_SUPPLIED")

if __name__ == "__main__":
    main()
