import numpy as np
from PIL import Image
from scipy.spatial import distance

def debug_coordinates(image_path):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    
    # Precise Segmentation
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    tu_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)
    
    t_coords = np.argwhere(t_mask)
    tu_coords = np.argwhere(tu_mask)
    
    print(f"DEBUG for {image_path}:")
    print(f"Total T-cells found: {len(t_coords)}")
    print(f"Total Tumor pixels found: {len(tu_coords)}")
    
    if len(t_coords) > 0 and len(tu_coords) > 0:
        # Check the first few T-cells
        sample_t = t_coords[:5]
        for i, t in enumerate(sample_t):
            # Find closest tumor pixel
            dists = distance.cdist([t], tu_coords)
            min_d = np.min(dists)
            print(f"  T-cell {i} at {t} is {min_d:.2f}px from nearest tumor.")

if __name__ == "__main__":
    debug_coordinates("real_excluded_lung.png")
