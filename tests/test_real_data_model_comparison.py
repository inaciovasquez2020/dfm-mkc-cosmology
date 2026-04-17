from src.data.load_public_cosmology_data import dataset_status

def test_dataset_status_shape():
    s = dataset_status()
    assert set(s.keys()) == {"desi_dr2", "des_y6", "planck"}
    assert all("present" in v and "missing" in v and "synthetic_present" in v and "synthetic_files" in v for v in s.values())
    assert all(isinstance(v["present"], bool) for v in s.values())
    assert all(isinstance(v["synthetic_present"], bool) for v in s.values())
    assert all(v["missing"] == [] for v in s.values())
    assert all(isinstance(v["synthetic_files"], list) for v in s.values())
