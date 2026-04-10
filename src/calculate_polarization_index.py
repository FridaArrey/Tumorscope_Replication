import numpy as np
import cv2

def calculate_synaptic_score(t_cell_mask, tumor_mask):
    """
    Translates Lemaitre $Z_0$ and $Z_1$ logic into a 2D Spatial Score.
    $Z_0$ = Synapse Plan (Distance to Tumor)
    $Z_1$ = Synaptic Dome (Centroid Displacement/Eccentricity)
    """
    # 1. Find Centroids
    M = cv2.moments(t_cell_mask)
    if M["m00"] == 0: return "INVALID"
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    # 2. Measure distance to nearest Tumor edge (The $Z_0$ Equivalent)
    # We use distanceTransform to find how far the T-cell is from the "Shore"
    dist_map = cv2.distanceTransform(cv2.bitwise_not(tumor_mask), cv2.DIST_L2, 5)
    dist_to_tumor = dist_map[cY, cX]
    
    # 3. Calculate Eccentricity (Is the cell polarized?)
    contours, _ = cv2.findContours(t_cell_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0: return "INVALID"
    
    # Need at least 5 points for an ellipse
    if len(contours[0]) >= 5:
        ellipse = cv2.fitEllipse(contours[0])
        (center, axes, angle) = ellipse
        major_axis = max(axes)
        minor_axis = min(axes)
        eccentricity = np.sqrt(1 - (minor_axis**2 / major_axis**2))
    else:
        eccentricity = 0 # Round cells aren't polarized
    
    # 4. Triage Logic
    if dist_to_tumor < 15 and eccentricity > 0.75:
        return "ACTIVE_SYNAPSE"
    elif dist_to_tumor >= 15 and eccentricity > 0.75:
        return "FRUSTRATED_EXCLUDED"
    else:
        return "DESERT_OR_INACTIVE"

# Test logic with dummy data to verify it works
if __name__ == "__main__":
    print("Testing Polarization Bridge Logic...")
    # Create a 100x100 dummy environment
    test_tumor = np.zeros((100, 100), dtype=np.uint8)
    test_tumor[0:20, :] = 255 # Tumor is at the top
    
    # Create an elongated T-cell (Polarized)
    test_t_cell = np.zeros((100, 100), dtype=np.uint8)
    cv2.ellipse(test_t_cell, (50, 50), (20, 5), 90, 0, 360, 255, -1)
    
    result = calculate_synaptic_score(test_t_cell, test_tumor)
    print(f"Test Result for 50px distance: {result}")
    
    # Move T-cell closer to tumor
    test_t_cell_close = np.zeros((100, 100), dtype=np.uint8)
    cv2.ellipse(test_t_cell_close, (50, 25), (20, 5), 90, 0, 360, 255, -1)
    result_close = calculate_synaptic_score(test_t_cell_close, test_tumor)
    print(f"Test Result for 5px distance: {result_close}")
