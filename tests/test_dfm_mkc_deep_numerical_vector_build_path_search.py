import subprocess
import sys

def test_dfm_mkc_deep_numerical_vector_build_path_search():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_deep_numerical_vector_build_path_search.py"],
        check=True,
    )
