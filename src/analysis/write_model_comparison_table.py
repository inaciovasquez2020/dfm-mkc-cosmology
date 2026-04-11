import csv
from src.data.load_public_cosmology_data import dataset_status

rows = [
    {"model":"LCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":"missing_real_data"},
    {"model":"wCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":"missing_real_data"},
    {"model":"curved_LCDM","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":"missing_real_data"},
    {"model":"DFM_MKC","logL":"","AIC":"","BIC":"","H0_mean":"","Omega_m_mean":"","status":"missing_real_data"},
]

s = dataset_status()
if all(v["present"] for v in s.values()):
    raise SystemExit("real-data table writer requires real fitting implementation before use")

with open("artifacts/results/model_comparison_real_data.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["model","logL","AIC","BIC","H0_mean","Omega_m_mean","status"])
    w.writeheader()
    w.writerows(rows)
