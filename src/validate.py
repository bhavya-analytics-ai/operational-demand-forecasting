import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROCESSED_PATH = Path("data/processed/daily_request_counts.csv")
QA_REPORT_PATH = Path("data/processed/qa_report.txt")

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def check_missing_days(df: pd.DataFrame):
    full_range = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    missing = full_range.difference(df["date"])
    return missing

def run_basic_checks(df: pd.DataFrame):
    report = []
    report.append(f"Total days: {len(df)}")
    report.append(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    report.append(f"Duplicate dates: {df['date'].duplicated().sum()}")

    report.append("\nDaily request count summary:")
    report.append(df["daily_request_count"].describe().to_string())

    return report

def save_report(lines, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    print("Loading processed data...")
    df = load_data(PROCESSED_PATH)

    print("Running QA checks...")
    report_lines = run_basic_checks(df)

    missing_days = check_missing_days(df)
    report_lines.append(f"\nMissing days: {len(missing_days)}")

    if len(missing_days) > 0:
        report_lines.append("First 10 missing dates:")
        report_lines.extend([str(d.date()) for d in missing_days[:10]])

    save_report(report_lines, QA_REPORT_PATH)

    print("LEVEL 2 complete.")
    print(f"QA report saved to {QA_REPORT_PATH}")
