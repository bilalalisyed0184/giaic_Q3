import json
import os
import streamlit as st

# Define a fallback default conversion data
default_conversion_data = {
    "Length": {
        "Meter": 1,
        "Kilometer": 1000,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254
    },
    "Mass": {
        "Kilogram": 1,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.453592,
        "Ounce": 0.0283495
    }
}

# Try to load the JSON file, otherwise use default data
conversion_data = default_conversion_data
if os.path.exists("conversion_data.json"):
    with open("conversion_data.json", "r") as f:
        conversion_data = json.load(f)

# Conversion function
def convert_value(value, from_unit, to_unit, category):
    if from_unit in conversion_data[category] and to_unit in conversion_data[category]:
        return value * (conversion_data[category][to_unit] / conversion_data[category][from_unit])
    return "Conversion not available"

# Formula display function
def get_formula(from_unit, to_unit, category, from_value, to_value):
    return f"{from_value} {from_unit} × (conversion factor) = {to_value} {to_unit}"

# Detailed explanation function
def get_conversion_details(from_unit, to_unit, category, from_value, to_value):
    return f"Converting {from_value} {from_unit} to {to_unit} based on standard conversion factors."

# Main App UI
st.markdown("<h1 class='main-header'>Multi-Unit Converter</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Convert between different units of measurement</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Categories")
    category = st.selectbox("Select category", list(conversion_data.keys()), label_visibility="collapsed")

with col2:
    st.markdown("<div class='category-card'>", unsafe_allow_html=True)
    st.markdown(f"### {category} Conversion")
    
    col_from, col_equal, col_to = st.columns([2, 1, 2])
    
    with col_from:
        from_unit = st.selectbox("From", list(conversion_data[category].keys()), key="from_unit")
        from_value = st.number_input("Enter value", value=1.0, format="%.8f", key="from_value")
    
    with col_equal:
        st.markdown("<div style='text-align: center; font-size: 2rem; margin-top: 1.7rem;'>=</div>", unsafe_allow_html=True)
    
    with col_to:
        to_unit = st.selectbox("To", list(conversion_data[category].keys()), key="to_unit")
        to_value = convert_value(from_value, from_unit, to_unit, category)
        
        precision = 2 if category in ["Temperature", "Fuel Economy"] else 4
        if isinstance(to_value, float):
            st.markdown(f"<div class='value-display'>{to_value:.{precision}f}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='value-display'>{to_value}</div>", unsafe_allow_html=True)
    
    formula = get_formula(from_unit, to_unit, category, from_value, to_value)
    st.markdown(f"<div class='formula-box'><strong>Formula:</strong> {formula}</div>", unsafe_allow_html=True)
    
    detailed_explanation = get_conversion_details(from_unit, to_unit, category, from_value, to_value)
    st.markdown(f"<div class='conversion-details'><strong>Details:</strong>\n{detailed_explanation}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Developed by Syed Bilal Ali Shah | © 2025 Multi-Unit Converter</div>", unsafe_allow_html=True)
