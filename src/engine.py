import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import norm

class SupplyChainEngine:
    def __init__(self):
        self.models = {}
        self.metrics = {}
        
    def prepare_features(self, df):
        """Creates time series features for demand forecasting."""
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by=['Product_ID', 'Date'])
        
        # Lags
        df['Demand_Lag_1'] = df.groupby('Product_ID')['Demand'].shift(1)
        df['Demand_Lag_7'] = df.groupby('Product_ID')['Demand'].shift(7)
        
        # Rolling averages
        df['Demand_Roll_7'] = df.groupby('Product_ID')['Demand'].transform(lambda x: x.rolling(7).mean())
        
        # Time features
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        df['Month'] = df['Date'].dt.month
        
        df = df.dropna()
        return df

    def train_models(self, df):
        """Trains an XGBoost model for each product to predict demand."""
        df_feat = self.prepare_features(df)
        products = df_feat['Product_ID'].unique()
        
        features = ['Demand_Lag_1', 'Demand_Lag_7', 'Demand_Roll_7', 'DayOfWeek', 'Month']
        target = 'Demand'
        
        for prod in products:
            prod_df = df_feat[df_feat['Product_ID'] == prod]
            
            X = prod_df[features]
            y = prod_df[target]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
            model.fit(X_train, y_train)
            
            preds = model.predict(X_test)
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            
            self.models[prod] = model
            self.metrics[prod] = {'MAE': mae, 'R2': r2}
            
        return self.metrics

    def predict_demand(self, df, days_ahead=7):
        """Predicts future demand for the given dataframe."""
        df_feat = self.prepare_features(df)
        products = df_feat['Product_ID'].unique()
        
        predictions = {}
        
        for prod in products:
            if prod in self.models:
                prod_df = df_feat[df_feat['Product_ID'] == prod]
                
                # Take the last row to predict the next day
                last_row = prod_df.iloc[-1:]
                X_pred = last_row[['Demand_Lag_1', 'Demand_Lag_7', 'Demand_Roll_7', 'DayOfWeek', 'Month']]
                
                pred = self.models[prod].predict(X_pred)[0]
                predictions[prod] = max(0, int(pred)) # Ensure non-negative
                
        return predictions

    def optimize_inventory(self, df, service_level=0.95):
        """
        Calculates Safety Stock and Reorder Point.
        Uses standard inventory optimization formulas.
        """
        optimization_results = []
        products = df['Product_ID'].unique()
        
        # Z-score for the desired service level
        z_score = norm.ppf(service_level)
        
        for prod in products:
            prod_df = df[df['Product_ID'] == prod]
            
            avg_demand = prod_df['Demand'].mean()
            std_demand = prod_df['Demand'].std()
            
            avg_lead_time = prod_df['Lead_Time'].mean()
            std_lead_time = prod_df['Lead_Time'].std()
            
            # Safety Stock Calculation
            # SS = Z * sqrt( (Avg_Lead_Time * Std_Demand^2) + (Avg_Demand^2 * Std_Lead_Time^2) )
            term1 = avg_lead_time * (std_demand ** 2)
            term2 = (avg_demand ** 2) * (std_lead_time ** 2)
            safety_stock = z_score * np.sqrt(term1 + term2)
            
            # Reorder Point (ROP) = (Avg Demand * Avg Lead Time) + Safety Stock
            rop = (avg_demand * avg_lead_time) + safety_stock
            
            optimization_results.append({
                'Product_ID': prod,
                'Average_Demand': round(avg_demand, 2),
                'Average_Lead_Time': round(avg_lead_time, 2),
                'Safety_Stock': int(safety_stock),
                'Reorder_Point': int(rop)
            })
            
        return pd.DataFrame(optimization_results)
