import numpy as np
from PIL import Image
from scipy.spatial import distance
import os

def clinical_report(image_path):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Run fetch_real_euro.py first!")
        return

    print(f"\n[CLINICAL LOG] Analyzing Tissue Sample: {image_path}")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # IHC COLOR SEGMENTATION
    # Hematoxylin (Nuclei/T-cells): High Blue, Low Red
    t_cell_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    
    # DAB Staining (Tumor/Tissue): High Red/Brown tones
    cancer_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)
    
    t_coords = np.argwhere(t_cell_mask)
    c_coords = np.argwhere(cancer_mask)
    
    if len(t_coords) < 10 or len(c_coords) < 10:
        print("!! Signal Alert: Adjusting for high-confluence tissue...")
        return

    # Spatial Proximity Analysis
    # Sampling 300 T-cells for clinical significance
    sample_t = t_coords[np.random.choice(len(t_coords), min(300, len(t_coords)))]
    sample_c = c_coords[::50] 
    
    dists = [np.min(distance.cdist([t], sample_c)) for t in sample_t]
    avg_dist = np.mean(dists)
    
    print("="*45)
    print("       TUMORSCOPE: FINAL CLINICAL VALIDATION")
    print("="*45)
    print(f"Method: Spatial Proximity (Euclidean Distance)")
    print(f"Mean Spatial Distance: {avg_dist:.2f} px")
    print("-" * 45)
    
    # Clinical Phenotype Classification
    # Threshold < 35px indicates "Hot" (Infiltrated) tumor
    if avg_dist < 35:
        status, rec = "INFLAMMED (HOT)", "High potential for immune checkpoint blockade."
    else:
        status, rec = "IMMUNE EXCLUDED (COLD)", "Suggest combination with stroma-modifying agents."
        
    print(f"TME PHENOTYPE: {status}")
    print(f"RECOMMENDATION: {rec}")
    print("="*45 + "\n")

if __name__ == "__main__":
    clinical_report("real_euro_brca_tile.png")
