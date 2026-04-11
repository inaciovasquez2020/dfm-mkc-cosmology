import csv
from src.data.load_public_cosmology_data import dataset_status

FIELDNAMES = ["model","logL","AIC","BIC","H0_mean","Omega_m_mean","status"]

def placeholder_status(summary: dict[str, dict[str, object]]) -> str:
    if any(v["synthetic_present"] for v in summary.values()):
        return "synthetic_placeholder_data"
    return "missing_real_data"

summary = dataset_status()
status = placeholder_status(summary)

rows = [
    {"model":"LCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":status},
    {"model":"wCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":status},
    {"model":"curved_LCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":status},
    {"model":"DFM_MKC","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":status},
]

with open("artifacts/results/model_comparison_real_data.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    w.writeheader()
    w.writerows(rows)
