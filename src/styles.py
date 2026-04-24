import streamlit as st

def apply_custom_styles():
    """
    Applies custom CSS for elements not covered by Streamlit's config.toml theme.
    """
    st.markdown("""
        <style>
        /* General Styles */
        .main {
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #3b82f6 !important; /* blue-500 */
            font-size: 2rem !important;
            font-weight: 700;
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important; /* slate-400 */
            font-size: 1rem;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
            color: white !important;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)
