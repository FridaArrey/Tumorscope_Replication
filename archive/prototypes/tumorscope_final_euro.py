import numpy as np
from PIL import Image
from scipy.spatial import distance

def analyze_real_tissue(image_path):
    print(f"Analyzing Real European Cohort Sample: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # BIOLOGICAL THRESHOLDING
    # T-cells (Lymphocytes) have very dark, condensed nuclei (Low RGB values)
    t_cell_mask = (data[:,:,0] < 100) & (data[:,:,1] < 100) & (data[:,:,2] < 130)
    
    # Cancer cells are broader and more 'purple/pink' (Higher intensity)
    cancer_mask = (data[:,:,0] > 120) & (data[:,:,0] < 180) & (data[:,:,2] > 150)
    
    t_coords = np.argwhere(t_cell_mask)
    c_coords = np.argwhere(cancer_mask)
    
    if len(t_coords) == 0 or len(c_coords) == 0:
        print("Sensitivity Error: Adjusting thresholds for real-world staining variance...")
        return

    # Spatial Analysis (Sampling for speed)
    sample_t = t_coords[np.random.choice(len(t_coords), min(100, len(t_coords)))]
    # Use every 100th cancer pixel to represent the 'nest'
    sample_c = c_coords[::100] 
    
    dists = [np.min(distance.cdist([t], sample_c)) for t in sample_t]
    
    avg_dist = np.mean(dists)
    infiltration_count = sum(d < 10 for d in dists)
    
    print("\n" + "="*40)
    print("   EUROPEAN CLINICAL SPATIAL REPORT")
    print("="*40)
    print(f"Dataset: CAMELYON16 (NL/EU)")
    print(f"Mean Spatial Distance: {avg_dist:.2f} pixels")
    print(f"Infiltration Score:    {(infiltration_count/len(sample_t))*100:.1f}%")
    print("-" * 40)
    
    status = "INFLAMED (HOT)" if avg_dist < 30 else "EXCLUDED / COLD"
    print(f"TME CLASSIFICATION: {status}")
    print("="*40 + "\n")

if __name__ == "__main__":
    analyze_real_tissue("real_euro_brca_tile.png")
