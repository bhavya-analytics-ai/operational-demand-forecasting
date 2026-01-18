# 📦 Operational Forecasting & Monitoring System

Decision-focused demand forecasting system built on NYC 311 data to support operational and capacity planning.

---

## 🎯 Decision Framing

This project is framed around a practical operational question:

What level of demand should operations plan for?

Two decision targets were evaluated:
- Next-day demand for short-term responsiveness
- 7-day average demand for staffing and capacity planning

Model selection was driven by decision usefulness, not algorithmic complexity.

---

## 🔄 Data & Pipeline

- Source: NYC 311 service request data (2023–2024)
- Raw data stored in AWS S3 (source of truth)
- Daily request counts aggregated locally
- Missing days detected and filled
- Explicit time-series feature engineering applied

Engineered features include:
- Lag features (1, 7, 14 days)
- Rolling statistics (mean and standard deviation over 7 and 14 days)
- Calendar features (day of week, week of year)

---

## 📊 Modeling & Results

Two modeling approaches were evaluated using identical data splits and features.

Baseline models:
- Next-day demand: lag-1 baseline  
  MAE ~ 926
- 7-day average demand: rolling mean (7 days)  
  MAE ~ 281

Gradient Boosting:
- Trained using the same feature set
- Evaluated under the same conditions

Result:  
Gradient Boosting did not outperform baseline models for either decision target.

---

## 🧠 Why Machine Learning Was Not Selected

Although a Gradient Boosting model was implemented and evaluated, it did not improve decision quality over simple statistical baselines.

Key observations:
- Demand showed strong short-term autocorrelation
- Rolling averages already captured the relevant signal
- Added model complexity did not reduce operational error

The baseline model was intentionally selected as the operational decision model.

---

## 🚦 Forecast Monitoring

Forecast reliability is monitored using rolling error metrics.

- Rolling MAE computed over a 28-day window
- Thresholds defined relative to baseline MAE
- Status flags: OK, WARN, ALERT

This enables early detection of forecast degradation without immediate retraining.

---

## 🗂 Repository Structure

operational-demand-forecasting/
├── data/
│   └── processed/
├── src/
│   ├── baseline.py
│   ├── train_gb.py
│   ├── monitor_7day.py
├── notebooks/
│   └── level8_decision_view.ipynb
├── README.md
└── requirements.txt

---

## ▶️ Reproducibility

1. Install dependencies  
   pip install -r requirements.txt

2. Run monitoring logic  
   python src/monitor_7day.py

Raw data is expected to be sourced from AWS S3.

---

## ✅ Key Takeaways

- Decision framing defines what good performance means
- Simple baselines can outperform ML for operational planning
- Monitoring is as important as model selection
- Model complexity was rejected when it did not improve decisions
