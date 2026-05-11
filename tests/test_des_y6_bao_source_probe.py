import subprocess

def test_des_y6_bao_source_probe():
    subprocess.run(
        ["python3", "tools/verify_des_y6_bao_source_probe.py"],
        check=True,
    )
