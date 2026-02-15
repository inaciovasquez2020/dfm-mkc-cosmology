import time
import random

def run_once():
    x = random.random()
    return {"z": x}

def test_stress_runs():
    start = time.time()
    results = []
    for _ in range(100):
        results.append(run_once())
    duration = time.time() - start

    assert len(results) == 100
    assert duration < 5.0

    for r in results:
        assert "z" in r
        assert r["z"] >= 0.0
