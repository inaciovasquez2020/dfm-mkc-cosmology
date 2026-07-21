"""Provenance gate for physical cosmological calibration.

The existing Planck table is not labelled synthetic, but its README does not
bind it to an immutable release identifier or a declared checksum. This gate
therefore rejects it as a physical calibration input without asserting that
the table itself is synthetic.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PhysicalCalibrationProvenanceCertificate:
    parameter_table_sha256: str
    declared_sha256: str | None
    source_name_documented: bool
    source_page_documented: bool
    immutable_source_identifier_documented: bool
    declared_sha256_matches: bool
    parameter_freeze_loaded: bool
    parameter_rules_frozen: bool
    authentic_parameter_table: bool
    physical_calibration_input_ready: bool
    missing_objects: tuple[str, ...]
    natural_unit_mapping_derived: bool
    calibrated_initial_conditions_derived: bool
    calibrated_dfm_parameters_derived: bool
    observational_likelihood_completed: bool


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _field_present(text: str, field: str) -> bool:
    return (
        re.search(
            rf"(?im)^\s*{re.escape(field)}\s*:\s*\S",
            text,
        )
        is not None
    )


def _declared_sha256(text: str) -> str | None:
    match = re.search(
        r"(?im)^\s*sha256\s*:\s*([0-9a-f]{64})\s*$",
        text,
    )
    return None if match is None else match.group(1).lower()


def inspect_physical_calibration_provenance(
    repository_root: str | Path,
) -> PhysicalCalibrationProvenanceCertificate:
    root = Path(repository_root).resolve()

    table = (
        root
        / "public_data"
        / "planck"
        / "planck_2018_baseline_params.csv"
    )
    readme = root / "public_data" / "planck" / "README.md"
    freeze = root / "config" / "dfm_mkc_parameter_freeze.json"

    for path in (table, readme, freeze):
        if not path.is_file():
            raise ValueError(f"MISSING_OBJECT := {path}")

    readme_text = readme.read_text()
    freeze_payload = json.loads(freeze.read_text())

    if not isinstance(freeze_payload, dict):
        raise ValueError(
            "MISSING_OBJECT := JSON-object parameter freeze"
        )

    table_sha256 = _sha256(table)
    declared_sha256 = _declared_sha256(readme_text)

    source_name_documented = _field_present(
        readme_text,
        "source_name",
    )
    source_page_documented = any(
        _field_present(readme_text, field)
        for field in ("source_page", "data_landing_page")
    )
    immutable_source_identifier_documented = any(
        _field_present(readme_text, field)
        for field in (
            "doi",
            "release_id",
            "archive_record",
            "source_version",
        )
    )

    declared_sha256_matches = (
        declared_sha256 is not None
        and declared_sha256 == table_sha256
    )

    parameter_freeze_loaded = (
        freeze_payload.get("model") == "DFM-MKC"
        and isinstance(
            freeze_payload.get("fitting_policy"),
            str,
        )
        and bool(freeze_payload["fitting_policy"].strip())
    )

    freeze_status = freeze_payload.get("status")
    parameter_rules_frozen = (
        isinstance(freeze_status, str)
        and freeze_status.startswith("PARAMETER_RULES_FROZEN")
    )

    authentic_parameter_table = (
        source_name_documented
        and source_page_documented
        and immutable_source_identifier_documented
        and declared_sha256_matches
    )

    missing_objects: list[str] = []

    if not source_name_documented:
        missing_objects.append("documented source name")

    if not source_page_documented:
        missing_objects.append("documented source page")

    if not immutable_source_identifier_documented:
        missing_objects.append(
            "immutable Planck release identifier"
        )

    if declared_sha256 is None:
        missing_objects.append(
            "declared SHA-256 for the Planck parameter table"
        )
    elif not declared_sha256_matches:
        missing_objects.append(
            "matching SHA-256 for the Planck parameter table"
        )

    if not parameter_freeze_loaded:
        missing_objects.append(
            "valid DFM-MKC parameter-freeze record"
        )

    if not parameter_rules_frozen:
        missing_objects.append(
            "active parameter-freeze status"
        )

    ready = (
        authentic_parameter_table
        and parameter_freeze_loaded
        and parameter_rules_frozen
    )

    return PhysicalCalibrationProvenanceCertificate(
        parameter_table_sha256=table_sha256,
        declared_sha256=declared_sha256,
        source_name_documented=source_name_documented,
        source_page_documented=source_page_documented,
        immutable_source_identifier_documented=(
            immutable_source_identifier_documented
        ),
        declared_sha256_matches=declared_sha256_matches,
        parameter_freeze_loaded=parameter_freeze_loaded,
        parameter_rules_frozen=parameter_rules_frozen,
        authentic_parameter_table=authentic_parameter_table,
        physical_calibration_input_ready=ready,
        missing_objects=tuple(missing_objects),
        natural_unit_mapping_derived=False,
        calibrated_initial_conditions_derived=False,
        calibrated_dfm_parameters_derived=False,
        observational_likelihood_completed=False,
    )


def require_physical_calibration_input(
    repository_root: str | Path,
) -> PhysicalCalibrationProvenanceCertificate:
    certificate = inspect_physical_calibration_provenance(
        repository_root
    )

    if not certificate.physical_calibration_input_ready:
        raise ValueError(
            "MISSING_OBJECT := provenance-bearing physical "
            "calibration input; gaps="
            + "; ".join(certificate.missing_objects)
        )

    return certificate
