from pathlib import Path
import importlib.util
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_schema_acceptance_predicate_implementation_surface_2026_05_21.json")
PREDICATE_MODULE = Path("tools/dfm_mkc_schema_acceptance_predicates.py")

def load_predicates():
    spec = importlib.util.spec_from_file_location("dfm_mkc_schema_acceptance_predicates", PREDICATE_MODULE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def test_schema_acceptance_predicate_implementation_surface_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_schema_acceptance_predicate_implementation_surface.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC schema acceptance predicate implementation surface verification OK." in result.stdout
    assert "PREDICATE_IMPLEMENTATION_SURFACE_ONLY_NO_PAYLOAD_VALIDATION" in result.stdout

def test_predicate_registry_covers_exact_required_fields():
    predicates = load_predicates()
    assert tuple(predicates.REQUIRED_FIELDS) == (
        "data_vector",
        "covariance_matrix",
        "mask",
        "likelihood_rule",
        "statistical_threshold",
        "protocol_hash",
        "actdr6_release_date",
        "data_freeze_lock",
    )
    assert set(predicates.ACCEPTANCE_PREDICATES) == set(predicates.REQUIRED_FIELDS)

def test_rejects_missing_data_vector_predicate():
    predicates = load_predicates()
    result = predicates.accept_data_vector({
        "field": "data_vector",
        "source": "protocol_approved_data_vector_source",
        "kind": "one_dimensional_numeric_array",
        "nonempty": True,
        "finite_real_entries": False,
        "length_equals_mask_length": True,
        "length_equals_covariance_row_count": True,
        "freeze_lock_covered": True,
    })
    assert not result.accepted
    assert "all entries are finite real numbers" in result.missing_predicates

def test_artifact_preserves_boundary_and_nonclaims():
    data = json.loads(ARTIFACT.read_text())
    assert data["hard_blocker"] == "schema validation remains blocked"
    assert "implementation surface only" in data["boundary"]
    assert "does not validate authentic ACT DR6 payload bytes" in data["boundary"]
    assert "does not promote any empirical slot" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
