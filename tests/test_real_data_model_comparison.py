from src.data.load_public_cosmology_data import dataset_status

def test_dataset_status_shape():
    s = dataset_status()
    assert set(s.keys()) == {"desi_dr2", "des_y6", "planck"}
    assert all("present" in v and "missing" in v for v in s.values())
    assert all(v["present"] is False for v in s.values())
    assert any(v["missing"] for v in s.values())
