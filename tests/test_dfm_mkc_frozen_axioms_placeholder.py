from pathlib import Path
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_frozen_axioms_placeholder_2026_05_21.json")

def test_frozen_axioms_placeholder_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_frozen_axioms_placeholder.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC frozen axioms placeholder verification OK." in result.stdout
    assert "FROZEN_AXIOMS_PLACEHOLDER_ONLY_FIELD_EQUATIONS_NOT_SUPPLIED" in result.stdout

def test_all_frozen_axiom_slots_are_placeholder_null():
    data = json.loads(ARTIFACT.read_text())
    assert data["frozen_axiom_slots"] == {
        "action_functional": None,
        "field_equations": None,
        "matter_coupling_rule": None,
        "parameter_table": None,
        "boundary_conditions": None,
        "prediction_map": None,
    }

def test_boundary_preserves_no_execution_and_no_evidence():
    data = json.loads(ARTIFACT.read_text())
    assert "placeholder only" in data["boundary"]
    assert "does not supply DFM-MKC field equations" in data["boundary"]
    assert "does not supply a likelihood rule" in data["boundary"]
    assert "does not execute the likelihood" in data["boundary"]
    assert "does not supply empirical evidence" in data["boundary"]
    assert "does not promote any empirical slot" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
