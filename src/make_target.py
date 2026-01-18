import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/daily_request_counts_filled.csv")
OUTPUT_PATH = Path("data/processed/target_7day_avg.csv")

if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 7-day forward average target
    df["target_7day_avg"] = (
        df["daily_request_count"]
        .shift(-1)
        .rolling(window=7)
        .mean()
    )

    df = df.dropna().reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("New target created:")
    print(df[["date", "daily_request_count", "target_7day_avg"]].head())
