import zarr
import s3fs
import matplotlib.pyplot as plt
import numpy as np

# 1. Connect to OpenOrganelle S3
s3_path = 'janelia-cosem-datasets/jrc_ctl-id8-1/jrc_ctl-id8-1.zarr'
s3 = s3fs.S3Map(root=s3_path, s3=s3fs.S3FileSystem(anon=True))
root = zarr.group(store=s3)

try:
    # 2. Navigate the specific hierarchy discovered in your terminal
    # Path: recon-1 / em / fibsem-uint8
    data_container = root['recon-1']['em']['fibsem-uint8']
    
    # Check if this is a multiscale group or a direct array
    if isinstance(data_container, zarr.hierarchy.Group):
        # List available resolutions (s0, s1, s2, etc.)
        res_levels = sorted(list(data_container.array_keys()))
        print(f"Available resolutions: {res_levels}")
        # Use a medium resolution (like s4 or s3) to avoid huge downloads
        target_res = 's4' if 's4' in res_levels else res_levels[-1]
        data = data_container[target_res]
    else:
        data = data_container

    print(f"Accessing array: {data.path}")
    print(f"Full Volume Shape: {data.shape} (Z, Y, X)")

    # 3. Extract a 3D Chunk from the center to find the Synapse
    # We take a 200x500x500 chunk to be sure we hit the cell
    z_mid, y_mid, x_mid = [s // 2 for s in data.shape]
    
    # Slicing a manageable preview
    preview = data[z_mid, y_mid-250:y_mid+250, x_mid-250:x_mid+250]

    # 4. Save the "Micro" architecture preview
    plt.figure(figsize=(8, 8))
    plt.imshow(preview, cmap='gray')
    plt.title(f"CTL-ID8-1: {data.path} (Voxel Ground Truth)")
    plt.axis('off')
    plt.savefig('micro_synapse_preview.png')
    
    print("\n--- Success! ---")
    print(f"Preview saved to: micro_synapse_preview.png")
    print(f"Voxel Data Type: {data.dtype}")
    
except Exception as e:
    print(f"Still having trouble: {e}")
    # Final debug recursion
    def print_keys(obj, indent=0):
        for key in obj.keys():
            print('  ' * indent + str(key))
            if isinstance(obj[key], zarr.hierarchy.Group):
                print_keys(obj[key], indent + 1)
    print("\nFull Dataset Tree:")
    print_keys(root)
