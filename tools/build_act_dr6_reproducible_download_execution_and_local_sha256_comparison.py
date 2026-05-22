#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_command_or_external_sha256_digest_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_execution_and_local_sha256_comparison_2026_05_22.json"
WORK = ROOT / "artifacts/reproducible_downloads/act_dr6_2026_05_22"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def run(cmd, cwd=None):
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=900,
        )
        return {
            "cmd": " ".join(cmd),
            "returncode": p.returncode,
            "output_tail": p.stdout[-4000:],
        }
    except FileNotFoundError as exc:
        return {
            "cmd": " ".join(cmd),
            "returncode": 127,
            "output_tail": f"missing executable: {exc.filename}",
        }

def find_candidate_payloads(root: Path):
    candidates = []
    for p in root.rglob("*"):
        if p.is_file() and (
            p.name.endswith(".fits")
            or p.name.endswith(".fits.gz")
            or "sacc" in p.name.lower()
        ):
            candidates.append({
                "path": str(p.relative_to(ROOT)),
                "size_bytes": p.stat().st_size,
                "sha256": sha256_file(p),
            })
    return sorted(candidates, key=lambda x: (x["path"], x["size_bytes"]))

def main():
    source = json.loads(SOURCE.read_text())
    local_path = ROOT / source["local_path"]
    local_sha256 = source["local_sha256"]

    executed_steps = []
    WORK.mkdir(parents=True, exist_ok=True)
    repo = WORK / "DR6-ACT-lite"

    status = "DOWNLOAD_EXECUTION_ATTEMPTED_NOT_CERTIFIED"
    execution_attempted = True

    if not repo.exists():
        executed_steps.append(run([
            "git", "clone", "https://github.com/ACTCollaboration/DR6-ACT-lite.git", str(repo)
        ]))
    else:
        executed_steps.append({
            "cmd": "git clone https://github.com/ACTCollaboration/DR6-ACT-lite.git DR6-ACT-lite",
            "returncode": 0,
            "output_tail": "repository already present"
        })

    if executed_steps[-1]["returncode"] == 0:
        executed_steps.append(run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=repo))

    if executed_steps[-1]["returncode"] == 0:
        executed_steps.append(run(["cobaya-install", "act_dr6_cmbonly"], cwd=repo))

    downloaded_payloads = find_candidate_payloads(WORK)
    matching = [p for p in downloaded_payloads if p["sha256"] == local_sha256]

    download_completed = bool(downloaded_payloads)
    hash_match = bool(matching)

    if hash_match:
        status = "REPRODUCIBLE_DOWNLOAD_EXECUTED_LOCAL_SHA256_MATCHED"
    elif download_completed:
        status = "REPRODUCIBLE_DOWNLOAD_EXECUTED_LOCAL_SHA256_NOT_MATCHED"
    else:
        status = "REPRODUCIBLE_DOWNLOAD_EXECUTION_FAILED_OR_NO_PAYLOAD_FOUND"

    artifact = {
        "object": "ACT_DR6_REPRODUCIBLE_DOWNLOAD_EXECUTION_AND_LOCAL_SHA256_COMPARISON",
        "date": "2026-05-22",
        "status": status,
        "source_object": source["object"],
        "local_path": source["local_path"],
        "local_sha256": local_sha256,
        "execution_attempted": execution_attempted,
        "download_completed": download_completed,
        "downloaded_payloads": downloaded_payloads,
        "matching_payloads": matching,
        "download_reproduces_local_sha256": hash_match,
        "executed_steps": executed_steps,
        "certified_for_profiled_likelihood_execution": False,
        "required_next_object": (
            "ACT_DR6_FULL_SACC_SCHEMA_VALIDATION"
            if hash_match else
            "ACT_DR6_DOWNLOAD_FAILURE_OR_HASH_MISMATCH_AUDIT"
        ),
        "does_not_prove": [
            "ACT DR6 full SACC schema certification",
            "complete certified likelihood manifest",
            "executed multiprobe likelihood run",
            "Lambda-CDM rejection",
            "six-parameter flat Lambda-CDM rejection",
            "alternative-model validation",
            "DFM-MKC validation",
            "dark matter resolution",
            "dark energy resolution",
            "any Clay problem"
        ]
    }

    OUT.write_text(json.dumps(artifact, indent=2) + "\n")
    print("ACT DR6 reproducible download execution and local sha256 comparison artifact written.")
    print("Status:", status)
    print("Download reproduces local sha256:", hash_match)

if __name__ == "__main__":
    main()
