import streamlit as st
import pandas as pd
import json
from functools import lru_cache

# Load conversion data
with open("conversion_data.json", "r") as f:
    conversion_data = json.load(f)

st.set_page_config(page_title="Multi-Unit Converter", layout="wide")

# Caching function for performance optimization
@lru_cache(maxsize=128)
def convert_value(value, from_unit, to_unit, category):
    if from_unit == to_unit:
        return value
    
    from_factor = conversion_data[category].get(from_unit, 1)
    to_factor = conversion_data[category].get(to_unit, 1)
    return round(value * (from_factor / to_factor), 6)

# Elegant UI Styling
st.markdown(
    """
    <style>
        body { font-family: 'Inter', sans-serif; }
        .main-header { text-align: center; font-size: 2.5rem; font-weight: bold; }
        .sub-header { text-align: center; font-size: 1.3rem; color: #555; }
        .container { background: #f9f9f9; padding: 20px; border-radius: 10px; }
        .category-card { padding: 20px; border-radius: 10px; background: #ffffff; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
        .value-display { font-size: 2rem; font-weight: bold; color: #007bff; text-align: center; }
        .formula-box { background: #eef2ff; padding: 10px; border-radius: 8px; }
        .conversion-details { background: #f1f1f1; padding: 15px; border-radius: 8px; }
        .footer { text-align: center; padding: 10px; font-size: 0.9rem; color: #777; }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<h1 class='main-header'>Multi-Unit Converter</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Convert between different units effortlessly</p>", unsafe_allow_html=True)

# UI Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Select Category")
    category = st.selectbox("Category", list(conversion_data.keys()), label_visibility="collapsed")

with col2:
    st.markdown(f"<div class='category-card'><h3>{category} Conversion</h3>", unsafe_allow_html=True)
    col_from, col_equal, col_to = st.columns([2, 1, 2])

    with col_from:
        from_unit = st.selectbox("From", list(conversion_data[category].keys()), key="from_unit")
        from_value = st.number_input("Value", value=1.0, format="%.6f", key="from_value")

    with col_equal:
        st.markdown("<div style='text-align: center; font-size: 2rem; margin-top: 1.7rem;'>=</div>", unsafe_allow_html=True)

    with col_to:
        to_unit = st.selectbox("To", list(conversion_data[category].keys()), key="to_unit")
        to_value = convert_value(from_value, from_unit, to_unit, category)

        precision = 2 if category in ["Temperature", "Fuel Economy"] else 4
        st.markdown(f"<div class='value-display'>{to_value:.{precision}f}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Developed by Syed Bilal Ali Shah | © 2025 Multi-Unit Converter</div>", unsafe_allow_html=True)
