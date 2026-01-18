# src/monitor_7day.py
"""
LEVEL 7 — Monitoring logic (rolling MAE, degradation thresholds)

Monitors reliability of the selected production forecast:
- Target: 7-day average demand
- Forecast: yesterday's 7-day average (persistence baseline)

Input CSV:
- data/processed/daily_request_counts_filled.csv
  Columns REQUIRED:
    - date
    - daily_request_count
"""

import pandas as pd
from pathlib import Path

# CONFIG
INPUT_FILE = Path("data/processed/daily_request_counts_filled.csv")

ROLL_TARGET_WINDOW = 7        # 7-day average demand
ROLLING_MAE_WINDOW = 28       # monitoring window

OK_MULT = 1.15
WARN_MULT = 1.35
# -----------------------


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"File not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    # Explicit columns 
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Daily demand
    df["requests"] = df["daily_request_count"]

    # 7-day average demand (target)
    df["y_true_7day"] = df["requests"].rolling(ROLL_TARGET_WINDOW).mean()

    # Baseline forecast = yesterday's 7-day average
    df["y_pred"] = df["y_true_7day"].shift(1)

    # Absolute error
    df["abs_error"] = (df["y_true_7day"] - df["y_pred"]).abs()

    # Rolling MAE for monitoring
    df["rolling_mae"] = df["abs_error"].rolling(ROLLING_MAE_WINDOW).mean()

    # Baseline MAE reference
    baseline_mae = df["abs_error"].mean()

    ok_thresh = baseline_mae * OK_MULT
    warn_thresh = baseline_mae * WARN_MULT

    # Status flag
    def status(x):
        if pd.isna(x):
            return "NA"
        if x <= ok_thresh:
            return "OK"
        if x <= warn_thresh:
            return "WARN"
        return "ALERT"

    df["status"] = df["rolling_mae"].apply(status)

    # OUTPUT (console)
    latest = df.dropna(subset=["rolling_mae"]).tail(1)

    print(f"\nBaseline MAE reference: ~{baseline_mae:.0f}")

    if len(latest):
        row = latest.iloc[0]
        print(
            f"Latest rolling MAE ({ROLLING_MAE_WINDOW}d): ~{row['rolling_mae']:.0f} | "
            f"Status: {row['status']} | Date: {row['date'].date()}"
        )
        print(
            f"OK <= ~{ok_thresh:.0f} | WARN <= ~{warn_thresh:.0f} | ALERT > that"
        )
    else:
        print("Not enough data yet to compute rolling MAE.")

    # Optional: save output for Level 8
    out_path = Path("data/processed/monitoring_7day.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSaved monitoring output to: {out_path}")


if __name__ == "__main__":
    main()
