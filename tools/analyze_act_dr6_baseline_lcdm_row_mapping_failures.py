#!/usr/bin/env python3
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

TRIAL_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial_2026_05_25.json")
MANIFEST = Path("artifacts/dfm_mkc/act_dr6_official_best_fits_dr6_lcdm_payload_manifest_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
SACC_PATH = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits")
ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_row_mapping_failure_analysis_2026_05_25.json")

SPECTRUM_KEYS = ["TT", "TE", "ET", "EE", "BB", "TB", "BT", "EB", "BE"]
ELL_KEYS = ["ell", "ells", "l", "lb", "leff", "ell_eff"]

def infer_spectrum_label(data_type: str) -> Optional[str]:
    text = data_type.lower()
    patterns = {
        "TT": ["tt", "cl_00"],
        "TE": ["te", "cl_0e"],
        "ET": ["et", "cl_e0"],
        "EE": ["ee", "cl_ee"],
        "BB": ["bb", "cl_bb"],
        "TB": ["tb", "cl_0b"],
        "BT": ["bt", "cl_b0"],
        "EB": ["eb", "cl_eb"],
        "BE": ["be", "cl_be"],
    }
    for label, tokens in patterns.items():
        if any(token in text for token in tokens):
            return label
    return None

def scalar_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        import numpy as np
        arr = np.asarray(value)
        if arr.size == 1:
            return float(arr.reshape(-1)[0])
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return None

def load_sacc_rows() -> Dict[str, Any]:
    if not SACC_PATH.exists():
        return {
            "status": "SACC_FILE_MISSING",
            "row_count": 0,
            "rows": [],
            "error": str(SACC_PATH),
        }

    try:
        import sacc  # type: ignore
    except Exception as exc:
        return {
            "status": "SACC_IMPORT_FAILED",
            "row_count": 0,
            "rows": [],
            "error": repr(exc),
        }

    try:
        s = sacc.Sacc.load_fits(str(SACC_PATH))
    except Exception as exc:
        return {
            "status": "SACC_LOAD_FAILED",
            "row_count": 0,
            "rows": [],
            "error": repr(exc),
        }

    rows: List[Dict[str, Any]] = []
    for i, dp in enumerate(getattr(s, "data", [])):
        tags = dict(getattr(dp, "tags", {}) or {})
        data_type = str(getattr(dp, "data_type", ""))
        tracers = [str(t) for t in list(getattr(dp, "tracers", []) or [])]

        ell = None
        ell_source_key = None
        for key in ELL_KEYS:
            if key in tags:
                ell = scalar_float(tags.get(key))
                if ell is not None:
                    ell_source_key = key
                    break

        spectrum = infer_spectrum_label(data_type)

        rows.append({
            "target_index": i,
            "data_type": data_type,
            "spectrum_label": spectrum,
            "tracers": tracers,
            "tag_keys": sorted(str(k) for k in tags),
            "ell": ell,
            "ell_source_key": ell_source_key,
            "has_required_spectrum": spectrum is not None,
            "has_scalar_ell": ell is not None,
            "has_tracers": bool(tracers),
        })

    return {
        "status": "SACC_ROW_METADATA_LOADED_FOR_FAILURE_ANALYSIS",
        "row_count": len(rows),
        "rows": rows,
        "error": None,
    }

def compact_rows(rows: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
    compact = []
    for row in rows[:limit]:
        compact.append({
            "target_index": row["target_index"],
            "data_type": row["data_type"],
            "spectrum_label": row["spectrum_label"],
            "tracers": row["tracers"],
            "ell": row["ell"],
            "tag_keys": row["tag_keys"][:20],
            "has_required_spectrum": row["has_required_spectrum"],
            "has_scalar_ell": row["has_scalar_ell"],
            "has_tracers": row["has_tracers"],
        })
    return compact

def main() -> None:
    for p in [TRIAL_ART, MANIFEST, ORDER]:
        if not p.exists():
            raise SystemExit(f"missing required input: {p}")

    trial = json.loads(TRIAL_ART.read_text())
    manifest = json.loads(MANIFEST.read_text())
    order = json.loads(ORDER.read_text())
    required_len = int(order["ordering_rule"]["required_prediction_vector_shape"][0])

    sacc = load_sacc_rows()
    rows = sacc["rows"]

    missing_spectrum = [r for r in rows if not r["has_required_spectrum"]]
    missing_ell = [r for r in rows if not r["has_scalar_ell"]]
    missing_tracers = [r for r in rows if not r["has_tracers"]]

    spectrum_counts = Counter(r["spectrum_label"] or "UNINFERRED" for r in rows)
    tag_key_counts = Counter(k for r in rows for k in r["tag_keys"])
    data_type_counts = Counter(r["data_type"] for r in rows)

    if sacc["status"] != "SACC_ROW_METADATA_LOADED_FOR_FAILURE_ANALYSIS":
        status = "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_SACC_METADATA_UNAVAILABLE"
        root_causes = [
            "ACT DR6 CMB-only SACC row metadata could not be loaded locally.",
            "Certified row_mapping cannot be constructed without target-row observable metadata."
        ]
    elif len(rows) != required_len:
        status = "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_ROW_COUNT_MISMATCH"
        root_causes = [
            f"SACC row count {len(rows)} does not match certified required vector length {required_len}."
        ]
    elif missing_spectrum or missing_ell or missing_tracers:
        status = "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_INCOMPLETE_SACC_ROW_METADATA"
        root_causes = [
            "At least one target row lacks an inferable spectrum label, scalar ell, or tracer metadata.",
            "A total explicit mapping from best-fit spectra table rows to every certified ACT DR6 target row cannot be certified."
        ]
    else:
        status = "ROW_MAPPING_FAILURE_ANALYSIS_LOCAL_SACC_METADATA_SUFFICIENT_MAPPING_ALGORITHM_STILL_OPEN"
        root_causes = [
            "Local SACC target rows expose spectrum, ell, and tracer metadata.",
            "Remaining blocker is the matching algorithm from ACT tracer/bin labels to official best-fit source-file labels."
        ]

    artifact = {
        "id": "ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS_2026_05_25",
        "status": status,
        "program": "DFM_MKC_DARK_SECTOR_VALIDATION",
        "depends_on": [
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_2026_05_25",
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_2026_05_25",
            "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25"
        ],
        "target_missing_object": "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
        "ultimate_target_missing_object": "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "trial_status": trial["status"],
        "payload_manifest_status": manifest["status"],
        "required_prediction_vector_shape": order["ordering_rule"]["required_prediction_vector_shape"],
        "sacc_metadata_status": sacc["status"],
        "sacc_error": sacc["error"],
        "row_count": len(rows),
        "required_row_count": required_len,
        "failure_counts": {
            "missing_spectrum_label": len(missing_spectrum),
            "missing_scalar_ell": len(missing_ell),
            "missing_tracers": len(missing_tracers),
        },
        "spectrum_counts": dict(sorted(spectrum_counts.items())),
        "top_tag_keys": dict(tag_key_counts.most_common(50)),
        "top_data_types": dict(data_type_counts.most_common(50)),
        "sample_missing_spectrum_rows": compact_rows(missing_spectrum),
        "sample_missing_ell_rows": compact_rows(missing_ell),
        "sample_missing_tracer_rows": compact_rows(missing_tracers),
        "root_causes": root_causes,
        "minimal_next_object": {
            "id": "ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE",
            "status": "MISSING",
            "role": "A deterministic rule binding ACT DR6 SACC row labels/tracers/ell bins to NASA LAMBDA best-fit source files and columns."
        },
        "blocked_until": [
            "SACC row metadata supplies or is supplemented with spectrum labels, ell/bin labels, and tracer labels for every target row",
            "best-fit source-file labels are normalized against SACC tracer labels",
            "each target row receives exactly one source_row/source_col assignment",
            "the mapping is independently audited against ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE"
        ],
        "allowed_next_status_after_binding_rule": "ROW_MAPPING_BINDING_RULE_READY_FOR_MAPPING_CONSTRUCTION",
        "promotion_decision": "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "still_missing_objects_after_this_analysis": [
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR"
        ],
        "physical_dark_matter_phase_claim_status": "HYPOTHESIS_ONLY",
        "does_not_prove": [
            "official best-fit row-order mapping exists",
            "baseline LCDM prediction vector exists",
            "baseline LCDM prediction vector has been extracted",
            "baseline LCDM prediction vector is row-aligned",
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
