import time, statistics

eval_count = 0
error_count = 0
timings = []

def record(fn):
def wrapped(*args, **kwargs):
global eval_count, error_count, timings
start = time.time()
try:
return fn(*args, **kwargs)
except Exception:
error_count += 1
raise
finally:
eval_count += 1
timings.append((time.time() - start) * 1000)
return wrapped

def report():
if timings:
print(f"EVAL_COUNT={eval_count}")
print(f"ERROR_COUNT={error_count}")
print(f"AVG_MS={statistics.mean(timings):.3f}")
print(f"MAX_MS={max(timings):.3f}")
else:
print("NO_EVALS")
