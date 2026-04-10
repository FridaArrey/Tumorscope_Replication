import openslide
import numpy as np
import pandas as pd
from PIL import Image
from pathology_master_suite import analyze_spatial_biology
from lc25000_triage import LungClassifier
import os

def is_not_background(tile, threshold=230, fraction=0.9):
    """Returns True if the tile contains actual tissue (not just white glass)."""
    gray = tile.convert('L')
    grid = np.array(gray)
    # If more than 90% of pixels are near-white, it's background
    white_pixels = np.sum(grid > threshold)
    return white_pixels < (grid.size * fraction)

def scan_tcga_slide(svs_path, model_path='lung_triage_v1.pth', patch_size=512):
    print(f"--- Opening WSI: {os.path.basename(svs_path)} ---")
    slide = openslide.OpenSlide(svs_path)
    classifier = LungClassifier(model_path=model_path)
    
    width, height = slide.dimensions
    results = []
    
    # Using a larger step to get a "representative sample" first
    # Change step to patch_size for a full exhaustive scan
    step = patch_size * 2 
    
    for y in range(0, height, step):
        for x in range(0, width, step):
            # Read tile at Level 0
            tile = slide.read_region((x, y), 0, (patch_size, patch_size)).convert('RGB')
            
            if is_not_background(tile):
                # Save temp tile for the classifier logic
                tile.save("temp_patch.jpeg")
                
                # 1. Triage
                diag, conf = classifier.predict("temp_patch.jpeg")
                
                # 2. Spatial Analysis (Only if Malignant)
                if diag != 'LUNG_N':
                    score, stroma, status = analyze_spatial_biology("temp_patch.jpeg")
                    results.append({
                        'x': x, 'y': y,
                        'diagnosis': diag,
                        'confidence': conf,
                        'stroma': stroma,
                        'infiltration': score
                    })
    
    os.remove("temp_patch.jpeg")
    df = pd.DataFrame(results)
    df.to_csv(f"{os.path.basename(svs_path)}_spatial_map.csv", index=False)
    print(f"--- Scan Complete. Analyzed {len(results)} tissue patches. ---")

if __name__ == "__main__":
    # Example usage (Replace with your downloaded .svs path)
    # scan_tcga_slide("your_tcga_file.svs")
    print("Ready for TCGA. Ensure 'openslide' is installed via brew.")
