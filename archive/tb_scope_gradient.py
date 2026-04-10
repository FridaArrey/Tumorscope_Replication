import numpy as np
from PIL import Image
from scipy.spatial import distance

def analyze_tb_infiltration_gradient(image_path):
    print(f"\n[TB-SCOPE v2] Analyzing Infiltration Dynamics: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # Segment Immune Cells (T-cells) and Nodule Center
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    nodule_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)
    
    t_coords = np.argwhere(t_mask)
    n_coords = np.argwhere(nodule_mask)
    
    if len(t_coords) == 0 or len(n_coords) == 0:
        return

    # Calculate Center
    center = np.mean(n_coords, axis=0)
    dists = distance.cdist([center], t_coords)[0]
    max_r = np.max(dists)

    # Divide into 3 Shells (Inner 33%, Mid 66%, Outer 100%)
    inner = dists[dists <= max_r * 0.33]
    mid = dists[(dists > max_r * 0.33) & (dists <= max_r * 0.66)]
    outer = dists[dists > max_r * 0.66]

    print("="*45)
    print("    TB GRANULOMA INFILTRATION GRADIENT")
    print("="*45)
    print(f"Inner Core T-cells:  {len(inner)} nodes")
    print(f"Mantle T-cells:      {len(mid)} nodes")
    print(f"Outer Cuff T-cells:  {len(outer)} nodes")
    print("-" * 45)

    # Logic from the Frontiers Research:
    # High Inner/Mid counts suggest an "Active/Infiltrated" Granuloma.
    if len(inner) > (len(outer) * 0.1):
        print("PHENOTYPE: High Infiltration (Active Immune Signaling)")
    else:
        print("PHENOTYPE: Classic Sequestration (Latent/Stable)")
    print("="*45 + "\n")

if __name__ == "__main__":
    analyze_tb_infiltration_gradient("real_euro_brca_tile.png")
