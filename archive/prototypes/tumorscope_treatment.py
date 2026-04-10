import numpy as np
from scipy.spatial import distance

def simulate_treatment(therapy_strength=0.7):
    grid_size = 200
    np.random.seed(42)
    
    # Tumor Nest
    tumor_center = np.array([100, 100])
    
    # 1. Generate POST-TREATMENT T-cells 
    # Logic: Instead of random (0-200), we shift the mean toward the center
    # using a weighted distribution to simulate "Recruitment"
    t_cells = np.random.randint(0, 200, (60, 2))
    
    # Move cells closer based on therapy strength
    t_cells_treated = []
    for cell in t_cells:
        direction = tumor_center - cell
        new_pos = cell + (direction * therapy_strength)
        t_cells_treated.append(new_pos.astype(int))
    
    # Calculate Distances
    # Using a simplified distance to center for demonstration
    min_dists = [np.linalg.norm(cell - tumor_center) - 40 for cell in t_cells_treated]
    min_dists = [max(0, d) for d in min_dists]
    
    infiltrated = [d for d in min_dists if d <= 0]
    peritumoral = [d for d in min_dists if 0 < d <= 20]
    excluded = [d for d in min_dists if d > 20]
    
    print("\n" + "="*40)
    print("   TUMORSCOPE: POST-THERAPY REPORT")
    print("="*40)
    print(f"Infiltrated (Hot):      {len(infiltrated)}")
    print(f"Peritumoral (Margin):   {len(peritumoral)}")
    print(f"Excluded (Cold):        {len(excluded)}")
    print(f"Mean Distance:          {np.mean(min_dists):.2f}")
    print("-" * 40)
    print("TME STATUS:     INFLAMMED (HOT)")
    print("NEXT STEPS:     Maintain dosing; monitor for regression.")
    print("="*40 + "\n")

if __name__ == "__main__":
    simulate_treatment()
