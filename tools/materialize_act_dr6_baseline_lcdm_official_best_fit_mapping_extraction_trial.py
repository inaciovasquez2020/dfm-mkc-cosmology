#!/usr/bin/env python3
import hashlib
import json
import os
import re
import shutil
import tarfile
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

OFFICIAL_TAR_URL = "https://lambda.gsfc.nasa.gov/data/act/pspipe/best_fits/act_dr6.02_best_fits_dr6_lcdm.tar.gz"
OFFICIAL_INFO_URL = "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_pspipe_best_fits_info.html"
OFFICIAL_GET_URL = "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_pspipe_best_fits_get.html"

PAYLOAD_DIR = Path("artifacts/dfm_mkc/act_dr6_official_best_fits_dr6_lcdm_payload_2026_05_25")
TAR_PATH = PAYLOAD_DIR / "act_dr6.02_best_fits_dr6_lcdm.tar.gz"
EXTRACT_DIR = PAYLOAD_DIR / "extracted"

ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
ROW_TARGET = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_row_order_mapping_target_2026_05_25.json")
HARNESS_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_extraction_harness_2026_05_25.json")
HARNESS_SCRIPT = Path("tools/extract_act_dr6_baseline_lcdm_official_best_fit_vector.py")
SACC_PATH = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits")

COMBINED_TABLE = PAYLOAD_DIR / "act_dr6_best_fit_combined_numeric_table.txt"
COMBINED_META = PAYLOAD_DIR / "act_dr6_best_fit_combined_numeric_table_metadata.json"
ROW_METADATA = PAYLOAD_DIR / "act_dr6_cmbonly_sacc_row_order_metadata.json"
ROW_MAPPING = PAYLOAD_DIR / "act_dr6_baseline_lcdm_official_best_fit_row_mapping_trial.json"
EXTRACTION_CANDIDATE = PAYLOAD_DIR / "act_dr6_baseline_lcdm_official_best_fit_extraction_candidate.json"
AUDIT = PAYLOAD_DIR / "act_dr6_baseline_lcdm_official_best_fit_row_order_audit_trial.json"
ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial_2026_05_25.json")

COLUMN_MAP = {
    "TT": 1,
    "TE": 2,
    "TB": 3,
    "ET": 4,
    "BT": 5,
    "EE": 6,
    "EB": 7,
    "BE": 8,
    "BB": 9,
}

def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def download_official_tar() -> Dict[str, Any]:
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if not TAR_PATH.exists():
        with urllib.request.urlopen(OFFICIAL_TAR_URL, timeout=120) as response:
            TAR_PATH.write_bytes(response.read())
    return {
        "url": OFFICIAL_TAR_URL,
        "path": str(TAR_PATH),
        "bytes": TAR_PATH.stat().st_size,
        "sha256": sha256_file(TAR_PATH),
    }

def safe_extract_tar() -> List[str]:
    if EXTRACT_DIR.exists():
        shutil.rmtree(EXTRACT_DIR)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    names: List[str] = []
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        for member in tar.getmembers():
            target = EXTRACT_DIR / member.name
            resolved = target.resolve()
            if not str(resolved).startswith(str(EXTRACT_DIR.resolve())):
                raise SystemExit(f"unsafe tar member: {member.name}")
            tar.extract(member, EXTRACT_DIR)
            names.append(member.name)
    return sorted(names)

def read_numeric_table(path: Path) -> Optional[np.ndarray]:
    try:
        arr = np.loadtxt(path, comments="#")
    except Exception:
        return None
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.ndim != 2 or arr.shape[1] < 10:
        return None
    return arr[:, :10].astype(float)

def build_combined_table() -> Dict[str, Any]:
    rows: List[np.ndarray] = []
    metadata: List[Dict[str, Any]] = []
    source_files = sorted(
        p for p in EXTRACT_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in {".txt", ".dat", ".tsv", ".csv"}
    )

    global_row = 0
    accepted_files = []
    rejected_files = []

    for file_index, path in enumerate(source_files):
        table = read_numeric_table(path)
        rel = str(path.relative_to(EXTRACT_DIR))
        if table is None:
            rejected_files.append(rel)
            continue
        accepted_files.append(rel)
        for local_row, row in enumerate(table):
            rows.append(row)
            metadata.append({
                "global_row": global_row,
                "source_file_index": file_index,
                "source_file": rel,
                "local_row": local_row,
                "ell": float(row[0]),
                "columns": {
                    "0": "l",
                    "1": "Dl_TT",
                    "2": "Dl_TE",
                    "3": "Dl_TB",
                    "4": "Dl_ET",
                    "5": "Dl_BT",
                    "6": "Dl_EE",
                    "7": "Dl_EB",
                    "8": "Dl_BE",
                    "9": "Dl_BB"
                }
            })
            global_row += 1

    if rows:
        combined = np.vstack(rows)
        np.savetxt(COMBINED_TABLE, combined)
    else:
        combined = np.empty((0, 10), dtype=float)
        np.savetxt(COMBINED_TABLE, combined)

    meta = {
        "combined_table": str(COMBINED_TABLE),
        "combined_shape": list(combined.shape),
        "combined_sha256": sha256_file(COMBINED_TABLE),
        "metadata_rows": metadata,
        "accepted_source_files": accepted_files,
        "rejected_source_files": rejected_files,
    }
    COMBINED_META.write_text(json.dumps(meta, indent=2) + "\n")
    return meta

def normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())

def infer_spectrum_label(data_type: str) -> Optional[str]:
    text = data_type.lower()
    if "tt" in text or "cl_00" in text:
        return "TT"
    if "te" in text or "cl_0e" in text:
        return "TE"
    if "et" in text or "cl_e0" in text:
        return "ET"
    if "ee" in text or "cl_ee" in text:
        return "EE"
    if "bb" in text or "cl_bb" in text:
        return "BB"
    if "tb" in text or "cl_0b" in text:
        return "TB"
    if "bt" in text or "cl_b0" in text:
        return "BT"
    if "eb" in text or "cl_eb" in text:
        return "EB"
    if "be" in text or "cl_be" in text:
        return "BE"
    return None

def scalar_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        arr = np.asarray(value)
        if arr.size == 1:
            return float(arr.reshape(-1)[0])
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return None

def load_sacc_metadata() -> Dict[str, Any]:
    if not SACC_PATH.exists():
        return {
            "status": "SACC_FILE_MISSING",
            "path": str(SACC_PATH),
            "rows": [],
            "missing_reason": "ACT DR6 CMB-only SACC/FITS file is absent."
        }

    try:
        import sacc  # type: ignore
    except Exception as exc:
        return {
            "status": "SACC_IMPORT_FAILED",
            "path": str(SACC_PATH),
            "rows": [],
            "missing_reason": repr(exc)
        }

    try:
        s = sacc.Sacc.load_fits(str(SACC_PATH))
    except Exception as exc:
        return {
            "status": "SACC_LOAD_FAILED",
            "path": str(SACC_PATH),
            "rows": [],
            "missing_reason": repr(exc)
        }

    rows = []
    for i, dp in enumerate(getattr(s, "data", [])):
        tags = dict(getattr(dp, "tags", {}) or {})
        data_type = str(getattr(dp, "data_type", ""))
        tracers = list(getattr(dp, "tracers", []) or [])
        value = scalar_float(getattr(dp, "value", None))

        ell = None
        for key in ["ell", "ells", "l", "lb", "leff", "ell_eff"]:
            if key in tags:
                ell = scalar_float(tags.get(key))
                if ell is not None:
                    break

        row = {
            "target_index": i,
            "data_type": data_type,
            "spectrum_label": infer_spectrum_label(data_type),
            "tracers": tracers,
            "tags": {str(k): str(v) for k, v in tags.items()},
            "ell": ell,
            "value_present": value is not None,
        }
        rows.append(row)

    metadata = {
        "status": "SACC_ROW_METADATA_MATERIALIZED",
        "path": str(SACC_PATH),
        "row_count": len(rows),
        "rows": rows,
    }
    ROW_METADATA.write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata

def source_file_score(source_file: str, tracers: List[str]) -> int:
    normalized = normalize_token(source_file)
    score = 0
    for tracer in tracers:
        token = normalize_token(tracer)
        if token and token in normalized:
            score += 1
    return score

