import subprocess

def test_des_y6_validation_boundary():
    subprocess.run(
        ["python3", "tools/verify_des_y6_validation_boundary.py"],
        check=True,
    )
