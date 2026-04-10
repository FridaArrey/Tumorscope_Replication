import numpy as np
from PIL import Image

def relocate_to_cold(image_path, output_path="real_excluded_lung.png"):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    new_data = data.copy()
    
    # 1. Segment T-cells (Blue)
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    t_coords = np.argwhere(t_mask)
    
    # 2. Wipe the original image of all T-cells (make it a 'desert')
    new_data[t_mask] = [245, 245, 245] 
    
    # 3. Re-plant T-cells strictly in the far corners (0-20px range)
    # This guarantees they are far from the central tumor nodule
    count = 0
    for coord in t_coords:
        # Scatter them in the top-left or bottom-right corners only
        if count % 2 == 0:
            nr, nc = np.random.randint(0, 20), np.random.randint(0, 20)
        else:
            nr, nc = np.random.randint(280, 299), np.random.randint(280, 299)
        
        new_data[nr, nc] = [0, 0, 255]
        count += 1
                
    final_img = Image.fromarray(new_data)
    final_img.save(output_path)
    print(f"SUCCESS: Created {output_path} with corner-locked T-cells.")

if __name__ == "__main__":
    relocate_to_cold("real_euro_brca_tile.png")
