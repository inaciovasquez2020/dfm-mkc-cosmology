#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "artifacts/status/zero_day_falsification_interface_receipt_2026_07_06.json"

REQUIRED_TOKENS = [
    "ZeroDayFalsificationInterfaceReceipt",
    "external_interface_only",
    "zero_day_restricted_closures",
    "DFM_MKC_formula_to_observable_map",
    "DESI_DR2_BAO_DFM_MKC_Test",
    "PantheonPlus_DFM_MKC_HubbleDiagram_Test",
    "DFM_MKC_FORMULA_SURFACE_FOUND_BUT_NO_ZD_CLOSURE_DERIVED",
    "does not prove a DFM-MKC cosmology theorem",
    "does not validate cosmology empirically",
    "does not reject Lambda-CDM",
    "does not independently reproduce DESI DR2 likelihoods",
    "does not independently reproduce PantheonPlus likelihoods",
]

def main() -> int:
    if not RECEIPT.exists():
        print(f"MISSING_OBJECT := {RECEIPT.relative_to(ROOT)}")
        return 1

    text = RECEIPT.read_text(encoding="utf-8")
    for token in REQUIRED_TOKENS:
        if token not in text:
            print(f"ZERO_DAY_FALSIFICATION_INTERFACE_RECEIPT_FAIL missing token: {token}")
            return 1

    data = json.loads(text)
    if data.get("status") != "external_interface_only":
        print("ZERO_DAY_FALSIFICATION_INTERFACE_RECEIPT_FAIL status")
        return 1

    non_claims = data.get("non_claims", [])
    forbidden_claims = [
        "validates cosmology empirically",
        "rejects Lambda-CDM",
        "proves a DFM-MKC cosmology theorem",
        "proves ZeroDayClosure",
        "proves unrestricted ZeroDayClosure",
    ]
    joined_non_claims = "\n".join(non_claims)
    for claim in forbidden_claims:
        if claim in text and claim not in joined_non_claims:
            print(f"ZERO_DAY_FALSIFICATION_INTERFACE_RECEIPT_FAIL forbidden claim escaped non_claims: {claim}")
            return 1

    print("ZERO_DAY_FALSIFICATION_INTERFACE_RECEIPT_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
