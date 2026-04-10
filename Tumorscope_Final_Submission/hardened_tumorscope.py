import numpy as np
from PIL import Image, ImageFilter
from scipy.spatial import cKDTree
import os

def find_file(filename):
    for root, dirs, files in os.walk("."):
        if filename in files:
            return os.path.join(root, filename)
    return None

def analyze_hardened(image_name):
    image_path = find_file(image_name)
    if not image_path:
        print(f"!! CRITICAL: {image_name} not found in any directory.")
        return

    print(f"--- Hardening Analysis: {image_path} ---")
    img = Image.open(image_path).convert('RGB')
    
    # 1. Texture-Based Stroma Mask (Critique #4: Stroma Context)
    gray = img.convert('L')
    texture = gray.filter(ImageFilter.MaxFilter(size=5))
    stroma_mask = np.array(texture) > 180 
    
    data = np.array(img).astype(float)
    
    # 2. Pseudo-Deconvolution (Critique #1: Stain Resilience)
    total_intensity = np.sum(data, axis=2) + 1
    r_norm = data[:,:,0] / total_intensity
    b_norm = data[:,:,2] / total_intensity
    
    tu_mask = (r_norm > 0.38) & (data[:,:,0] > 110)
    t_mask = (b_norm > 0.42) & (data[:,:,2] > 100)
    
    tu_coords = np.argwhere(tu_mask)
    t_coords = np.argwhere(t_mask)

    if len(tu_coords) == 0 or len(t_coords) == 0:
        print("!! Detection Failure: Check threshold calibration.")
        return

    # 3. KDTree with Physical Radius (Critique #2: Cell Physics)
    tree = cKDTree(tu_coords)
    CELL_RADIUS_PX = 15 
    
    interacting_indices = tree.query_ball_point(t_coords, r=CELL_RADIUS_PX)
    interacting_count = sum(1 for x in interacting_indices if len(x) > 0)
    
    # 4. Functional Probability (Critique #3: Functional Potential)
    stroma_penalty = np.mean(stroma_mask)
    interaction_score = (interacting_count / len(t_coords)) * (1 - stroma_penalty)

    print("-" * 30)
    print(f"Immune Cells: {len(t_coords)} | Tumor Pixels: {len(tu_coords)}")
    print(f"Stroma Obstruction Factor: {stroma_penalty:.2f}")
    print(f"Final Interaction Probability: {interaction_score:.4f}")
    print("-" * 30)
    
    if interaction_score > 0.25:
        print("RESULT: HIGH FUNCTIONAL INFILTRATION (HOT)")
    else:
        print("RESULT: SPATIAL EXCLUSION (COLD/STROMAL BARRIER)")

if __name__ == "__main__":
    analyze_hardened("real_euro_brca_tile.png")
