import torch
import numpy as np
from PIL import Image, ImageFilter
from scipy.spatial import cKDTree
import os
import sys

# Import our Triage logic from the previous script
from lc25000_triage import LungClassifier

def analyze_spatial_biology(image_path):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img).astype(float)
    
    # 1. Texture-Based Stroma Mask (The TB Barrier)
    gray = img.convert('L')
    texture = gray.filter(ImageFilter.MaxFilter(size=5))
    stroma_mask = np.array(texture) > 180 
    
    # 2. Cell Detection (Normalized Ratios)
    total_intensity = np.sum(data, axis=2) + 1
    r_norm = data[:,:,0] / total_intensity
    b_norm = data[:,:,2] / total_intensity
    
    tu_mask = (r_norm > 0.38) & (data[:,:,0] > 110)
    t_mask = (b_norm > 0.42) & (data[:,:,2] > 100)
    
    tu_coords = np.argwhere(tu_mask)
    t_coords = np.argwhere(t_mask)

    if len(tu_coords) == 0 or len(t_coords) == 0:
        return 0, np.mean(stroma_mask), "LOW_SIGNAL"

    # 3. Physical Contact Analysis
    tree = cKDTree(tu_coords)
    interacting_indices = tree.query_ball_point(t_coords, r=15)
    interacting_count = sum(1 for x in interacting_indices if len(x) > 0)
    
    interaction_score = (interacting_count / len(t_coords))
    return interaction_score, np.mean(stroma_mask), "SUCCESS"

def main_report(image_path):
    print("="*50)
    print(f"PATHOLOGY REPORT: {os.path.basename(image_path)}")
    print("="*50)

    # STEP 0: TRIAGE
    classifier = LungClassifier(model_path='lung_triage_v1.pth')
    diagnosis, confidence = classifier.predict(image_path)
    
    print(f"DIAGNOSIS: {diagnosis} ({confidence*100:.2f}% Confidence)")
    
    if diagnosis == 'LUNG_N':
        print("\nSUMMARY: No malignant patterns detected.")
        print("RECOMMENDATION: Routine follow-up.")
        return

    # STEP 1-4: SPATIAL ANALYSIS
    score, stroma, status = analyze_spatial_biology(image_path)
    
    print(f"STROMAL DENSITY: {stroma*100:.1f}%")
    print(f"IMMUNE INFILTRATION: {score*100:.1f}%")
    
    # STEP 5: CLINICAL CORRELATION (TB + CANCER)
    print("\n" + "-"*30)
    print("CLINICAL RECOMMENDATION (Berlin Suite)")
    print("-"*30)
    
    if score > 0.30 and stroma < 0.40:
        print("PHENOTYPE: 'HOT' TUMOR")
        print("ADVICE: High probability of Immunotherapy response.")
        if stroma < 0.20:
            print("ALERT: Low stromal barrier. Monitor for TB dissemination if co-infection exists.")
    elif score < 0.15 and stroma > 0.50:
        print("PHENOTYPE: 'EXCLUDED' TUMOR")
        print("ADVICE: T-cells are trapped in stroma. Consider anti-fibrotic priming.")
        print("ALERT: Strong granuloma-like stroma suggests TB is likely sequestered/safe.")
    else:
        print("PHENOTYPE: 'IMMUNE DESERT' OR INTERMEDIATE")
        print("ADVICE: Further IHC staining for PD-L1 recommended.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_report(sys.argv[1])
    else:
        print("Usage: python3 pathology_master_suite.py <path_to_tile>")