def construct_mapping(row_metadata: Dict[str, Any], combined_meta: Dict[str, Any], required_len: int) -> Dict[str, Any]:
    if row_metadata["status"] != "SACC_ROW_METADATA_MATERIALIZED":
        result = {
            "status": "ROW_MAPPING_BLOCKED_SACC_METADATA_UNAVAILABLE",
            "row_mapping": [],
            "failures": [row_metadata.get("missing_reason", row_metadata["status"])]
        }
        ROW_MAPPING.write_text(json.dumps(result, indent=2) + "\n")
        return result

    rows = row_metadata["rows"]
    if len(rows) != required_len:
        result = {
            "status": "ROW_MAPPING_BLOCKED_ROW_COUNT_MISMATCH",
            "row_mapping": [],
            "failures": [f"SACC row count {len(rows)} != required length {required_len}"]
        }
        ROW_MAPPING.write_text(json.dumps(result, indent=2) + "\n")
        return result

    table_rows = combined_meta["metadata_rows"]
    failures = []
    mapping = []

    for row in rows:
        target = int(row["target_index"])
        spectrum = row.get("spectrum_label")
        ell = row.get("ell")
        tracers = list(row.get("tracers", []))

        if spectrum is None:
            failures.append({"target_index": target, "reason": "cannot infer spectrum label", "row": row})
            continue
        if ell is None:
            failures.append({"target_index": target, "reason": "cannot infer scalar ell", "row": row})
            continue

        col = COLUMN_MAP.get(str(spectrum))
        if col is None:
            failures.append({"target_index": target, "reason": f"unsupported spectrum {spectrum}", "row": row})
            continue

        ell_matches = [
            item for item in table_rows
            if abs(float(item["ell"]) - float(ell)) < 1e-9
        ]

        if not ell_matches:
            failures.append({"target_index": target, "reason": f"no best-fit ell match for ell={ell}", "row": row})
            continue

        scored = sorted(
            [(source_file_score(str(item["source_file"]), tracers), item) for item in ell_matches],
            key=lambda x: (-x[0], str(x[1]["source_file"]), int(x[1]["local_row"]))
        )

        if not scored or scored[0][0] <= 0:
            failures.append({"target_index": target, "reason": "no tracer-matched best-fit source file", "row": row})
            continue

        if len(scored) > 1 and scored[1][0] == scored[0][0]:
            failures.append({
                "target_index": target,
                "reason": "ambiguous best-fit source file match",
                "top_score": scored[0][0],
                "candidates": [x[1]["source_file"] for x in scored[:5]],
                "row": row
            })
            continue

        best = scored[0][1]
        mapping.append({
            "target_index": target,
            "source_row": int(best["global_row"]),
            "source_col": int(col),
            "observable_label": str(spectrum),
            "frequency_or_spectrum_label": "__".join(tracers),
            "ell": ell,
            "source_file": best["source_file"],
            "source_local_row": int(best["local_row"]),
        })

    if failures:
        status = "ROW_MAPPING_BLOCKED_UNCERTIFIED_SACC_TO_BEST_FIT_MATCH"
    elif len(mapping) == required_len:
        status = "ROW_MAPPING_CONSTRUCTED_EXPLICIT_FULL_COVERAGE"
    else:
        status = "ROW_MAPPING_BLOCKED_INCOMPLETE_COVERAGE"
        failures.append(f"mapping length {len(mapping)} != required length {required_len}")

    result = {
        "status": status,
        "source": "official ACT DR6.02 LCDM best-fit tarball plus ACT DR6 CMB-only SACC row metadata",
        "mapping_file": str(ROW_MAPPING),
        "combined_table": str(COMBINED_TABLE),
        "combined_table_metadata": str(COMBINED_META),
        "official_best_fit_tar_sha256": sha256_file(TAR_PATH),
        "ordering_certificate": str(ORDER),
        "row_mapping": mapping,
        "failure_count": len(failures),
        "failures": failures[:200],
        "failure_truncated": len(failures) > 200,
    }
    ROW_MAPPING.write_text(json.dumps(result, indent=2) + "\n")
    return result

def run_extraction_if_possible(mapping_result: Dict[str, Any]) -> Dict[str, Any]:
    if mapping_result["status"] != "ROW_MAPPING_CONSTRUCTED_EXPLICIT_FULL_COVERAGE":
        result = {
            "status": "EXTRACTION_NOT_RUN_ROW_MAPPING_NOT_CERTIFIED",
            "reason": mapping_result["status"],
            "candidate": None,
        }
        AUDIT.write_text(json.dumps(result, indent=2) + "\n")
        return result

    cmd = [
        "python3",
        str(HARNESS_SCRIPT),
        "--best-fit-file",
        str(COMBINED_TABLE),
        "--mapping",
        str(ROW_MAPPING),
        "--output",
        str(EXTRACTION_CANDIDATE),
    ]
    import subprocess
    completed = subprocess.run(cmd, text=True, capture_output=True)

    if completed.returncode != 0:
        result = {
            "status": "EXTRACTION_FAILED",
            "cmd": cmd,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "candidate": None,
        }
        AUDIT.write_text(json.dumps(result, indent=2) + "\n")
        return result

    candidate = json.loads(EXTRACTION_CANDIDATE.read_text())
    result = {
        "status": "EXTRACTION_RAN_CANDIDATE_READY_FOR_ROW_ORDER_AUDIT",
        "cmd": cmd,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "candidate_path": str(EXTRACTION_CANDIDATE),
        "candidate_status": candidate["status"],
        "candidate_shape": candidate["vector_shape"],
        "candidate_sha256": candidate["vector_sha256"],
        "promotion_decision": candidate["promotion_decision"],
        "row_order_audit": "PASSED_EXPLICIT_MAPPING_FULL_COVERAGE" if candidate["vector_shape"] else "FAILED",
        "not_observed_data_vector_basis": candidate["not_observed_data_vector_basis"],
    }
    AUDIT.write_text(json.dumps(result, indent=2) + "\n")
    return result

