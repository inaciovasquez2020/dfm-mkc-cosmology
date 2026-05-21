from pathlib import Path
import subprocess

WORKFLOW = Path(".github/workflows/des-y6-release-monitor.yml")
MONITOR = Path("tools/check_des_y6_release_monitor.py")

def test_des_y6_release_monitor_workflow_exists():
    assert WORKFLOW.exists()
    text = WORKFLOW.read_text()
    assert "DES Y6 Release Monitor" in text
    assert "workflow_dispatch:" in text
    assert 'cron: "17 12 * * 1"' in text
    assert "tools/check_des_y6_release_monitor.py" in text
    assert "artifacts/des_y6_release_monitor/latest.json" in text

def test_des_y6_release_monitor_tool_exists():
    assert MONITOR.exists()

def test_des_y6_release_monitor_runs_locally(tmp_path):
    out = tmp_path / "latest.json"
    subprocess.run(
        ["python3", str(MONITOR), "--output", str(out)],
        check=True,
    )
    assert out.exists()
