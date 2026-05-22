#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026_05_22"

EXPECTED = {
    "MULTIPROBE_LCDM_REJECTION_DATASET_REGISTRY": "DATASET_REGISTRY_ONLY_NO_LCDM_REJECTION",
    "DESI_DR2_CMB_SN_REJECTION_REPRODUCER": "REPRODUCER_SPEC_ONLY_NO_EXECUTED_LIKELIHOOD",
    "GROWTH_SECTOR_HOLDOUT_COMPATIBILITY_TEST": "HOLDOUT_TEST_SPEC_ONLY_NO_EXECUTED_GROWTH_REJECTION",
    "H0_DISTANCE_LADDER_SYSTEMATICS_PROFILE": "SYSTEMATICS_PROFILE_ONLY_NO_H0_DISPROOF",
    "ALTERNATIVE_MODEL_STABILITY_SCORECARD": "SCORECARD_ONLY_NO_ALTERNATIVE_VALIDATED",
}

SLUGS = [
    "multiprobe_lcdm_rejection_dataset_registry",
    "desi_dr2_cmb_sn_rejection_reproducer",
    "growth_sector_holdout_compatibility_test",
    "h0_distance_ladder_systematics_profile",
    "alternative_model_stability_scorecard",
]

REQUIRED_DOES_NOT_PROVE = {
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem",
}

REQUIRED_SOURCE_IDS = {
    "PLANCK_2018_COSMOLOGICAL_PARAMETERS",
    "ACT_DR6_POWER_SPECTRA_LIKELIHOODS",
    "DESI_DR2_BAO",
    "PANTHEON_PLUS_SH0ES_DATA_RELEASE",
    "DES_Y6_3X2PT",
    "JWST_SH0ES_CEPHEID_CROSSCHECK",
}

def main():
    seen = {}
    for slug in SLUGS:
        path = ROOT / "artifacts" / "cosmology" / f"{slug}_{STAMP}.json"
        assert path.exists(), path
        data = json.loads(path.read_text())
        artifact_id = data["id"]
        seen[artifact_id] = data["status"]
        assert EXPECTED[artifact_id] == data["status"]
        assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))
        assert REQUIRED_SOURCE_IDS.issubset({x["id"] for x in data["source_basis"]})
        assert "no Lambda-CDM rejection certificate" in data["boundary"]

        doc = ROOT / "docs" / "status" / f"{artifact_id}_{STAMP}.md"
        assert doc.exists(), doc
        text = doc.read_text()
        assert data["status"] in text
        assert data["required_next_object"] in text
        assert "Does not prove" in text
        assert "Lambda-CDM failure" in text
        assert "any Clay problem" in text

    assert seen == EXPECTED
    print("Multiprobe Lambda-CDM rejection frontier bundle verification OK.")
    print("Status: FRONTIER_BUNDLE_ONLY_NO_LCDM_REJECTION")
    print("Required next object: OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE")

if __name__ == "__main__":
    main()
