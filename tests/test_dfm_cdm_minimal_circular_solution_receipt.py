import subprocess


def test_dfm_cdm_minimal_circular_solution_receipt():
    result = subprocess.run(
        [
            "python3",
            "-B",
            "tools/verify_dfm_cdm_minimal_circular_solution_receipt.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_OK"
        in result.stdout
    )
