import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the results
df = pd.read_csv('cohort_results.csv')

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Stroma_Density', y='Infiltration_Score', 
                hue='Phenotype', style='Diagnosis', s=100, palette='viridis')

plt.title('Lung Cancer Cohort: Immune-Stromal Landscape')
plt.xlabel('Stromal Density (Physical Barrier)')
plt.ylabel('T-Cell Infiltration (Immune Activity)')
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='High Stroma Threshold')
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('cohort_landscape.png')
print("Plot saved as cohort_landscape.png")
