import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# -----------------------------
# Paths
# -----------------------------
INPUT_PATH = Path("data/processed/features.csv")

# -----------------------------
# Load data
# -----------------------------
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

# -----------------------------
# Baseline models
# -----------------------------
def run_baselines(df: pd.DataFrame):
    y_true = df["daily_request_count"]

    preds = {
        "naive_lag_1": df["lag_1"],           # tomorrow = yesterday
        "rolling_mean_7": df["roll_mean_7"], # tomorrow = last 7-day avg
    }

    results = {}

    for name, y_pred in preds.items():
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        results[name] = {"MAE": mae, "RMSE": rmse}

    return results

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("Loading feature data...")
    df = load_data(INPUT_PATH)

    print("Running baseline models...")
    results = run_baselines(df)

    print("\nLEVEL 4 — Baseline Results")
    for model, metrics in results.items():
        print(f"{model}: MAE={metrics['MAE']:.2f}, RMSE={metrics['RMSE']:.2f}")
