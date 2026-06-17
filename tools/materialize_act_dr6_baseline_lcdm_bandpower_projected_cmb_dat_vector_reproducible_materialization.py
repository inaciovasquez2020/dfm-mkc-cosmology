import hashlib
import json
import shutil
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import sacc

CANDIDATE = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_candidate_2026_06_17.json")
OUT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_reproducible_materialization_2026_06_17.json")

WORK = Path("/tmp/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_reproducible_materialization_20260617")
TAR = WORK / "act_dr6.02_best_fits_dr6_lcdm.tar.gz"
EXTRACTED = WORK / "extracted"

TOL = 1e-9


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(tar: tarfile.TarFile, target: Path) -> None:
    target_resolved = target.resolve()
    for member in tar.getmembers():
        dest = (target / member.name).resolve()
        if not str(dest).startswith(str(target_resolved)):
            raise RuntimeError(f"unsafe tar member: {member.name}")
    tar.extractall(target)


def canonical_decimal_sha(vec: np.ndarray) -> str:
    payload = json.dumps([format(float(x), ".12g") for x in vec], separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def materialize_payload(candidate: dict) -> Path:
    if WORK.exists():
        shutil.rmtree(WORK)
    EXTRACTED.mkdir(parents=True)

    urllib.request.urlretrieve(candidate["source_theory_parent_payload"], TAR)

    with tarfile.open(TAR, "r:gz") as tar:
        safe_extract(tar, EXTRACTED)

    cmb = next(EXTRACTED.rglob("cmb.dat"))
    cmb_sha = sha256_file(cmb)
    if cmb_sha != candidate["source_theory_file_sha256"]:
        raise AssertionError(f"cmb.dat sha mismatch: {cmb_sha}")

    return cmb


def main() -> None:
    candidate = json.loads(CANDIDATE.read_text())
    cmb = materialize_payload(candidate)

    s = sacc.Sacc.load_fits(candidate["source_sacc_path"])
    theory_table = np.loadtxt(cmb, comments="#")

    assert theory_table.shape == (8998, 10)
    assert len(s.data) == candidate["sacc_row_count"]

    ell = theory_table[:, 0].astype(int)
    parts = []
    block_records = []
    max_sample_abs_diff = 0.0

    sample_key_by_type = {
        "cl_00": "cl_00_head",
        "cl_0e": "cl_0e_head",
        "cl_ee": "cl_ee_head",
    }

    for block in candidate["projection_rule"]["blocks"]:
        start, end = block["target_index_range"]
        typ = block["data_type"]
        col = block["source_col"]

        dp = s.data[start]
        window = dict(dp.tags)["window"]

        assert dp.data_type == typ
        assert list(dp.tracers) == block["tracers"]
        assert end - start + 1 == 45
        assert int(window.nv) == 45
        assert int(window.nell) == 8500

        values = np.asarray(window.values).astype(int)
        weights = np.asarray(window.weight, dtype=np.float64)

        assert values.shape == (8500,)
        assert weights.shape == (8500, 45)

        idx = np.searchsorted(ell, values)
        assert np.all(ell[idx] == values)

        theory = np.asarray(theory_table[idx, col], dtype=np.float64)

        # Use explicit sum, not BLAS matmul, to avoid raw-byte instability from summation order.
        band = np.sum(weights * theory[:, None], axis=0, dtype=np.float64)

        assert band.shape == (45,)
        assert np.isfinite(band).all()

        candidate_head = np.asarray(candidate["sample_outputs"][sample_key_by_type[typ]], dtype=np.float64)
        sample_abs_diff = float(np.max(np.abs(band[:5] - candidate_head)))
        max_sample_abs_diff = max(max_sample_abs_diff, sample_abs_diff)
        assert sample_abs_diff <= TOL, (typ, sample_abs_diff)

        parts.append(band)
        block_records.append({
            "data_type": typ,
            "target_index_range": [start, end],
            "source_col": col,
            "source_column_label": block["source_column_label"],
            "computed_shape": [45],
            "head": band[:5].tolist(),
            "tail": band[-5:].tolist(),
            "max_abs_diff_against_candidate_head": sample_abs_diff,
        })

    vec = np.ascontiguousarray(np.concatenate(parts), dtype=np.float64)
    raw_sha = hashlib.sha256(vec.tobytes()).hexdigest()
    canonical_sha = canonical_decimal_sha(vec)

    out = {
        "id": "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION_2026_06_17",
        "status": "REPRODUCIBLE_MATERIALIZATION_NUMERIC_TOLERANCE_PASSED_RAW_BYTE_SHA_UNSTABLE_CANDIDATE_STILL_NOT_PROMOTED",
        "program": "DFM_MKC_DARK_SECTOR_VALIDATION",
        "created_utc_date": "2026-06-17",
        "materializes_candidate": candidate["id"],
        "candidate_artifact": str(CANDIDATE),
        "source_sacc_path": candidate["source_sacc_path"],
        "source_theory_file": candidate["source_theory_file"],
        "source_theory_file_sha256": candidate["source_theory_file_sha256"],
        "ordering_certificate_id": candidate["ordering_certificate_id"],
        "computed_shape": [135],
        "computed_finite": True,
        "numeric_tolerance": TOL,
        "max_abs_diff_against_candidate_samples": max_sample_abs_diff,
        "candidate_raw_byte_sha256": candidate["candidate_sha256_input_only_not_artifact"],
        "observed_raw_byte_sha256": raw_sha,
        "raw_byte_sha256_match": raw_sha == candidate["candidate_sha256_input_only_not_artifact"],
        "canonical_decimal_sha256": canonical_sha,
        "canonical_decimal_precision": ".12g",
        "projection_operation": "sum(window.weight * cmb.dat source column over ell values 2..8501, axis=0)",
        "blocks": block_records,
        "promotion_decision": "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "next_required_validation": "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_OFFICIAL_CONVENTION_AUDIT",
        "does_not_prove": candidate["does_not_prove"],
    }

    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print("ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION_WRITTEN")
    print("RAW_SHA_MATCH :=", out["raw_byte_sha256_match"])
    print("MAX_ABS_DIFF_AGAINST_CANDIDATE_SAMPLES :=", max_sample_abs_diff)
    print("CANONICAL_DECIMAL_SHA256 :=", canonical_sha)


if __name__ == "__main__":
    main()
