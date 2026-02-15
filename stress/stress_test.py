import time
import random
def run_once():
x = random.random()
y = random.random()
z = x * x + y * y
return {
"x": x,
"y": y,
"z": z,
}
def test_stress_runs():
start = time.time()
results = []
for _ in range(100):
results.append(run_once())
duration = time.time() - startassert len(results) == 100
assert duration < 5.0
for r in results:
    assert "z" in r
    assert r["z"] >= 0.0
