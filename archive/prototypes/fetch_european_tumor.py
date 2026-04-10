import requests

# Targeting a sample tile from a European-based open-access pathology resource
# This is a sample H&E tile representative of European breast cancer cohorts
URL = "https://zenodo.org/record/4034515/files/sample_he_tile.png?download=1"

def download_euro_sample():
    print("Connecting to European Open Science nodes...")
    try:
        response = requests.get(URL, stream=True, timeout=20)
        if response.status_code == 200:
            with open("euro_brca_sample.png", "wb") as f:
                f.write(response.content)
            print("Success: euro_brca_sample.png downloaded.")
        else:
            print(f"Failed to fetch. Status: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    download_euro_sample()
