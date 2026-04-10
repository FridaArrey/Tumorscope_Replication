import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from calculate_polarization_index import calculate_synaptic_score

# CRITICAL: Tell PIL to allow huge pathology slides
Image.MAX_IMAGE_PIXELS = None 

TB_DIR = "lc25000_data/lung_tb_jem/granuloma_samples"
OUTPUT_CSV = "tb_polarization_detailed.csv"

def analyze_steyn_pathology(img_path):
    try:
        pil_img = Image.open(img_path).convert('RGB')
        
        # RESIZE STRATEGY: 
        # These slides are huge. To match LC25000 scale, we downsample.
        width, height = pil_img.size
        # Limit to max 4000px wide while maintaining aspect ratio
        if width > 4000:
            scale = 4000 / width
            pil_img = pil_img.resize((4000, int(height * scale)), Image.Resampling.LANCZOS)
            
        img = np.array(pil_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error reading {img_path}: {e}")
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Target: The Mycetoma/Necrotic Core (Steyn 2022 Logic)
    _, core_thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    kernel = np.ones((31,31), np.uint8)
    target_mask = cv2.morphologyEx(core_thresh, cv2.MORPH_CLOSE, kernel)
    
    # T-Cells: The Mbano 2026 'Fibrotic Cuff'
    _, t_cell_mask = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(t_cell_mask)
    
    counts = {"ACTIVE": 0, "FRUSTRATED": 0, "DESERT": 0}
    total_cells = 0
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        # Adjusted area for the downsampled magnification
        if 20 < area < 500:
            total_cells += 1
            cell = (labels == i).astype(np.uint8) * 255
            status = calculate_synaptic_score(cell, target_mask)
            if status == "ACTIVE_SYNAPSE": counts["ACTIVE"] += 1
            elif status == "FRUSTRATED_EXCLUDED": counts["FRUSTRATED"] += 1
            else: counts["DESERT"] += 1
    
    return counts, total_cells

results = []
image_files = [f for f in os.listdir(TB_DIR) if f.lower().endswith(('.tif', '.tiff'))]
print(f"Analyzing {len(image_files)} Steyn Lab (AHRI) validation slides...")

for file in image_files:
    path = os.path.join(TB_DIR, file)
    print(f"Processing: {file}...")
    counts, total_cells = analyze_steyn_pathology(path)
    
    if counts:
        results.append({
            "file": file,
            "active_synapses": counts["ACTIVE"],
            "frustrated_excluded": counts["FRUSTRATED"],
            "immune_desert": counts["DESERT"],
            "total_cells": total_cells
        })

pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
print(f"TB Batch Analysis Complete. Results: {OUTPUT_CSV}")
