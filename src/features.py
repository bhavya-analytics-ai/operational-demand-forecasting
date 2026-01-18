import pandas as pd
from pathlib import Path

# Paths
INPUT_PATH = Path("data/processed/daily_request_counts_filled.csv")
OUTPUT_PATH = Path("data/processed/features.csv")

# Load data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

# Feature engineering
def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Target
    y = df["daily_request_count"]

    # Lag features
    df["lag_1"] = y.shift(1)
    df["lag_7"] = y.shift(7)
    df["lag_14"] = y.shift(14)

    # Rolling stats
    df["roll_mean_7"] = y.rolling(7).mean()
    df["roll_std_7"] = y.rolling(7).std()
    df["roll_mean_14"] = y.rolling(14).mean()
    df["roll_std_14"] = y.rolling(14).std()

    # Calendar features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    # Drop rows with NaNs from lags/rolling
    df = df.dropna().reset_index(drop=True)

    return df

# Save features
def save_features(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

# Main
if __name__ == "__main__":
    print("Loading filled daily data...")
    df = load_data(INPUT_PATH)

    print("Creating features...")
    feat_df = make_features(df)

    print(f"Saving features to {OUTPUT_PATH}...")
    save_features(feat_df, OUTPUT_PATH)

    print("LEVEL 3 complete.")
    print(feat_df.head())
    print(f"Rows: {len(feat_df)}")
