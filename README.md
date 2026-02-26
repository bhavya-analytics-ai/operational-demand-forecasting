#  Operational Forecasting & Monitoring System (NYC 311)

Decision-focused time-series forecasting system designed to support operational and capacity planning using NYC 311 demand data.

This project prioritizes **decision quality, baseline rigor, and monitoring** over model complexity.

---

##  Decision Framing (Level 0)

The system is built around a concrete operational question:

> What level of demand should operations plan for?

Two decision targets were explicitly evaluated:

- Next-day demand (short-term responsiveness)  
- 7-day average demand (capacity and staffing planning)  

All modeling choices were evaluated based on **decision usefulness**, not predictive novelty.

---

## ☁️ Data Ingestion & Storage (Level 1)

- Source: NYC 311 service request data (2023–2024)  
- Raw data stored in AWS S3 as the system of record  
- Local workflows operate on derived, reproducible datasets only  

This separation avoids coupling modeling logic to raw ingestion.

---

##  Data Validation & Quality Checks (Level 2)

Before modeling, the pipeline enforces explicit data quality checks:

- Date parsing and ordering validation  
- Duplicate detection  
- Missing-day detection and reporting  
- QA summary generated for traceability  

No modeling is performed until validation passes.

---

##  Feature Engineering (Level 3)

Time-series features constructed from daily request counts:

- Lag features: 1, 7, 14 days  
- Rolling statistics: mean and standard deviation (7, 14)  
- Calendar features: day of week, week of year  

All features are generated deterministically and stored as processed artifacts.

---

## 📊 Baseline Modeling (Level 4)

Baseline models are treated as first-class candidates.

### Results

- Next-day demand (lag-1 baseline):  
  MAE ~ 926  

- 7-day average demand (rolling mean, 7 days):  
  MAE ~ 281  

The 7-day rolling baseline achieved low error relative to operational scale.

---

## 🌲 Gradient Boosting Benchmark (Level 5)

A Gradient Boosting model was implemented and evaluated using:

- The same feature set  
- Identical splits  
- Identical evaluation logic  

### Result

Gradient Boosting did not outperform baseline models for either decision target.

The ML model is retained as a benchmark, not selected for production use.

---

##  Error Analysis & Model Selection (Level 6)

Analysis showed:

- Strong short-term autocorrelation in demand  
- Rolling averages captured the dominant signal  
- Added model complexity did not reduce decision-level error  

The baseline model was intentionally selected as the operational model.

---

## 🚦 Forecast Monitoring (Level 7)

Forecast reliability is monitored using rolling error metrics:

- Rolling MAE computed over a 28-day window  
- Thresholds defined relative to baseline MAE  
- Status states:
  - OK  
  - WARN  
  - ALERT  

This enables early detection of degradation without immediate retraining.

---

## 📈 Decision View & Interpretation (Level 8)

A decision-oriented notebook visualizes:

- Actual vs forecasted demand (7-day average)  
- Rolling MAE trends over time  
- Current system status relative to thresholds  

The output is designed for **operational interpretation**, not model debugging.

---

## 🗂 Repository Structure
```
operational-demand-forecasting/
├── data/
│ └── processed/
├── src/
│ ├── download_raw.py
│ ├── aggregate.py
│ ├── validate.py
│ ├── features.py
│ ├── baseline.py
│ ├── baseline_7day.py
│ ├── train_gb.py
│ ├── monitor_7day.py
├── notebooks/
│ └── level8_decision_view.ipynb
├── README.md
└── requirements.txt
```

---

## ▶️ Reproducibility

1. Install dependencies
```
pip install -r requirements.txt
```

2. Run monitoring logic
```
python src/monitor_7day.py
```

Raw data is expected to be sourced from AWS S3.

---

## ✅ Key Takeaways

- Decision framing determines what “good performance” means  
- Simple baselines can outperform ML for operational planning  
- Monitoring is as important as model choice  
- ML was evaluated and intentionally rejected when it did not improve decisions


---

## Author

**Bhavya Pandya**  
LinkedIn: https://www.linkedin.com/in/bhavya-91p/

