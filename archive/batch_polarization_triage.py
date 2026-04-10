import os
import cv2
import numpy as np
import pandas as pd
from calculate_polarization_index import calculate_synaptic_score

# Base path - the script will now search recursively
DATA_DIR = "lc25000_data" 
OUTPUT_CSV = "scc_polarization_detailed.csv"

def density_weighted_segment(img):
    """Refined Thresholding for T-cell/Tumor segmentation"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Tumor is usually lighter/dense in these tiles
    _, tumor_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    # T-cells are the small, dark, high-contrast spots
    _, t_cell_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    return t_cell_mask, tumor_mask

results = []
print(f"Scanning {DATA_DIR} for images...")

# Walk through all subdirectories to find images
image_paths = []
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_paths.append(os.path.join(root, file))

print(f"Found {len(image_paths)} images. Analyzing first 50...")

for path in image_paths[:50]:
    img = cv2.imread(path)
    if img is None: continue
    
    t_cells, tumor = density_weighted_segment(img)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(t_cells)
    
    counts = {"ACTIVE": 0, "FRUSTRATED": 0, "DESERT": 0}
    
    for i in range(1, num_labels):
        # Filter by size to ignore noise (only look at T-cell sized blobs)
        if 20 < stats[i, cv2.CC_STAT_AREA] < 500:
            single_cell = (labels == i).astype(np.uint8) * 255
            status = calculate_synaptic_score(single_cell, tumor)
            
            if status == "ACTIVE_SYNAPSE": counts["ACTIVE"] += 1
            elif status == "FRUSTRATED_EXCLUDED": counts["FRUSTRATED"] += 1
            else: counts["DESERT"] += 1

    results.append({
        "file": os.path.basename(path),
        "folder": os.path.dirname(path),
        "active_synapses": counts["ACTIVE"],
        "frustrated_excluded": counts["FRUSTRATED"],
        "immune_desert": counts["DESERT"]
    })

df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Analysis complete. Results saved to {OUTPUT_CSV}")