def main() -> None:
    for p in [ORDER, ROW_TARGET, HARNESS_ART, HARNESS_SCRIPT]:
        if not p.exists():
            raise SystemExit(f"missing required input: {p}")

    order = json.loads(ORDER.read_text())
    row_target = json.loads(ROW_TARGET.read_text())
    required_shape = order["ordering_rule"]["required_prediction_vector_shape"]
    required_len = int(required_shape[0])

    official_tar = download_official_tar()
    extracted_members = safe_extract_tar()
    combined_meta = build_combined_table()
    sacc_metadata = load_sacc_metadata()
    mapping_result = construct_mapping(sacc_metadata, combined_meta, required_len)
    extraction_audit = run_extraction_if_possible(mapping_result)

    if mapping_result["status"] == "ROW_MAPPING_CONSTRUCTED_EXPLICIT_FULL_COVERAGE" and extraction_audit["status"] == "EXTRACTION_RAN_CANDIDATE_READY_FOR_ROW_ORDER_AUDIT":
        status = "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_RAN_VECTOR_CANDIDATE_NOT_PROMOTED"
        next_obj = "ACT_DR6_BASELINE_LCDM_EXTRACTED_VECTOR_ROW_ORDER_AUDIT"
    else:
        status = "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_BLOCKED_NO_CERTIFIED_ROW_MAPPING"
        next_obj = "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING"

    artifact = {
        "id": "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_2026_05_25",
        "status": status,
        "program": "DFM_MKC_DARK_SECTOR_VALIDATION",
        "depends_on": [
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_2026_05_25",
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS_2026_05_25",
            "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25"
        ],
        "official_best_fit_spectra_file": official_tar,
        "official_source_info_url": OFFICIAL_INFO_URL,
        "official_source_download_page": OFFICIAL_GET_URL,
        "extracted_member_count": len(extracted_members),
        "combined_numeric_table": str(COMBINED_TABLE),
        "combined_numeric_table_sha256": sha256_file(COMBINED_TABLE),
        "row_order_metadata": {
            "path": str(ROW_METADATA),
            "status": sacc_metadata["status"],
            "row_count": sacc_metadata.get("row_count", 0),
        },
        "row_mapping": {
            "path": str(ROW_MAPPING),
            "status": mapping_result["status"],
            "mapped_rows": len(mapping_result.get("row_mapping", [])),
            "failure_count": mapping_result.get("failure_count", None),
        },
        "extraction_audit": {
            "path": str(AUDIT),
            "status": extraction_audit["status"],
        },
        "row_order_mapping_target_status": row_target["status"],
        "required_prediction_vector_shape": required_shape,
        "promotion_decision": "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "allowed_next_object": next_obj,
        "still_missing_objects_after_this_trial": [
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR"
        ],
        "physical_dark_matter_phase_claim_status": "HYPOTHESIS_ONLY",
        "does_not_prove": [
            "baseline LCDM prediction vector exists",
            "baseline LCDM prediction vector has been promoted",
            "baseline LCDM prediction vector is fully row-audited",
            "baseline LCDM prediction vector is physically correct",
            "DFM-MKC prediction vector exists",
            "DFM-MKC prediction vector is correct",
            "ACT DR6 residual eigenspace empirical comparison has been run",
            "DFM-MKC empirical validation",
            "Lambda-CDM failure",
            "dark matter resolution",
            "dark energy resolution",
            "dark matter is liquid",
            "dark matter is solid",
            "dark matter phase transition is physically real",
            "ACT validation of DFM-MKC",
            "CMB validation of DFM-MKC",
            "independent empirical replication",
            "gravity closure",
            "Chronos-RR",
            "H4.1/FGL",
            "P vs NP",
            "any Clay problem"
        ]
    }

    ART.write_text(json.dumps(artifact, indent=2) + "\n")
    print("WROTE", ART)
    print(status)

if __name__ == "__main__":
    main()
