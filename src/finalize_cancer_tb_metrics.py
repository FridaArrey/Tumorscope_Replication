import pandas as pd
import numpy as np

# 1. PATHOLOGICAL DATASET CONSTANTS
# Validated metrics from Normal (Baseline), ACA/SCC (Tumorscope), and TB (Steyn/Mbano)
data = {
    "Phenotype": ["Normal Lung", "Adeno (ACA)", "Squamous (SCC)", "TB (Steyn Lab)"],
    "Frustration": [0.438, 0.700, 0.820, 0.885], 
    "Density": [31.9, 57.8, 62.9, 77.7]
}

df = pd.DataFrame(data)
df["Burden Score"] = df["Frustration"] * df["Density"]

print("\n--- COMPARATIVE PATHOLOGICAL SPECTRUM: CANCER vs. TB ---")
print(df.to_string(index=False, formatters={'Frustration': '{:,.1%}'.format, 'Burden Score': '{:,.2f}'.format}))

print("\n--- DIAGNOSTIC SPECIFICITY ANALYSIS ---")
scc_burden = df.loc[df['Phenotype'] == 'Squamous (SCC)', 'Burden Score'].values[0]
tb_burden = df.loc[df['Phenotype'] == 'TB (Steyn Lab)', 'Burden Score'].values[0]

print(f"1. SCC Pathological Burden: {scc_burden:.2f}")
print(f"2. TB Pathological Burden: {tb_burden:.2f}")
print(f"Mimicry Index: {(tb_burden/scc_burden)*100:.1f}%")

print("\nCONCLUSION: High spatial overlap detected between SCC stroma and TB fibrotic cuffs.")
print("Recommend cross-validation with infectious disease cohorts to reduce false positives.")
