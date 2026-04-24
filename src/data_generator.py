import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_supply_chain_data(days=365, num_products=5):
    """
    Generates supply chain data for internal simulation and testing.
    """
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    product_data = []
    
    for product_id in range(1, num_products + 1):
        # Base demand with seasonality and trend
        trend = np.linspace(0, 5, days)
        seasonality = np.sin(np.linspace(0, 4 * np.pi, days)) * 20
        noise = np.random.normal(0, 5, days)
        
        # Base demand between 50 and 200
        base_demand = np.random.randint(50, 200)
        
        daily_demand = base_demand + trend + seasonality + noise
        daily_demand = np.maximum(daily_demand, 0).astype(int) # Ensure non-negative
        
        # Inventory dynamics
        inventory = np.zeros(days)
        inventory[0] = base_demand * 5 # Initial stock
        
        # Lead times (randomized per product)
        lead_time_mean = np.random.randint(3, 10)
        lead_time_std = np.random.uniform(0.5, 2.0)
        
        df = pd.DataFrame({
            'Date': dates,
            'Product_ID': f'PROD-{product_id:03d}',
            'Demand': daily_demand,
            'Lead_Time': np.random.normal(lead_time_mean, lead_time_std, days).astype(int),
            'Unit_Cost': np.random.uniform(10.0, 50.0),
            'Holding_Cost_Rate': np.random.uniform(0.1, 0.2)
        })
        product_data.append(df)
        
    final_df = pd.concat(product_data, ignore_index=True)
    return final_df
