import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_reproducible_download_command_or_external_sha256_digest.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_command_or_external_sha256_digest_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_reproducible_download_command_or_external_sha256_digest", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_official_references_bound():
    data = json.loads(ARTIFACT.read_text())
    assert data["official_references"]["act_dr6_data_products"].startswith("https://act.princeton.edu/")
    assert data["official_references"]["dr6_act_lite_repository"].startswith("https://github.com/ACTCollaboration/")

def test_reproducible_download_command_is_bound_but_not_executed():
    data = json.loads(ARTIFACT.read_text())
    assert data["reproducible_download_command_supplied"] is True
    assert "cobaya-install act_dr6_cmbonly" in data["reproducible_download_commands"]
    assert data["reproducible_download_executed"] is False
    assert data["download_reproduces_local_sha256"] is False

def test_external_digest_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["external_sha256_digest"] is None
    assert data["external_sha256_digest_supplied"] is False
    assert data["downloaded_payload_sha256"] is None

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 reproducible download execution" in data["does_not_prove"]
    assert "ACT DR6 downloaded payload hash match" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
