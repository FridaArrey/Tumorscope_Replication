import os
import csv
import glob
from pathology_master_suite import analyze_spatial_biology
from lc25000_triage import LungClassifier

def process_cohort(data_directory, output_file="cohort_results.csv", limit=100):
    print(f"--- Starting Batch Processing (Limit: {limit} images) ---")
    classifier = LungClassifier(model_path='lung_triage_v1.pth')
    headers = ['Filename', 'Diagnosis', 'Confidence', 'Stroma_Density', 'Infiltration_Score', 'Phenotype']
    
    # Target ONLY Squamous Cell (scc) files
    image_paths = glob.glob(os.path.join(data_directory, "**/lung_scc/*.jpeg"), recursive=True)[:limit]
    
    if not image_paths:
        # Try an alternative path structure just in case
        image_paths = glob.glob(os.path.join(data_directory, "**/logscc*.jpeg"), recursive=True)[:limit]

    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i, path in enumerate(image_paths):
            diag, conf = classifier.predict(path)
            if diag != 'LUNG_N':
                score, stroma, status = analyze_spatial_biology(path)
                if score > 0.30 and stroma < 0.40: phenotype = "HOT"
                elif score < 0.15 and stroma > 0.50: phenotype = "EXCLUDED"
                else: phenotype = "DESERT/INTERMEDIATE"
            else:
                score, stroma, phenotype = 0, 0, "BENIGN"
            writer.writerow([os.path.basename(path), diag, f"{conf:.4f}", f"{stroma:.4f}", f"{score:.4f}", phenotype])
            if (i + 1) % 10 == 0: print(f"Processed {i + 1}/{len(image_paths)}...")
    print(f"--- Done. Results in {output_file} ---")

if __name__ == "__main__":
    target_dir = 'lc25000_data/lung_colon_image_set/lung_image_sets'
    process_cohort(target_dir)
