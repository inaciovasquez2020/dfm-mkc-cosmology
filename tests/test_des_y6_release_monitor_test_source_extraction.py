import subprocess

def test_des_y6_release_monitor_test_source_extraction():
    subprocess.run(
        ["python3", "tools/verify_des_y6_release_monitor_test_source_extraction.py"],
        check=True,
    )
