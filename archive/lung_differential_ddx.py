import numpy as np
from PIL import Image
from scipy.spatial import distance

def run_differential_analysis(image_path):
    print(f"\n[LUNG-DDx] Performing Differential Analysis: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # 1. Segment Immune Cells (Blue/Purple)
    immune_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    # 2. Segment Target Tissue (Pink/Brown/Nodule)
    nodule_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)
    
    i_coords = np.argwhere(immune_mask)
    n_coords = np.argwhere(nodule_mask)
    
    if len(i_coords) < 10 or len(n_coords) < 10:
        print("!! Signal Error: Insufficient cellularity for DDx.")
        return

    # ANALYSIS A: Infiltration (Tumorscope Logic)
    sample_i = i_coords[np.random.choice(len(i_coords), min(200, len(i_coords)))]
    sample_n = n_coords[::50]
    inf_dist = np.mean([np.min(distance.cdist([i], sample_n)) for i in sample_i])
    
    # ANALYSIS B: Zonation/Symmetry (TB-Scope Logic)
    nodule_center = np.mean(n_coords, axis=0)
    rad_dists = distance.cdist([nodule_center], i_coords)[0]
    rad_std = np.std(rad_dists)

    print("="*45)
    print("      LUNG CLINICAL DIFFERENTIAL REPORT")
    print("="*45)
    print(f"Infiltration Score (Min-Dist): {inf_dist:.2f} px")
    print(f"Zonation Variance (Std-Dev):   {rad_std:.2f} px")
    print("-" * 45)
    
    # DIFFERENTIAL LOGIC
    # Low Infiltration Dist + High Variance = Likely Cancer (Infiltrating)
    # High Infiltration Dist + Low Variance  = Likely TB (Sequestrating)
    
    if inf_dist < 10:
        diagnosis = "MALIGNANT NEOPLASM (LUNG CANCER)"
        confidence = "High (Infiltrative Pattern)"
    elif rad_std < 45:
        diagnosis = "INFECTIOUS GRANULOMA (TUBERCULOSIS)"
        confidence = "High (Zonal Sequestration)"
    else:
        diagnosis = "UNDETERMINED NODULE"
        confidence = "Low (Mixed Pattern)"
        
    print(f"PREDICTED PATHOLOGY: {diagnosis}")
    print(f"DIAGNOSTIC CONFIDENCE: {confidence}")
    print("="*45 + "\n")

if __name__ == "__main__":
    run_differential_analysis("real_euro_brca_tile.png")
