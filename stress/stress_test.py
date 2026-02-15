import random
from stress.counters import record, report
from scripts.cosmology import run_model

run = record(run_model)

def random_params():
return {
"omega_m": random.uniform(0.1, 0.5),
"sigma8": random.uniform(0.7, 0.9),
"hubble": random.uniform(0.65, 0.75),
}

for _ in range(1000):
run(random_params())

report()
