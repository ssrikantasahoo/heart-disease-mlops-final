import os
import pandas as pd
import requests

DATA_URL = "https://archive.ics.uci.edu/static/public/45/heart+disease.zip"
OUTPUT_DIR = "data"
CSV_PATH = os.path.join(OUTPUT_DIR, "heart.csv")

def download_dataset():
    """
    Downloads Heart Disease dataset from UCI Repository.
    Extracts and saves as heart.csv.
    Returns path to CSV.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    zip_path = os.path.join(OUTPUT_DIR, "heart.zip")

    # Download
    print("Downloading dataset...")
    r = requests.get(DATA_URL)
    with open(zip_path, "wb") as f:
        f.write(r.content)

    # Unzip
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(OUTPUT_DIR)

    # UCI dataset includes multiple files; select processed Cleveland data
    target_file = "processed.cleveland.data"
    extracted_files = os.listdir(OUTPUT_DIR)
    
    if target_file in extracted_files:
        # Read the data - it has no header
        df = pd.read_csv(os.path.join(OUTPUT_DIR, target_file), header=None)
        df.to_csv(CSV_PATH, index=False, header=False) # Keep it raw, preprocessing will add headers
        print(f"Successfully extracted {target_file}")
    else:
        # Fallback if specific file not found (unlikely with correct zip)
        print(f"Warning: {target_file} not found. Searching for .data files...")
        for file in extracted_files:
            if file.endswith(".data"):
                df = pd.read_csv(os.path.join(OUTPUT_DIR, file), header=None)
                df.to_csv(CSV_PATH, index=False, header=False)
                print(f"Used fallback file: {file}")
                break

    print(f"Dataset saved at {CSV_PATH}")
    return CSV_PATH

if __name__ == "__main__":
    download_dataset()
