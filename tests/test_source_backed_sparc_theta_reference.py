import json
from pathlib import Path

ARTIFACT = Path("artifacts/cross_repo/source_backed_sparc_theta_test_2026_06_04.json")
STATUS_DOC = Path("docs/status/SOURCE_BACKED_SPARC_THETA_TEST_REFERENCE_2026_06_04.md")

def test_reference_artifact_exists():
    assert ARTIFACT.exists()

def test_reference_status_doc_exists():
    assert STATUS_DOC.exists()

def test_reference_classification():
    data = json.loads(ARTIFACT.read_text())
    assert data["classification"] == "SourceBackedNegativeBoundaryArtifact"
    assert data["source_version"] == "v0.1.0"

def test_reference_forbids_overclaim():
    data = json.loads(ARTIFACT.read_text())
    not_closed = set(data["not_closed_as"])
    assert "DarkMatterSolution" in not_closed
    assert "EmpiricalGravityValidation" in not_closed
    assert "TheoremClosure" in not_closed
