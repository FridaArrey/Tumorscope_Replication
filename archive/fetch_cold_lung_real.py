import requests

def download_cold_tile():
    # Target: A known low-infiltration (Immune Desert) case from the CPTAC-LUAD collection
    # Using a public manifest link for a representative "Cold" H&E/IHC tile
    url = "https://services.cancerimagingarchive.net/nbia-api/services/v1/getImage?SeriesInstanceUID=1.3.6.1.4.1.14519.5.2.1.3344.2526.126442657801844964648160052342"
    
    print("Connecting to TCIA to retrieve 'Cold' Lung Adenocarcinoma tile...")
    
    try:
        # We simulate the fetch of a specific high-exclusion region
        # In a full API flow, we would parse the DICOM, but for this lab, 
        # we target the representative JPEG transition.
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open("real_cold_luad_tile.png", "wb") as f:
                f.write(response.content)
            print("SUCCESS: 'real_cold_luad_tile.png' acquired.")
        else:
            print(f"FAILED: TCIA API returned status {response.status_code}")
    except Exception as e:
        print(f"Error fetching real cold sample: {e}")

if __name__ == "__main__":
    download_cold_tile()
