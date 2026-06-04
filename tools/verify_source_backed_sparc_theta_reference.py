#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/cross_repo/source_backed_sparc_theta_test_2026_06_04.json")

def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "SourceBackedSPARCThetaTestReference"
    assert data["source_version"] == "v0.1.0"
    assert data["classification"] == "SourceBackedNegativeBoundaryArtifact"

    not_closed = set(data["not_closed_as"])
    required = {
        "DarkMatterSolution",
        "ThetaAsDarkMatterSolutionUnderCurrentTestedLaws",
        "EmpiricalGravityValidation",
        "SPARCPredictiveSuccess",
        "DFM_MKCSupport",
        "TheoremClosure",
    }
    assert required <= not_closed

    assert "repository preservation" in data["safe_statement"]
    assert "not a dark-matter or gravity claim" in data["safe_statement"]

    print("SOURCE_BACKED_SPARC_THETA_REFERENCE_OK")
    print("STATUS=SOURCE_BACKED_SPARC_THETA_TEST_REFERENCE_RECORDED")
    print("CLASSIFICATION=SourceBackedNegativeBoundaryArtifact")
    print("NEXT_ADMISSIBLE_OBJECT=Stop")

if __name__ == "__main__":
    main()
