#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_sacc_reader_and_independent_release_hash_validation_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_public_release_digest_and_full_sacc_schema_reader_2026_05_22.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_fits_headers(path: Path):
    headers = []
    if not path.exists() or not path.is_file():
        return headers

    with path.open("rb") as f:
        while True:
            block = f.read(2880)
            if not block:
                break
            if len(block) < 2880:
                break

            cards = [block[i:i+80].decode("ascii", errors="ignore") for i in range(0, 2880, 80)]
            if not cards or not (cards[0].startswith("SIMPLE") or cards[0].startswith("XTENSION")):
                break

            header_cards = cards[:]
            while not any(card.startswith("END") for card in header_cards):
                block = f.read(2880)
                if not block or len(block) < 2880:
                    break
                more = [block[i:i+80].decode("ascii", errors="ignore") for i in range(0, 2880, 80)]
                header_cards.extend(more)
                if any(card.startswith("END") for card in more):
                    break

            parsed = {}
            for card in header_cards:
                if "=" in card[:10]:
                    key = card[:8].strip()
                    value = card[10:80].split("/")[0].strip().strip("'")
                    parsed[key] = value

            headers.append({
                "index": len(headers),
                "kind": "PRIMARY" if "SIMPLE" in parsed else parsed.get("XTENSION", "UNKNOWN"),
                "extname": parsed.get("EXTNAME"),
                "naxis": parsed.get("NAXIS"),
                "cards_observed": len(header_cards),
            })

            try:
                bitpix = abs(int(parsed.get("BITPIX", "0")))
                naxis = int(parsed.get("NAXIS", "0"))
                size = 0
                if naxis > 0:
                    size = bitpix // 8
                    for i in range(1, naxis + 1):
                        size *= int(parsed.get(f"NAXIS{i}", "0"))
                pcount = int(parsed.get("PCOUNT", "0"))
                gcount = int(parsed.get("GCOUNT", "1"))
                data_size = (size + pcount) * max(gcount, 1)
                padding = (2880 - (data_size % 2880)) % 2880
                f.seek(data_size + padding, 1)
            except Exception:
                break

    return headers

def main():
    source = json.loads(SOURCE.read_text())
    path = ROOT / source["local_path"]
    headers = read_fits_headers(path)
    extnames = sorted({h["extname"] for h in headers if h.get("extname")})

    artifact = {
        "object": "ACT_DR6_PUBLIC_RELEASE_DIGEST_AND_FULL_SACC_SCHEMA_READER",
        "date": "2026-05-22",
        "status": "LOCAL_FITS_HEADER_ENUMERATOR_ONLY_PUBLIC_DIGEST_AND_FULL_SACC_SCHEMA_OPEN",
        "source_object": source["object"],
        "input_key": "act_dr6_cmb_lite",
        "local_path": source["local_path"],
        "local_payload": {
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
            "fits_hdu_headers_observed": len(headers),
            "fits_extnames_observed": extnames,
        },
        "reader": {
            "name": "LOCAL_FITS_HEADER_ENUMERATOR",
            "executes_on_local_payload": bool(headers),
            "full_sacc_schema_reader_implemented": False,
            "full_sacc_schema_validation_passed": False,
        },
        "public_release_digest": {
            "external_release_url_or_doi": None,
            "external_release_digest": None,
            "independent_hash_match_verified": False,
            "release_provenance_certified": False,
        },
        "certified_for_profiled_likelihood_execution": False,
        "required_next_object": "ACT_DR6_EXTERNAL_RELEASE_REFERENCE_AND_SACC_SCHEMA_CONFORMANCE_RULES",
        "does_not_prove": [
            "ACT DR6 public release digest certification",
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

if __name__ == "__main__":
    main()
