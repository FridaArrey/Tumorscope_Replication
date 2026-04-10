import numpy as np
from PIL import Image
from scipy.spatial import distance

def analyze_granuloma(image_path):
    print(f"\n[TB-SCOPE] Analyzing Granuloma Architecture: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # SEGMENTATION
    # 1. Necrotic Core (Often pale/pink/acellular)
    core_mask = (data[:,:,0] > 200) & (data[:,:,1] > 180) & (data[:,:,2] > 180)
    
    # 2. Lymphocyte Cuff (Dense dark purple T-cells)
    t_cell_mask = (data[:,:,2] > 140) & (data[:,:,0] < 110)
    
    c_coords = np.argwhere(core_mask)
    t_coords = np.argwhere(t_cell_mask)
    
    if len(c_coords) == 0 or len(t_coords) == 0:
        print("!! Detection Error: Could not identify core or cuff.")
        return

    # Calculate the Center of the Granuloma Core
    core_center = np.mean(c_coords, axis=0)
    
    # Calculate distances of all T-cells from the core center
    # This measures 'Radial Distribution'
    distances_from_center = distance.cdist([core_center], t_coords)[0]
    
    avg_radius = np.mean(distances_from_center)
    std_radius = np.std(distances_from_center) # Lower STD = More 'perfect' ring
    
    print("="*45)
    print("       TB-SCOPE: GRANULOMA INTEGRITY REPORT")
    print("="*45)
    print(f"Mean Cuff Radius:   {avg_radius:.2f} px")
    print(f"Structural Symmetry: {100 - std_radius:.2f}%")
    print("-" * 45)
    
    # Clinical Interpretation
    if std_radius < 50:
        status = "STABLE / SEQUESTERED"
        rec = "Bacterial containment likely successful."
    else:
        status = "DISORGANIZED / DISSEMINATING"
        rec = "High risk of bacterial escape (Miliary TB potential)."
        
    print(f"GRANULOMA STATE: {status}")
    print(f"CLINICAL INSIGHT: {rec}")
    print("="*45 + "\n")

if __name__ == "__main__":
    # We reuse the IHC tile as a proxy for the high-contrast tissue structure
    analyze_granuloma("real_euro_brca_tile.png")
