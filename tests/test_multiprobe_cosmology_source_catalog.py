import json
import subprocess
from pathlib import Path

ART = Path("artifacts/cosmology/multiprobe_cosmology_source_catalog_2026_05_24.json")
DOC = Path("docs/status/MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_2026_05_24.md")

def test_catalog_status_is_source_catalog_only():
    data = json.loads(ART.read_text())
    assert data["record_id"] == "MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_2026_05_24"
    assert data["status"] == "SOURCE_CATALOG_RECORD_ONLY_DIGESTS_AND_LIKELIHOOD_RUNS_PENDING"
    assert data["strand"] == "DFM-MKC / cosmology"

def test_catalog_contains_expected_datasets():
    data = json.loads(ART.read_text())
    dataset_ids = {item["dataset_id"] for item in data["datasets"]}
    assert {
        "DESI_DR2_BAO",
        "PLANCK_2018_PLIK_LOWELL",
        "ACT_DR6_CMB_LENSING",
        "SPT_3G_DR1",
        "DES_Y6_3X2PT",
        "PANTHEON_PLUS",
        "ROMAN_MOCK_SN",
        "ESGB_SCALAR_DARK_SECTOR_COMPARATOR_2507_05207_V3",
    } <= dataset_ids

def test_first_certified_packet_target_fields_are_explicit():
    data = json.loads(ART.read_text())
    target = data["first_certified_packet_target"]
    assert target["target_id"] == "CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET"
    assert target["minimal_dataset_choice"] == "DESI_DR2_BAO"
    for field in [
        "dataset_name",
        "source_url",
        "release_version",
        "data_vector_path",
        "covariance_path",
        "nuisance_prior_path_or_null",
        "likelihood_config_path",
        "data_vector_sha256",
        "covariance_sha256",
        "nuisance_priors_sha256_or_null",
        "likelihood_config_sha256",
        "cross_covariance_policy",
        "lcdm_baseline_command",
        "dfm_mkc_comparison_command",
        "boundary",
    ]:
        assert field in target["required_fields"]

def test_catalog_negative_use_lock():
    text = DOC.read_text()
    for token in [
        "source catalog only",
        "no downloaded data vectors certified",
        "no covariance digests certified",
        "no likelihood execution",
        "no Lambda-CDM rejection",
        "no DFM-MKC validation",
        "not Chronos proof input",
        "not evidence for R1",
        "not evidence for R2",
        "not evidence for R3",
        "not evidence for NON_FACTORISATION",
        "not evidence for Chronos-RR",
        "not evidence for H4.1/FGL",
        "not evidence for P vs NP",
        "not evidence for any Clay problem",
    ]:
        assert token in text

def test_catalog_verifier_passes():
    out = subprocess.check_output(
        ["python3", "tools/verify_multiprobe_cosmology_source_catalog.py"],
        text=True,
    )
    assert "MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_OK" in out
