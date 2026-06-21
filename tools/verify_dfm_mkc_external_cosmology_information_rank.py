#!/usr/bin/env python3
from pathlib import Path
import json

artifact_path = Path("artifacts/dfm_mkc/external_cosmology_information_rank_2026_06_21.json")
doc_path = Path("docs/status/DFM_MKC_EXTERNAL_COSMOLOGY_INFORMATION_RANK_2026_06_21.md")

data = json.loads(artifact_path.read_text())
doc = doc_path.read_text()

assert data["status"] == "DFM_MKC_EXTERNAL_COSMOLOGY_INFORMATION_RANK_2026_06_21"
assert data["answer"] == "yes_but_not_solution"
assert data["solves"] is False
assert data["weakest_missing_object"] == "DFM_MKC_parameter_to_observable_map_to_ACT_DR6_135_row_prediction_vector"
assert len(data["ranked_external_information"]) == 4

ranked = data["ranked_external_information"]
assert ranked[0]["name"] == "ACT DR6.02 LAMBDA data release"
assert ranked[0]["source_url"] == "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/"
assert ranked[0]["usefulness"] == "strongest_actionable_external_input_surface"
assert "likelihood SACC files" in ranked[0]["helps_by"]
assert ranked[0]["does_not_supply"] == "DFM-MKC forward model or ACT DR6 135-row DFM-MKC prediction vector"

assert ranked[1]["name"] == "DES Y6 cosmology results and data products"
assert ranked[1]["source_url"] == "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/"
assert ranked[1]["does_not_supply"] == "DFM-MKC parameter-to-observable map"

assert ranked[2]["name"] == "DESI DR2 cosmology chains and data products"
assert ranked[2]["source_url"] == "https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/"

assert ranked[3]["name"] == "DESI DR2 publications index"
assert ranked[3]["source_url"] == "https://data.desi.lbl.gov/doc/papers/dr2/"

classification = data["classification"]
assert classification["external_data_surfaces_improved"] is True
assert classification["external_prior_art_improved"] is True
assert classification["direct_dfm_mkc_solver_found"] is False
assert classification["act_dr6_prediction_vector_found"] is False
assert classification["lambda_cdm_rejection_claim_admissible"] is False
assert classification["dfm_mkc_validation_claim_admissible"] is False

assert "external-information ranking only" in data["boundary"]
assert "no new theorem" in data["boundary"]
assert "no cosmology solution" in data["boundary"]
assert "no claim of Lambda-CDM rejection" in data["boundary"]
assert "no DFM-MKC validation" in data["boundary"]
assert "no ACT DR6 135-row prediction vector" in data["boundary"]
assert "parameter-to-observable" in data["next_bounded_improvement"]

assert "Status: `DFM_MKC_EXTERNAL_COSMOLOGY_INFORMATION_RANK_2026_06_21`" in doc
assert "Solves: `false`" in doc
assert "ACT DR6.02 LAMBDA data release" in doc
assert "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/" in doc
assert "DES Y6 cosmology results and data products" in doc
assert "DESI DR2 cosmology chains and data products" in doc
assert "Direct DFM-MKC solver found: no." in doc
assert "DFM-MKC validation claim admissible: no." in doc
assert "external-information ranking only" in doc

print("DFM_MKC_EXTERNAL_COSMOLOGY_INFORMATION_RANK_OK")
