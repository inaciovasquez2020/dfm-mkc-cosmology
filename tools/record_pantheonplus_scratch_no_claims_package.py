import hashlib
import json
from pathlib import Path

ROOT = Path.home()
REPO = Path.cwd()

package_dir = ROOT / "pantheonplus_scratch_no_claims_package_2026_06_03"
archive = ROOT / "pantheonplus_scratch_no_claims_package_2026_06_03.tar.gz"
manifest = package_dir / "pantheonplus_scratch_no_claims_package_manifest_2026_06_03.json"
sha_file = package_dir / "SHA256SUMS"

missing = [str(p) for p in [package_dir, archive, manifest, sha_file] if not p.exists()]
if missing:
    raise SystemExit(json.dumps({
        "decision": "FAIL",
        "status": "MISSING_LOCAL_SCRATCH_PACKAGE_OBJECTS",
        "missing": missing
    }, indent=2))

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

manifest_data = json.loads(manifest.read_text(encoding="utf-8"))

artifact = {
    "object": "PantheonPlusScratchNoClaimsPackageRepoStatus",
    "status": "SCRATCH_PACKAGE_STATUS_RECORDED_NO_COSMOLOGY_CLAIM",
    "date": "2026-06-03",
    "local_package_dir": str(package_dir),
    "local_archive": str(archive),
    "local_manifest": str(manifest),
    "local_sha256s": str(sha_file),
    "package_manifest_status": manifest_data.get("status"),
    "package_file_count": manifest_data.get("file_count"),
    "archive_size_bytes": archive.stat().st_size,
    "archive_sha256": sha256_file(archive),
    "manifest_sha256": sha256_file(manifest),
    "sha256s_sha256": sha256_file(sha_file),
    "repo_records_only": True,
    "large_scratch_payload_not_committed": True,
    "valid_claim": "A local PantheonPlus scratch package was hash-recorded for provenance and boundary tracking.",
    "forbidden_claims": [
        "official PantheonPlus likelihood reproduced",
        "cosmological parameters measured",
        "Lambda_CDM_refuted",
        "dark_energy_resolved",
        "DFM_MKC_validated",
        "new_physics_detected",
        "publication_grade_cosmology_result"
    ],
    "next_object": "StopOrExternalArchiveScratchPackage"
}

if artifact["package_manifest_status"] != "SCRATCH_ARTIFACTS_PACKAGED_NO_COSMOLOGY_CLAIM":
    raise SystemExit(json.dumps({
        "decision": "FAIL",
        "status": "UNEXPECTED_PACKAGE_MANIFEST_STATUS",
        "found": artifact["package_manifest_status"]
    }, indent=2))

if artifact["package_file_count"] != 13:
    raise SystemExit(json.dumps({
        "decision": "FAIL",
        "status": "UNEXPECTED_PACKAGE_FILE_COUNT",
        "found": artifact["package_file_count"]
    }, indent=2))

out = REPO / "artifacts/repo_intake/pantheonplus_scratch_no_claims_package_status_2026_06_03.json"
out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

doc = REPO / "docs/status/PANTHEONPLUS_SCRATCH_NO_CLAIMS_PACKAGE_STATUS_2026_06_03.md"
doc.write_text(
    "# PantheonPlus Scratch No-Claims Package Status — 2026-06-03\n\n"
    "Status: `SCRATCH_PACKAGE_STATUS_RECORDED_NO_COSMOLOGY_CLAIM`\n\n"
    "This record hash-registers a local PantheonPlus scratch package produced outside the repository.\n\n"
    "Recorded object:\n\n"
    f"- Local archive: `{artifact['local_archive']}`\n"
    f"- Archive SHA-256: `{artifact['archive_sha256']}`\n"
    f"- Manifest SHA-256: `{artifact['manifest_sha256']}`\n"
    f"- Package file count: `{artifact['package_file_count']}`\n\n"
    "Boundary:\n\n"
    "- No official PantheonPlus likelihood reproduction is claimed.\n"
    "- No cosmological parameter measurement is claimed.\n"
    "- No Lambda-CDM refutation is claimed.\n"
    "- No dark-energy resolution is claimed.\n"
    "- No DFM-MKC validation is claimed.\n"
    "- No new-physics detection is claimed.\n"
    "- No publication-grade cosmology result is claimed.\n\n"
    "Next admissible object: `StopOrExternalArchiveScratchPackage`.\n",
    encoding="utf-8"
)

print(json.dumps({
    "decision": "PASS",
    "artifact": str(out),
    "status": artifact["status"],
    "archive_sha256": artifact["archive_sha256"],
    "manifest_sha256": artifact["manifest_sha256"],
    "package_file_count": artifact["package_file_count"],
    "next_object": artifact["next_object"]
}, indent=2))
