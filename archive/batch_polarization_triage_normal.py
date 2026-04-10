import os
import cv2
import numpy as np
import pandas as pd
from calculate_polarization_index import calculate_synaptic_score

DATA_DIR = "lc25000_data/lung_colon_image_set/lung_image_sets/lung_n" 
OUTPUT_CSV = "normal_polarization_detailed.csv"

def massive_solid_segment(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Target Mask: Higher threshold + Heavy Morphology
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    
    # Close the gaps to find large, continuous regions
    kernel = np.ones((30,30), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closing)
    mass_mask = np.zeros_like(closing)
    
    # Only keep targets that are truly massive (Tumor Nests/Large Vessels)
    # 30,000 pixels is the threshold for 'Solid Tissue' vs 'Air Space scaffolding'
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > 30000:
            mass_mask[labels == i] = 255
            
    # 2. T-Cell Mask
    _, t_cell_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    
    return t_cell_mask, mass_mask

results = []
image_paths = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.lower().endswith(('.jpeg', '.png'))]
print("Filtering Normal Lung for Massive Solid targets...")

for path in image_paths[:50]:
    img = cv2.imread(path)
    if img is None: continue
    t_cells, target = massive_solid_segment(img)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(t_cells)
    
    counts = {"ACTIVE": 0, "FRUSTRATED": 0, "DESERT": 0}
    for i in range(1, num_labels):
        if 20 < stats[i, cv2.CC_STAT_AREA] < 500:
            single_cell = (labels == i).astype(np.uint8) * 255
            # If no massive target exists, the cell is 'DESERT' (Success!)
            status = calculate_synaptic_score(single_cell, target)
            if status == "ACTIVE_SYNAPSE": counts["ACTIVE"] += 1
            elif status == "FRUSTRATED_EXCLUDED": counts["FRUSTRATED"] += 1
            else: counts["DESERT"] += 1
            
    results.append({"file": os.path.basename(path), "active_synapses": counts["ACTIVE"], "frustrated_excluded": counts["FRUSTRATED"], "immune_desert": counts["DESERT"]})

pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
print("Normal baseline updated.")
