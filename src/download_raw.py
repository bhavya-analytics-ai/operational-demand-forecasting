import pandas as pd
from pathlib import Path
from urllib.parse import urlencode
import boto3

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = OUT_DIR / "nyc_311_2023_2024_raw.csv"

# 🔁 CHANGE THESE
S3_BUCKET = "your-bucket-name"
S3_KEY = "raw/nyc_311_2023_2024_raw.csv"

s3 = boto3.client("s3")


def build_url(start, end):
    query = {
        "$where": f"created_date >= '{start}' AND created_date < '{end}'",
        "$limit": 200000
    }
    return f"{BASE_URL}?{urlencode(query)}"


def download_month(year, month):
    start = f"{year}-{month:02d}-01T00:00:00"
    end = (
        f"{year+1}-01-01T00:00:00"
        if month == 12
        else f"{year}-{month+1:02d}-01T00:00:00"
    )

    print(f"Downloading {year}-{month:02d}")
    url = build_url(start, end)
    return pd.read_csv(url, low_memory=False)


def upload_to_s3(local_path):
    print("Uploading to S3...")
    s3.upload_file(str(local_path), S3_BUCKET, S3_KEY)
    print("Upload complete")


def main():
    dfs = []

    for year in [2023, 2024]:
        for month in range(1, 13):
            df = download_month(year, month)
            if not df.empty:
                dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)
    full_df.to_csv(RAW_FILE, index=False)

    print(f"Saved locally: {len(full_df)} rows")
    upload_to_s3(RAW_FILE)


if __name__ == "__main__":
    main()
