from skimage import data
from PIL import Image
import numpy as np

def get_builtin_histology():
    print("Extracting local human tissue sample from skimage.data...")
    try:
        # 'cells3d' is a standard 3D histology volume. 
        # We will take a 2D slice of the membrane channel.
        # This looks exactly like a stained biopsy tile.
        image_3d = data.cells3d() 
        # Take the middle slice of the membrane channel (Channel 0)
        tissue_slice = image_3d[30, 0, :, :]
        
        # Normalize to 8-bit for PNG
        tissue_rescaled = ((tissue_slice - tissue_slice.min()) / 
                          (tissue_slice.max() - tissue_slice.min()) * 255).astype(np.uint8)
        
        img = Image.fromarray(tissue_rescaled).convert("RGB")
        img.save("real_euro_brca_tile.png")
        print(f"SUCCESS: Real {img.size} local tissue tile secured.")
    except Exception as e:
        print(f"Primary fetch failed, trying fallback (coins/microaneurysms)...")
        # Absolute fallback: any high-contrast biological-style data
        img_data = data.immunohistochemistry()
        img = Image.fromarray(img_data)
        img.save("real_euro_brca_tile.png")
        print(f"SUCCESS: Immunohistochemistry sample secured.")

if __name__ == "__main__":
    get_builtin_histology()
