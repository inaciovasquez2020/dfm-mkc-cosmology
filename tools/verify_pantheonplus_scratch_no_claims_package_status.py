import json
from pathlib import Path

artifact_path = Path("artifacts/repo_intake/pantheonplus_scratch_no_claims_package_status_2026_06_03.json")
doc_path = Path("docs/status/PANTHEONPLUS_SCRATCH_NO_CLAIMS_PACKAGE_STATUS_2026_06_03.md")

if not artifact_path.exists():
    raise SystemExit("missing artifact")
if not doc_path.exists():
    raise SystemExit("missing status doc")

artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
doc = doc_path.read_text(encoding="utf-8")

assert artifact["object"] == "PantheonPlusScratchNoClaimsPackageRepoStatus"
assert artifact["status"] == "SCRATCH_PACKAGE_STATUS_RECORDED_NO_COSMOLOGY_CLAIM"
assert artifact["package_manifest_status"] == "SCRATCH_ARTIFACTS_PACKAGED_NO_COSMOLOGY_CLAIM"
assert artifact["package_file_count"] == 13
assert artifact["repo_records_only"] is True
assert artifact["large_scratch_payload_not_committed"] is True
assert artifact["next_object"] == "StopOrExternalArchiveScratchPackage"

for key in ["archive_sha256", "manifest_sha256", "sha256s_sha256"]:
    assert isinstance(artifact[key], str)
    assert len(artifact[key]) == 64
    int(artifact[key], 16)

for forbidden in [
    "official PantheonPlus likelihood reproduced",
    "cosmological parameters measured",
    "Lambda_CDM_refuted",
    "dark_energy_resolved",
    "DFM_MKC_validated",
    "new_physics_detected",
    "publication_grade_cosmology_result",
]:
    assert forbidden in artifact["forbidden_claims"]

assert "No official PantheonPlus likelihood reproduction is claimed." in doc
assert "No Lambda-CDM refutation is claimed." in doc
assert "No DFM-MKC validation is claimed." in doc

print("PANTHEONPLUS_SCRATCH_NO_CLAIMS_PACKAGE_STATUS_OK")
