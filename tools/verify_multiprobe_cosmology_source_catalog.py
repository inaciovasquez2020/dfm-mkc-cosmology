#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/cosmology/multiprobe_cosmology_source_catalog_2026_05_24.json")
DOC = Path("docs/status/MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_2026_05_24.md")

REQUIRED_DATASETS = [
    "DESI_DR2_BAO",
    "PLANCK_2018_PLIK_LOWELL",
    "ACT_DR6_CMB_LENSING",
    "SPT_3G_DR1",
    "DES_Y6_3X2PT",
    "PANTHEON_PLUS",
    "ROMAN_MOCK_SN",
    "ESGB_SCALAR_DARK_SECTOR_COMPARATOR_2507_05207_V3",
]

REQUIRED_PACKET_FIELDS = [
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
]

REQUIRED_NEGATIVE_LOCK = [
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
]

REQUIRED_BOUNDARY_DOC = [
    "does not certify that any listed data vector has been downloaded",
    "does not certify covariance matrices",
    "does not certify nuisance priors",
    "does not run Cobaya",
    "does not produce posterior chains",
    "does not compare ΛCDM against DFM-MKC",
    "does not reject Lambda-CDM",
    "does not validate DFM-MKC",
    "does not provide Chronos proof input",
    "does not prove R1/R2/R3",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

def main() -> None:
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["record_id"] == "MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_2026_05_24"
    assert data["status"] == "SOURCE_CATALOG_RECORD_ONLY_DIGESTS_AND_LIKELIHOOD_RUNS_PENDING"
    assert data["strand"] == "DFM-MKC / cosmology"

    dataset_ids = {item["dataset_id"] for item in data["datasets"]}
    for dataset_id in REQUIRED_DATASETS:
        assert dataset_id in dataset_ids, dataset_id
        assert dataset_id in doc, dataset_id

    assert data["first_certified_packet_target"]["target_id"] == "CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET"
    assert data["first_certified_packet_target"]["minimal_dataset_choice"] == "DESI_DR2_BAO"

    for field in REQUIRED_PACKET_FIELDS:
        assert field in data["first_certified_packet_target"]["required_fields"], field
        assert field in doc, field

    for token in REQUIRED_NEGATIVE_LOCK:
        assert token in data["negative_use_lock"], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY_DOC:
        assert token in doc, token

    print("MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_OK")

if __name__ == "__main__":
    main()
