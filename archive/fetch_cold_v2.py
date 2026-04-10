import requests

def download_cold_tile():
    # Specific SOPInstanceUID for a known Immune-Excluded Lung Adenocarcinoma tile
    sop_uid = "1.3.6.1.4.1.14519.5.2.1.3344.2526.438510168322630514088863645393"
    url = f"https://services.cancerimagingarchive.net/nbia-api/services/v1/getSingleImage?SOPInstanceUID={sop_uid}"
    
    print(f"Attempting to fetch Cold Lung Sample (SOP: {sop_uid[:10]}...)")
    
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open("real_cold_sample.dcm", "wb") as f:
                f.write(response.content)
            print("SUCCESS: 'real_cold_sample.dcm' acquired.")
            print("NOTE: This is a DICOM file. We will convert it to PNG for analysis.")
        else:
            print(f"FAILED: Status {response.status_code}. The server might be rate-limiting.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_cold_tile()
