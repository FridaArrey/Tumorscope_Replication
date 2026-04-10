import numpy as np
from PIL import Image
from scipy.spatial import distance
import sys

def check_for_stromal_barrier(image_path):
    print(f"\n[BARRIER-ANALYSIS] High-Contrast Masking: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img).astype(float)
    
    # 1. T-cells: Pure Blue detection
    t_mask = (data[:,:,2] > 180) & (data[:,:,0] < 150)
    
    # 2. SELECTIVE Tumor: Only the darkest pink/brown areas
    # This filters out the 'Pale Pink' background that was causing the 115k saturation
    tu_mask = (data[:,:,0] > 160) & (data[:,:,1] < 100) & (data[:,:,2] < 140)

    t_coords = np.argwhere(t_mask)
    tu_coords = np.argwhere(tu_mask)
    
    print(f"Cells: {len(t_coords)} | High-Density Target Pixels: {len(tu_coords)}")

    if len(tu_coords) < 10:
        print("!! Target too small. Reverting to Intensity-only mask.")
        tu_mask = (data[:,:,0] > 180) & (data[:,:,1] < 150)
        tu_coords = np.argwhere(tu_mask)

    if len(t_coords) == 0:
        print("!! No cells detected.")
        return

    # Spatial Calculation
    sample_tu = tu_coords[::20]
    dists = [np.min(distance.cdist([t], sample_tu)) for t in t_coords]
    
    # Exclusion Threshold: If cell is > 50px from the dark nodule
    exclusion_rate = sum(1 for d in dists if d > 50) / len(t_coords)

    print("="*45)
    print("      STROMA ENTRAPMENT (COLD) REPORT")
    print("="*45)
    print(f"Exclusion Rate: {exclusion_rate*100:.1f}%")
    print("-" * 45)

    if exclusion_rate > 0.6:
        print("DIAGNOSIS: IMMUNE-EXCLUDED (COLD)")
    else:
        print("DIAGNOSIS: IMMUNE-INFILTRATED (HOT)")
    print("="*45 + "\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "real_euro_brca_tile.png"
    check_for_stromal_barrier(target)
