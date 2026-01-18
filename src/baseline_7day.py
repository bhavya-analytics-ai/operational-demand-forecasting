import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

INPUT_PATH = Path("data/processed/target_7day_avg.csv")

def load_data(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

def run_baselines(df):
    y_true = df["target_7day_avg"]

    preds = {
        # common sense baselines
        "naive_lag_1": df["daily_request_count"],              # yesterday as proxy
        "rolling_mean_7": df["daily_request_count"].rolling(7).mean()
    }

    results = {}
    for name, y_pred in preds.items():
        valid = ~y_pred.isna()
        mae = mean_absolute_error(y_true[valid], y_pred[valid])
        rmse = np.sqrt(mean_squared_error(y_true[valid], y_pred[valid]))
        results[name] = {"MAE": mae, "RMSE": rmse}

    return results

if __name__ == "__main__":
    df = load_data(INPUT_PATH)
    results = run_baselines(df)

    print("\nLEVEL 4 — Baseline (7-day avg target)")
    for model, metrics in results.items():
        print(f"{model}: MAE={metrics['MAE']:.2f}, RMSE={metrics['RMSE']:.2f}")
