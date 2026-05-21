import subprocess

def test_dfm_mkc_theory_content_digest():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_theory_content_digest.py"],
        check=True,
    )
