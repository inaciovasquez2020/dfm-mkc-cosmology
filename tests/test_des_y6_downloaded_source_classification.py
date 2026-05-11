import subprocess

def test_des_y6_downloaded_source_classification():
    subprocess.run(
        ["python3", "tools/verify_des_y6_downloaded_source_classification.py"],
        check=True,
    )
