import subprocess


def test_dfm_mkc_external_cosmology_information_rank():
    subprocess.run(
        [
            "python3",
            "-B",
            "tools/verify_dfm_mkc_external_cosmology_information_rank.py",
        ],
        check=True,
    )
