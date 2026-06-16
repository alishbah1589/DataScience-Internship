import streamlit as st
import pandas as pd

# -----------------------
# Page Configuration
# -----------------------

st.set_page_config(
    page_title="Global Superstore Dashboard",
    layout="wide"
)

st.title("📊 Global Superstore Dashboard")

# -----------------------
# Load Data
# -----------------------

df = pd.read_csv("../datasets/superstore.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Remove Postal Code
if 'Postal Code' in df.columns:
    df = df.drop('Postal Code', axis=1)

# -----------------------
# Sidebar Filters
# -----------------------

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

sub_category = st.sidebar.multiselect(
    "Sub-Category",
    options=df['Sub-Category'].unique(),
    default=df['Sub-Category'].unique()
)

# -----------------------
# Apply Filters
# -----------------------

filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Sub-Category'].isin(sub_category))
]

# -----------------------
# KPIs
# -----------------------

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

st.divider()

# -----------------------
# Sales by Category
# -----------------------

st.subheader("Sales by Category")

sales_by_category = (
    filtered_df.groupby('Category')['Sales']
    .sum()
)

st.bar_chart(sales_by_category)

# -----------------------
# Profit by Category
# -----------------------

st.subheader("Profit by Category")

profit_by_category = (
    filtered_df.groupby('Category')['Profit']
    .sum()
)

st.bar_chart(profit_by_category)

# -----------------------
# Top 5 Customers
# -----------------------

st.subheader("Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.dataframe(top_customers)

# -----------------------
# Region Sales
# -----------------------

st.subheader("Sales by Region")

region_sales = (
    filtered_df.groupby('Region')['Sales']
    .sum()
)

st.bar_chart(region_sales)

# -----------------------
# Raw Data
# -----------------------

st.subheader("Filtered Dataset")

st.dataframe(filtered_df)