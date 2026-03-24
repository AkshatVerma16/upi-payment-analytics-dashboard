import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="UPI Analytics Pro", layout="wide", page_icon="💳")
st.title("💳 Professional UPI Payment Analytics Dashboard")
st.markdown("Analyze digital payment behavior, user segments, and fraud patterns in real-time.")

# 2. File Handling Logic
current_dir = os.path.dirname(os.path.abspath(__file__))
default_file = os.path.join(current_dir, '..', 'data', 'upi_data.csv')

st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload UPI CSV File", type=["csv"])

# Function to load and clean data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df['date_time'] = pd.to_datetime(df['date_time'])
    return df

# Use uploaded file if available, else use the generated one
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("Using Uploaded Data")
else:
    if os.path.exists(default_file):
        df = load_data(default_file)
        st.sidebar.info("Using Default Generated Data")
    else:
        st.error("No data found! Please run 'generate_data.py' first.")
        st.stop()

# 3. Dynamic Sidebar Filters
st.sidebar.header("🔍 Global Filters")

# Date Filter
min_date = df['date_time'].min().date()
max_date = df['date_time'].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# City & Merchant Filters
selected_cities = st.sidebar.multiselect("Select Cities", options=df['location'].unique(), default=df['location'].unique())
selected_merchants = st.sidebar.multiselect("Select Merchants", options=df['merchant'].unique(), default=df['merchant'].unique())

# Applying Filters
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df['date_time'].dt.date >= start_date) & (df['date_time'].dt.date <= end_date) & \
           (df['location'].isin(selected_cities)) & (df['merchant'].isin(selected_merchants))
    df_filtered = df[mask]
else:
    df_filtered = df

# 4. Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Transactions", f"{len(df_filtered):,}")
with col2:
    st.metric("Total Value", f"₹{df_filtered['amount'].sum():,.0f}")
with col3:
    st.metric("Avg Ticket Size", f"₹{df_filtered['amount'].mean():,.2f}")
with col4:
    st.metric("Unique Users", df_filtered['user_id'].nunique())

st.divider()

# 5. Visual Analysis Tabs
tab1, tab2, tab3 = st.tabs(["⏰ Time Analysis", "👥 User Insights", "🚨 Fraud Detection"])

with tab1:
    st.subheader("Peak Transaction Hours")
    df_filtered['hour'] = df_filtered['date_time'].dt.hour
    hourly_data = df_filtered.groupby('hour').size().reset_index(name='Volume')
    fig_hour = px.area(hourly_data, x='hour', y='Volume', title="Hourly Traffic Pattern", color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_hour, use_container_width=True)

with tab2:
    st.subheader("User Segmentation")
    user_txns = df_filtered.groupby('user_id').size().reset_index(name='count')
    def get_segment(c):
        if c > 50: return 'Power User'
        if c > 20: return 'Regular'
        return 'Occasional'
    user_txns['Segment'] = user_txns['count'].apply(get_segment)
    fig_pie = px.pie(user_txns, names='Segment', hole=0.4, title="User Base Split")
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Potential Fraud Alerts")
    # Rule: High value (>45k)
    high_val = df_filtered[df_filtered['amount'] > 45000]
    if not high_val.empty:
        st.dataframe(high_val[['transaction_id', 'user_id', 'amount', 'date_time', 'location']], use_container_width=True)
    else:
        st.success("No suspicious high-value transactions found in this period.")

# 6. Export Feature
st.sidebar.divider()
st.sidebar.download_button("📥 Download Filtered Data", df_filtered.to_csv(index=False), "filtered_upi_data.csv", "text/csv")