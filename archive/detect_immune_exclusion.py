import numpy as np
from PIL import Image
from scipy.spatial import distance

def analyze_cold_signature(image_path):
    print(f"\n[CLINICAL-DDx] Analyzing for Immune Exclusion: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # 1. Segment T-cells (Blue)
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    # 2. Segment Nodule/Tumor (Pink/Brown)
    target_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)
    
    t_coords = np.argwhere(t_mask)
    target_coords = np.argwhere(target_mask)
    
    if len(t_coords) == 0 or len(target_coords) == 0:
        print("!! Warning: Insufficient cell density for exclusion analysis.")
        return

    # Calculate the Minimum Distance for every T-cell to the nearest Tumor pixel
    # If the majority of T-cells are > 30px away, it's 'Excluded' (COLD)
    # If they are < 10px, it's 'Inflamed' (HOT)
    
    sample_t = t_coords[np.random.choice(len(t_coords), min(500, len(t_coords)))]
    # Use a faster sampling for the target tissue
    sample_target = target_coords[::10]
    
    dists = [np.min(distance.cdist([t], sample_target)) for t in sample_t]
    avg_min_dist = np.mean(dists)
    percent_excluded = sum(1 for d in dists if d > 20) / len(dists) * 100

    print("="*45)
    print("      SPATIAL EXCLUSION (COLD) REPORT")
    print("="*45)
    print(f"Mean Interaction Gap: {avg_min_dist:.2f} px")
    print(f"Exclusion Threshold:  {percent_excluded:.1f}% of T-cells blocked")
    print("-" * 45)

    if avg_min_dist > 25:
        print("PHENOTYPE: COLD / IMMUNE-EXCLUDED")
        print("CLINICAL: Fibrotic barrier likely preventing T-cell entry.")
    else:
        print("PHENOTYPE: HOT / INFLAMED")
        print("CLINICAL: Active infiltration detected.")
    print("="*45 + "\n")

if __name__ == "__main__":
    analyze_cold_signature("real_euro_brca_tile.png")
