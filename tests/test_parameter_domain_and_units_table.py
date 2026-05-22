import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "parameter_domain_and_units_table_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_parameter_domain_and_units_table.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PARAMETER_DOMAIN_AND_UNITS_TABLE_SUPPLIED_STRUCTURAL_ONLY" in result.stdout
    assert "COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED" in result.stdout

def test_parameter_table_matches_action_couplings():
    params = json.loads(PARAM_SPEC.read_text())
    action = json.loads(ACTION_SPEC.read_text())
    table_symbols = {item["symbol"] for item in params["parameter_table"]}
    assert table_symbols == set(action["coupling_constants"])

def test_parameter_dimensions_and_domains_are_present():
    params = json.loads(PARAM_SPEC.read_text())
    expected_dimensions = {
        "M_Pl": 1,
        "Lambda_0": 4,
        "alpha_phi": 0,
        "m_phi": 1,
        "lambda_phi": 0,
        "alpha_A": 0,
        "m_A": 1,
        "beta_phi_A": 0,
        "xi_phi": 0,
        "xi_A": 0,
        "gamma_m": -1,
    }
    by_symbol = {item["symbol"]: item for item in params["parameter_table"]}
    for symbol, dimension in expected_dimensions.items():
        assert by_symbol[symbol]["mass_dimension"] == dimension
        assert by_symbol[symbol]["domain"]
        assert by_symbol[symbol]["constraint"]
        assert by_symbol[symbol]["appears_in"]

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not prove physical correctness of the parameter choices" in boundary
    assert "does not supply numerical parameter values" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
