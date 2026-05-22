import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_external_release_reference_and_sacc_schema_conformance_rules.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_external_release_reference_and_sacc_schema_conformance_rules_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_external_release_reference_and_sacc_schema_conformance_rules", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_conformance_rules_are_defined():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["sacc_schema_conformance_rules"]) == module.REQUIRED_RULES
    assert data["summary"]["rules_defined"] == len(module.REQUIRED_RULES)

def test_external_release_reference_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    ref = data["external_release_reference"]
    assert ref["release_url_or_doi"] is None
    assert ref["external_digest"] is None
    assert ref["external_reference_supplied"] is False
    assert ref["external_digest_supplied"] is False
    assert ref["external_digest_matches_local_payload"] is False

def test_rules_are_not_validated():
    data = json.loads(ARTIFACT.read_text())
    assert data["summary"]["rules_validated"] == 0
    assert data["summary"]["full_sacc_schema_conformance_established"] is False
    for entry in data["sacc_schema_conformance_rules"].values():
        assert entry["validated"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
