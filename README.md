# ContinuumSC: Continuous Operations Platform

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/-Streamlit-05122A?style=flat&logo=streamlit)
![XGBoost](https://img.shields.io/badge/-XGBoost-05122A?style=flat)

ContinuumSC is an end-to-end MLOps intelligence system designed to optimize supply chain operations through continuous machine learning. The platform automates demand forecasting and inventory optimization using a sleek, interactive command center.

<!-- A screenshot or short GIF of the dashboard belongs here: it is the single
     biggest factor in whether a visitor explores the repo. Save one as
     docs/screenshot.png and uncomment the line below.
![ContinuumSC dashboard](docs/screenshot.png)
-->

## Features

- **Demand forecasting** — XGBoost with time-series feature engineering, predicting future product demand from historical trends, seasonality and lags.
- **Inventory optimization** — calculates Safety Stock and Reorder Points using standard service-level formulas.
- **Interactive dashboard** — a modern, dark-themed Streamlit UI with clear visualisations and operational controls.
- **Custom data ingestion** — upload your own CSV or Excel supply chain data, or use the built-in generator to try the platform with simulated data.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SaadTadja/continuumsc.git
   cd continuumsc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

No configuration is required for a first run — if you do not upload a file, the
built-in generator produces a simulated dataset so the dashboard is populated
immediately.

## Custom data schema

If you upload your own data via the **Upload CSV/Excel** sidebar tool, it should
contain the following columns:

| Column | Type | Meaning |
|---|---|---|
| `Date` | datetime / string | Timestamp of the record |
| `Product_ID` | string | Unique product identifier |
| `Demand` | integer / float | Daily demand volume |
| `Lead_Time` | integer / float | Lead time to replenish stock |
| `Unit_Cost` | float | Cost per unit |
| `Holding_Cost_Rate` | float | Share of unit cost to hold inventory |

## Project structure

```
app.py                    main Streamlit dashboard
src/engine.py             forecasting and optimization logic (XGBoost)
src/data_generator.py     simulated data when no file is provided
src/styles.py             custom UI styling
.streamlit/config.toml    theme configuration
```

## License

MIT — see [LICENSE](LICENSE).
