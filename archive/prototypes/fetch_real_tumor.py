import requests
import os

# A specific file_id for a TCGA BRCA Diagnostic Slide
# This is a public, open-access ID
FILE_ID = "0005958a-36b6-4f91-8d5c-9e320d367c33" 

def download_tcga_sample():
    print(f"Connecting to NIH Genomic Data Commons...")
    # Using the GDC Data endpoint
    url = f"https://api.gdc.cancer.gov/data/{FILE_ID}"
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        
        if response.status_code == 200:
            print("Downloading slide fragment (this may take a moment)...")
            with open("real_tumor_sample.svs", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("Success: real_tumor_sample.svs downloaded.")
        else:
            print(f"Error accessing GDC: Status Code {response.status_code}")
            print("Note: Some TCGA files require controlled access, but this ID is typically Open.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_tcga_sample()
