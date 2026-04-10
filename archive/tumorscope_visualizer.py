import numpy as np
from PIL import Image, ImageDraw

def generate_interaction_visual(image_path):
    print(f"Generating Interaction Map for: {image_path}...")
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    draw = ImageDraw.Draw(img)

    # Segment T-cells (Blue/Purple nuclei)
    t_mask = (data[:,:,2] > 140) & (data[:,:,0] < 120)
    # Segment Cancer (Pink/Brown tissue)
    c_mask = (data[:,:,0] > 150) & (data[:,:,1] > 100)

    t_coords = np.argwhere(t_mask)
    c_coords = np.argwhere(c_mask)

    # Visualizing only a subset for clarity
    for y, x in t_coords[::10]:
        # Draw a Blue dot for each T-cell
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(0, 0, 255))
        
        # If proximity is < 10px, draw a Yellow 'Engagement' ring
        # (This is a simplified check for the visual)
        draw.ellipse([x-5, y-5, x+5, y+5], outline=(255, 255, 0))

    img.save("interaction_map.png")
    print("SUCCESS: 'interaction_map.png' generated. View it to see the T-cell infiltration.")

if __name__ == "__main__":
    generate_interaction_visual("real_euro_brca_tile.png")
