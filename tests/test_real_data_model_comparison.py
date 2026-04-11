from src.data.load_public_cosmology_data import dataset_status

def test_dataset_status_shape():
    s = dataset_status()
    assert set(s.keys()) == {"desi_dr2", "des_y6", "planck"}
    assert all("present" in v and "missing" in v and "synthetic_present" in v and "synthetic_files" in v for v in s.values())
    assert all(v["present"] is False for v in s.values())
    assert all(v["synthetic_present"] is True for v in s.values())
    assert all(v["missing"] == [] for v in s.values())
    assert all(len(v["synthetic_files"]) >= 1 for v in s.values())
