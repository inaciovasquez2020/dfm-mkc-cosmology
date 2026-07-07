#!/usr/bin/env python3
import json
from pathlib import Path


receipt_path = Path("artifacts/status/sidfh_repository_route_receipt_2026_07_07.json")
receipt = json.loads(receipt_path.read_text())

required = {
    "receipt": "sidfh_repository_route_receipt_2026_07_07",
    "core_name": "SIDFH",
    "expanded_name": "Shadow of Infinity Dark Front Hypothesis",
    "primary_repo": "inaciovasquez2020/dfm-mkc-cosmology",
    "boundary": "BOUNDARY := ¬ current_work_proves_universal_physical_minimum_nonzero_speed",
}

for key, value in required.items():
    assert receipt.get(key) == value, f"{key} mismatch"

related = receipt.get("related_repos", {})
for repo in ["dfm-mkc-cosmology", "chronos-urf-rr", "urf-core", "urf-textbook"]:
    assert repo in related, f"missing related repo: {repo}"

classification = receipt.get("classification", {})
assert classification.get("sidfh_new_physics_proved") is False
assert classification.get("sidfh_independent_math_proved") is False
assert classification.get("sidfh_reduction_surface_supported") is True
assert classification.get("v_min_physical_derivation_proved") is False
assert classification.get("motion_band_shadow_status") == "bounded relation only"

forbidden = set(receipt.get("forbidden_claims", []))
for claim in [
    "SIDFH proves new cosmology",
    "SIDFH proves dark matter",
    "SIDFH proves a universal physical minimum nonzero speed",
    "SIDFH derives v_min from physical first principles",
    "MotionBandShadow proves a universal physical minimum nonzero speed",
    "ShadowOfInfinity implies physical time dilation",
]:
    assert claim in forbidden, f"missing forbidden claim: {claim}"

objects = set(receipt.get("core_objects", []))
assert "SIDFHTachSpeedInputSurface" in objects
assert "MotionBandShadow(V,c,v) := V < v ∧ v < c" in objects
assert "dark_front(t)" in objects

print("SIDFH_REPOSITORY_ROUTE_RECEIPT_OK")
