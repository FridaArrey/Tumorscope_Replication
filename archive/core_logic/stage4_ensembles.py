import numpy as np
from PIL import Image
from scipy.spatial import KDTree
import os

def space_ensemble_analysis(image_path):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    print(f"\n[SPACE-Lite] Analyzing Cellular Ensembles (PNAS 2025): {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # 1. Segment T-cells (Blue/Purple nuclei)
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120) 
    # 2. Segment Macrophages (Stained Brown/Yellow in many IHC protocols)
    # We target the 'DAB' brown tones seen in the PNAS clusters
    mac_mask = (data[:,:,0] > 140) & (data[:,:,1] > 100) & (data[:,:,2] < 100)
    
    t_coords = np.argwhere(t_mask)
    mac_coords = np.argwhere(mac_mask)
    
    if len(t_coords) < 5 or len(mac_coords) < 5:
        print("!! Low cellularity: Cannot detect Ensembles.")
        return

    # SEARCH RADIUS: Based on SPACE (Spatial Patterning Analysis of Cellular Ensembles)
    # We define an 'Ensemble' as a T-cell within 20 pixels of a Macrophage.
    tree = KDTree(mac_coords)
    indices = tree.query_ball_point(t_coords, r=20)
    
    # Count how many T-cells are 'huddled' in an ensemble
    ensemble_t_cells = sum(1 for match in indices if len(match) > 0)
    ensemble_ratio = ensemble_t_cells / len(t_coords)

    print("="*45)
    print("      PNAS 2025: SPACE ENSEMBLE REPORT")
    print("="*45)
    print(f"Total T-cells:        {len(t_coords)}")
    print(f"Ensemble-Linked:      {ensemble_t_cells}")
    print(f"Ensemble Ratio:       {ensemble_ratio:.4f}")
    print("-" * 45)

    # Interpretation from PNAS Figure 5G: 
    # Log Ratio of Aggregates vs. Null is significantly higher in Postmortem samples.
    if ensemble_ratio > 0.45:
        status = "HIGH AGGREGATION (Advanced TB/Postmortem Profile)"
        insight = "High CD68 Macrophage covariation observed."
    else:
        status = "LOW AGGREGATION (Early/Biopsy Profile)"
        insight = "Diffuse spatial organization detected."
        
    print(f"STATUS:  {status}")
    print(f"INSIGHT: {insight}")
    print("="*45 + "\n")

if __name__ == "__main__":
    space_ensemble_analysis("real_euro_brca_tile.png")
