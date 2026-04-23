from pathlib import Path

FILES = [
    Path("public_data/des_y6/y6_3x2pt_summary.csv"),
    Path("public_data/des_y6/y6_covariance.csv"),
]

BAD_TOKENS = ("<html", "404 not found", "<body", "<center>", "nginx")

def test_des_y6_files_are_authentic():
    for path in FILES:
        text = path.read_text(errors="ignore")
        low = text.lower()
        assert not any(tok in low for tok in BAD_TOKENS), f"{path} is placeholder HTML"
        assert "," in text.splitlines()[0], f"{path} is not CSV-shaped"
        assert len(text.splitlines()) >= 2, f"{path} is missing data rows"
