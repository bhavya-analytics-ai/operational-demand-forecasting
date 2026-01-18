import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
INPUT_PATH = Path("data/processed/daily_request_counts.csv")
OUTPUT_PATH = Path("data/processed/daily_request_counts_filled.csv")

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").set_index("date")
    return df

def fill_missing_days(df: pd.DataFrame) -> pd.DataFrame:
    # Create full daily date range
    full_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    # Reindex to full range
    df = df.reindex(full_index)

    # Fill missing days with zero demand
    df["daily_request_count"] = (
        df["daily_request_count"]
        .fillna(0)
        .astype(int)
    )

    df.index.name = "date"
    df = df.reset_index()

    return df

def main():
    print("Loading aggregated data...")
    df = load_data(INPUT_PATH)

    print("Filling missing days with zero demand...")
    filled_df = fill_missing_days(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    filled_df.to_csv(OUTPUT_PATH, index=False)

    print("LEVEL 2.5 complete.")
    print(f"Saved to {OUTPUT_PATH}")
    print(f"Total days after fix: {len(filled_df)}")

if __name__ == "__main__":
    main()
