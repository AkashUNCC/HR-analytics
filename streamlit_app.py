import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

# Title
st.title("HR Analytics Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload HR Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())
    
    # Select Key Columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_department = st.sidebar.selectbox("Select Department", ["All"] + df['Department'].unique().tolist()) if 'Department' in df.columns else None
    
    # Apply Department Filter
    if selected_department and selected_department != "All":
        df = df[df['Department'] == selected_department]
    
    # Employee Turnover Visualization
    if 'Attrition' in df.columns:
        st.write("### Employee Attrition")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='Attrition', ax=ax, palette='coolwarm')
        st.pyplot(fig)
    
    # Department-wise Distribution
    if 'Department' in df.columns:
        st.write("### Department-wise Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=df, y='Department', order=df['Department'].value_counts().index, palette='viridis')
        st.pyplot(fig)
    
    # Salary Distribution
    if 'MonthlyIncome' in df.columns:
        st.write("### Salary Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['MonthlyIncome'], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    
    # Correlation Heatmap
    if numeric_cols:
        st.write("### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)
else:
    st.info("Please upload a CSV file to proceed.")
