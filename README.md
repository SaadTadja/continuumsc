# ContinuumSC: Continuous Operations Platform

ContinuumSC is an end-to-end MLOps intelligence system designed to optimize supply chain operations through continuous machine learning. The platform automates demand forecasting and inventory optimization using a sleek, interactive command center.

## Features
- **Demand Forecasting**: Uses XGBoost and time-series feature engineering to predict future product demand based on historical trends, seasonality, and lags.
- **Inventory Optimization**: Automatically calculates Safety Stock and Reorder Points using standard service-level formulas.
- **Interactive Dashboard**: A modern, dark-themed Streamlit UI providing clear data visualizations and operational controls.
- **Custom Data Ingestion**: Upload your own CSV or Excel supply chain data, or use the built-in data generator to test the platform.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/continuumsc.git
   cd continuumsc
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Custom Data Schema
If you choose to upload your own data via the "Upload CSV/Excel" sidebar tool, please ensure it contains the following columns:

- `Date`: (Datetime/String) The timestamp of the record.
- `Product_ID`: (String) Unique identifier for the product.
- `Demand`: (Integer/Float) The daily demand volume.
- `Lead_Time`: (Integer/Float) The lead time required to replenish stock.
- `Unit_Cost`: (Float) Cost per unit.
- `Holding_Cost_Rate`: (Float) The percentage of unit cost to hold inventory.

## Project Structure
- `app.py`: Main Streamlit dashboard application.
- `src/engine.py`: Machine learning and optimization logic (XGBoost).
- `src/data_generator.py`: Generates simulation data if no file is provided.
- `src/styles.py`: Custom UI stylings.
- `.streamlit/config.toml`: Global theme configuration.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
