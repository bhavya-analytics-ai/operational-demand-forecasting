# Operational Forecasting & Monitoring System
### NYC 311 demand forecasting - where the baseline beat the ML model, and that was the right call.

![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Gradient%20Boosting%20%7C%20AWS%20S3-3776AB?style=flat&logo=python&logoColor=white)
![Data](https://img.shields.io/badge/Data-NYC%20311%202023--2024-orange?style=flat)
![Status](https://img.shields.io/badge/Status-Level%208%20Complete-brightgreen?style=flat)

---

## What This Is

A decision-focused time-series forecasting system for operational and capacity planning using NYC 311 service request data. Built around one concrete question:

> What level of demand should operations plan for?

This project prioritizes **decision quality, baseline rigor, and monitoring** over model complexity - and the results justify that choice.

---

## The Key Result

Gradient Boosting did not outperform the baseline. The baseline was intentionally selected as the production model.

| Model | Target | MAE |
|-------|--------|-----|
| Lag-1 Baseline | Next-day demand | ~926 |
| 7-day Rolling Mean | 7-day average demand | ~281 |
| Gradient Boosting | Both targets | Worse than baseline |

Strong short-term autocorrelation in 311 demand means rolling averages already capture the dominant signal. Added complexity didn't reduce decision-level error - so it wasn't added.

---

## System Levels

### Level 0 - Decision Framing
Two decision targets defined upfront before any modeling:

- Next-day demand - short-term operational responsiveness
- 7-day average demand - capacity and staffing planning

All modeling choices evaluated on decision usefulness, not predictive novelty.

### Level 1 - Data Ingestion & Storage
NYC 311 service request data (2023-2024) sourced and stored in AWS S3 as the system of record. Local workflows operate on derived, reproducible datasets only - modeling logic never touches raw ingestion.

### Level 2 - Data Validation & Quality Checks
Hard QA gate before any modeling runs:

- Date parsing and ordering validation
- Duplicate detection
- Missing-day detection and reporting
- QA summary generated for traceability

### Level 3 - Feature Engineering
Deterministic time-series features from daily request counts:

- Lag features: 1, 7, 14 days
- Rolling mean and std: 7 and 14-day windows
- Calendar features: day of week, week of year

### Level 4 - Baseline Modeling
Baselines treated as first-class candidates, not throwaway comparisons. Both selected for production use after Level 5 evaluation.

### Level 5 - Gradient Boosting Benchmark
Same feature set, same splits, same evaluation logic as baseline. Gradient Boosting evaluated and rejected - it didn't improve decisions, so it doesn't ship.

### Level 6 - Error Analysis & Model Selection
Confirmed that rolling averages capture the dominant autocorrelation signal. Complexity budget spent on monitoring instead.

### Level 7 - Forecast Monitoring
Rolling MAE over a 28-day window with explicit thresholds:

- `OK` - within baseline error range
- `WARN` - degrading, watch closely
- `ALERT` - retraining or intervention needed

Early degradation detection without immediate retraining.

### Level 8 - Decision View
Operational notebook showing actual vs forecasted demand, rolling MAE trends, and current system status. Designed for operational interpretation, not model debugging.

---

## Reproducibility

```bash
pip install -r requirements.txt
python src/monitor_7day.py
```

Raw data sourced from AWS S3.

---

## Repo Structure

```
operational-demand-forecasting/
├── data/
│   └── processed/
├── src/
│   ├── download_raw.py
│   ├── aggregate.py
│   ├── validate.py
│   ├── features.py
│   ├── baseline.py
│   ├── baseline_7day.py
│   ├── train_gb.py
│   └── monitor_7day.py
├── notebooks/
│   └── level8_decision_view.ipynb
├── requirements.txt
└── README.md
```

---

**Bhavya Pandya** · [LinkedIn](https://www.linkedin.com/in/bhavya-91p/) · M.S. Data Analytics, LIU Brooklyn
