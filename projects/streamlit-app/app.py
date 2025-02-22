import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup our App
st.set_page_config(page_title="⚙ Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue
        
        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        
        # Show first 5 rows of the dataframe
        st.write("### Preview of Data")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            if f"cleaned_{file.name}" not in st.session_state:
                st.session_state[f"cleaned_{file.name}"] = df.copy()
                
            cleaned_df = st.session_state[f"cleaned_{file.name}"]
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    cleaned_df.drop_duplicates(inplace=True)
                    st.session_state[f"cleaned_{file.name}"] = cleaned_df
                    st.write("✅ Duplicates Removed!")
                    st.dataframe(cleaned_df.head())
            
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
                    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
                    st.session_state[f"cleaned_{file.name}"] = cleaned_df
                    st.write("✅ Missing Values have been Filled!")
                    st.dataframe(cleaned_df.head())
        
        # Column Selection
        st.subheader("📌 Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        
        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.warning("No numerical columns available for visualization.")
        
        # File Conversion
        st.subheader("♻ File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                filename=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed!")
