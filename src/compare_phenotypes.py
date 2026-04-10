import pandas as pd

def get_stats(csv_file, is_tb=False):
    try:
        df = pd.read_csv(csv_file)
        if df.empty: return 0, 0, 0
        
        # Calculate Frustration
        total_pol = df['active_synapses'].sum() + df['frustrated_excluded'].sum()
        rate = df['frustrated_excluded'].sum() / total_pol if total_pol > 0 else 0
        
        # SPATIAL NORMALIZATION: 
        # Steyn images (5x) cover 16x more area than LC25000 (20x).
        # We divide TB density by 16 to get "per-equivalent-tile" density.
        density = df['total_cells'].mean()
        if is_tb:
            density = density / 16
            
        return rate, density, rate * density
    except:
        return 0, 0, 0

# Re-loading everything
n_r, n_d, n_b = get_stats("normal_polarization_detailed.csv")
a_r, a_d, a_b = get_stats("aca_polarization_detailed.csv")
s_r, s_d, s_b = get_stats("scc_polarization_detailed.csv")
t_r, t_d, t_b = get_stats("tb_polarization_detailed.csv", is_tb=True)

print(f"\n--- NORMALIZED PATHOLOGICAL SPECTRUM (Berlin) ---")
print(f"{'Phenotype':<20} | {'Frustration':<12} | {'Density':<8} | {'Burden'}")
print("-" * 65)
print(f"{'Normal Lung':<20} | {n_r:>11.1%} | {n_d:>8.1f} | {n_b:>12.2f}")
print(f"{'Adeno (ACA)':<20} | {a_r:>11.1%} | {a_d:>8.1f} | {a_b:>12.2f}")
print(f"{'Squamous (SCC)':<20} | {s_r:>11.1%} | {s_d:>8.1f} | {s_b:>12.2f}")
print(f"{'TB (Steyn Lab)':<20} | {t_r:>11.1%} | {t_d:>8.1f} | {t_b:>12.2f}")
