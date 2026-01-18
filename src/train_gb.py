import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

# -----------------------------
# Paths
# -----------------------------
INPUT_PATH = Path("data/processed/features.csv")

# -----------------------------
# Load data
# -----------------------------
def load_data(path: Path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

# -----------------------------
# Train / test split (time-based)
# -----------------------------
def time_split(df, test_ratio=0.2):
    split_idx = int(len(df) * (1 - test_ratio))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    return train, test

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("Loading features...")
    df = load_data(INPUT_PATH)

    target = "daily_request_count"
    features = [
        "lag_1", "lag_7", "lag_14",
        "roll_mean_7", "roll_std_7",
        "roll_mean_14", "roll_std_14",
        "day_of_week", "week_of_year"
    ]

    train_df, test_df = time_split(df)

    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]

    print("Training Gradient Boosting model...")
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train, y_train)

    print("Evaluating...")
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    print("\nLEVEL 5 — Gradient Boosting Results")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
