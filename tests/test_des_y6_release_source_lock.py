import subprocess

def test_des_y6_release_source_lock():
    subprocess.run(
        ["python3", "tools/verify_des_y6_release_source_lock.py"],
        check=True,
    )
