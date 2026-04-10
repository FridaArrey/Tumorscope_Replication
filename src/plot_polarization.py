import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("aca_polarization_detailed.csv")
df['frustration_index'] = df['frustrated_excluded'] / (df['active_synapses'] + df['frustrated_excluded'] + 1e-5)

plt.figure(figsize=(10, 6))
plt.hist(df['frustration_index'], bins=20, color='salmon', edgecolor='black')
plt.title("T-cell Frustration Index (Adenocarcinoma Cohort)")
plt.xlabel("Ratio of Frustrated to Total Polarized Cells")
plt.ylabel("Frequency (Number of Tiles)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('frustration_landscape.png')
print("Graph saved as frustration_landscape.png")
