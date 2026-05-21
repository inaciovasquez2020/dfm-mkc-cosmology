from pathlib import Path
import json

artifact = Path("artifacts/des_y6_release_monitor/test_source_extraction_2026_05_21.json")
doc = Path("docs/status/DES_Y6_RELEASE_MONITOR_TEST_SOURCE_EXTRACTION_2026_05_21.md")

data = json.loads(artifact.read_text())
text = doc.read_text()

assert data["status"] == "PRIVATE_REPO_TEST_SOURCE_CAPTURED"
assert data["source"] == "tests/test_des_y6_release_monitor.py"
assert data["files"]["test_file"]["exists"] is True
assert data["files"]["test_file"]["sha256"]
assert "no DES Y6 authentic release ingestion claim" in data["boundary"]
assert "no theorem-level URF cosmology closure claim" in data["boundary"]

for token in [
    "PRIVATE_REPO_TEST_SOURCE_CAPTURED",
    "tests/test_des_y6_release_monitor.py",
    "artifacts/des_y6_release_monitor/test_source_extraction_2026_05_21.json",
    "no DES Y6 authentic release ingestion claim",
    "no theorem-level URF cosmology closure claim",
]:
    assert token in text, token

print("DES Y6 release monitor test source extraction verified.")
