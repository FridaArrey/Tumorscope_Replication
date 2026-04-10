import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

def run_tumorscope_pipeline():
    # 1. Simulation Parameters
    grid_size = 200
    np.random.seed(42)
    
    # 2. Generate Tumor Nest (The "Cold" Core)
    tumor_mask = np.zeros((grid_size, grid_size))
    y, x = np.ogrid[:grid_size, :grid_size]
    # Central tumor mass
    mask = (y - 100)**2 + (x - 100)**2 <= 40**2
    tumor_mask[mask] = 1
    
    # 3. Generate T-cells (Stochastic distribution)
    # Simulating a baseline immune state before therapy
    t_cells = np.random.randint(0, 200, (60, 2))
    
    # 4. Calculate Spatial Infiltration (Euclidean Distance)
    tumor_coords = np.argwhere(tumor_mask == 1)
    min_dists = [np.min(distance.cdist([cell], tumor_coords)) for cell in t_cells]
    
    # 5. Spatial Classification
    # Thresholds: 0 (In-tumor), 1-20 (Peritumoral/Margin), >20 (Excluded)
    infiltrated = [d for d in min_dists if d <= 0]
    peritumoral = [d for d in min_dists if 0 < d <= 20]
    excluded = [d for d in min_dists if d > 20]
    
    # 6. Clinical Diagnostic Logic
    avg_dist = np.mean(min_dists)
    
    print("\n" + "="*40)
    print("      TUMORSCOPE: SPATIAL BIO-REPORT")
    print("="*40)
    print(f"Total T-cells Analyzed: {len(t_cells)}")
    print(f"Infiltrated (Hot):      {len(infiltrated)}")
    print(f"Peritumoral (Margin):   {len(peritumoral)}")
    print(f"Excluded (Cold):        {len(excluded)}")
    print(f"Mean Distance to Tumor: {avg_dist:.2f} units")
    print("-" * 40)
    
    # Status Determination
    if len(infiltrated) > len(excluded):
        status = "INFLAMED (HOT)"
        recommendation = "High probability of Immunotherapy response."
    elif len(peritumoral) > len(infiltrated):
        status = "IMMUNE EXCLUDED"
        recommendation = "Consider stromal-targeting combination therapy."
    else:
        status = "IMMUNE DESERT (COLD)"
        recommendation = "Priming therapies required to recruit T-cells."
        
    print(f"TME STATUS:     {status}")
    print(f"NEXT STEPS:     {recommendation}")
    print("="*40 + "\n")

if __name__ == "__main__":
    run_tumorscope_pipeline()
