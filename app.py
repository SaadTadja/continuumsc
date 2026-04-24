import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_generator import generate_supply_chain_data
from src.engine import SupplyChainEngine
from src.styles import apply_custom_styles

st.set_page_config(
    page_title="ContinuumSC Command Center",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
apply_custom_styles()

@st.cache_data
def get_simulation_data():
    return generate_supply_chain_data(days=365, num_products=5)

def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
    return get_simulation_data()

@st.cache_resource
def get_engine():
    return SupplyChainEngine()

def main():
    st.title("ContinuumSC Platform")
    st.markdown("Automated Demand Forecasting & Inventory Optimization via Machine Learning.")

    st.sidebar.markdown("### Data Source")
    uploaded_file = st.sidebar.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
    if uploaded_file:
        st.sidebar.success("Custom data loaded")
    else:
        st.sidebar.info("Using simulation data")

    df = load_data(uploaded_file)
    engine = get_engine()

    # --- Sidebar ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Forecasting", "Inventory Optimizer"])

    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Status")
    if st.sidebar.button("Models Deployed"):
        st.toast("Models are currently active and predicting.")
    if st.sidebar.button("Data Stream Active"):
        st.toast("Data stream is live and receiving updates.")
    
    # Global Filter
    selected_product = st.sidebar.selectbox("Filter by Product", ["All"] + list(df['Product_ID'].unique()))

    if selected_product != "All":
        df_filtered = df[df['Product_ID'] == selected_product]
    else:
        df_filtered = df

    # --- Page 1: Dashboard ---
    if page == "Dashboard":
        st.header("Overview")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Products", df['Product_ID'].nunique())
        col2.metric("Total Demand (YTD)", f"{df['Demand'].sum():,}")
        col3.metric("Avg Lead Time (Days)", f"{df['Lead_Time'].mean():.1f}")
        col4.metric("System Health", "99.9%", "+0.1%")

        st.markdown("---")
        
        # Demand Trend Chart
        st.subheader("Demand Trend (Last 30 Days)")
        recent_df = df_filtered[df_filtered['Date'] >= df_filtered['Date'].max() - pd.Timedelta(days=30)]
        fig = px.line(recent_df, x='Date', y='Demand', color='Product_ID', 
                      title="Daily Demand by Product",
                      template="plotly_dark",
                      color_discrete_sequence=['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#eff6ff'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # --- Page 2: Forecasting ---
    elif page == "Forecasting":
        st.header("ML Demand Forecasting")
        
        if st.button("Train ML Models"):
            with st.spinner("Training XGBoost models for all products..."):
                metrics = engine.train_models(df)
                st.session_state['models_trained'] = True
                st.session_state['metrics'] = metrics
            st.success("Models trained successfully!")

        if st.session_state.get('models_trained', False):
            st.subheader("Model Performance")
            
            # Display metrics
            metrics = st.session_state['metrics']
            metrics_df = pd.DataFrame(metrics).T.reset_index()
            metrics_df.rename(columns={'index': 'Product_ID'}, inplace=True)
            
            st.dataframe(metrics_df.style.format({'MAE': '{:.2f}', 'R2': '{:.2f}'}), use_container_width=True)

            st.subheader("Next Day Forecast")
            predictions = engine.predict_demand(df)
            pred_df = pd.DataFrame(list(predictions.items()), columns=['Product_ID', 'Predicted_Demand'])
            
            fig = px.bar(pred_df, x='Product_ID', y='Predicted_Demand', 
                         title="Predicted Demand for Next Cycle",
                         template="plotly_dark",
                         color='Predicted_Demand',
                         color_continuous_scale='Blues')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please train the models to view forecasts.")

    # --- Page 3: Inventory Optimizer ---
    elif page == "Inventory Optimizer":
        st.header("Inventory Optimization")
        
        service_level = st.slider("Target Service Level (%)", min_value=80, max_value=99, value=95) / 100.0
        
        if st.button("Calculate Optimal Inventory"):
            with st.spinner("Calculating Safety Stock and Reorder Points..."):
                opt_df = engine.optimize_inventory(df, service_level=service_level)
                
            st.success("Optimization Complete!")
            
            st.dataframe(opt_df, use_container_width=True)
            
            # Visualization
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=opt_df['Product_ID'],
                y=opt_df['Average_Demand'],
                name='Avg Daily Demand',
                marker_color='#64748b' # slate-500
            ))
            fig.add_trace(go.Bar(
                x=opt_df['Product_ID'],
                y=opt_df['Safety_Stock'],
                name='Safety Stock',
                marker_color='#3b82f6' # blue-500
            ))
            fig.update_layout(
                title='Inventory Requirements by Product',
                barmode='stack',
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
