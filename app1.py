import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Afficionado Coffee Roasters Sales Dashboard", layout="wide")

st.title("☕ Afficionado Coffee Roasters Sales Analytics Dashboard")

# Load dataset
df = pd.read_csv(r"C:\Users\venne\Downloads\New Afficionado Coffee Roasters.csv")

# Convert date
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format="%H:%M:%S")

# Feature Engineering
df['hour'] = df['transaction_time'].dt.hour
df['day'] = df['transaction_time'].dt.day_name()
df['date'] = df['transaction_time'].dt.date

df['revenue'] = df['transaction_qty'] * df['unit_price']

# Sidebar Filters
st.sidebar.header("Filters")

store = st.sidebar.multiselect(
    "Select Store Location",
    df['store_location'].unique(),
    default=df['store_location'].unique()
)

category = st.sidebar.multiselect(
    "Select Product Category",
    df['product_category'].unique(),
    default=df['product_category'].unique()
)

filtered_df = df[
    (df['store_location'].isin(store)) &
    (df['product_category'].isin(category))
]

# KPIs
st.header("Key Performance Indicators")

total_sales = filtered_df['revenue'].sum()
transactions = len(filtered_df)
avg_order = total_sales / transactions

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Transactions", transactions)
col3.metric("Average Order Value", f"${avg_order:.2f}")

# Sales Trend
st.subheader("Daily Sales Trend")

daily_sales = filtered_df.groupby('date')['revenue'].sum()

fig, ax = plt.subplots()
daily_sales.plot(ax=ax)
ax.set_ylabel("Revenue")
ax.set_title("Daily Sales Trend")

st.pyplot(fig)

# Day-of-week analysis
st.subheader("Sales by Day of Week")

dow_sales = filtered_df.groupby('day')['revenue'].mean()

fig, ax = plt.subplots()
dow_sales.plot(kind='bar', ax=ax)
ax.set_ylabel("Average Revenue")

st.pyplot(fig)

# Hourly demand heatmap
st.subheader("Hourly Demand Heatmap")

hourly = filtered_df.groupby(['day','hour']).size().unstack()

fig, ax = plt.subplots()
sns.heatmap(hourly, cmap="coolwarm", ax=ax)

st.pyplot(fig)

# Location comparison
st.subheader("Store Location Performance")

loc_sales = filtered_df.groupby('store_location')['revenue'].sum()

fig, ax = plt.subplots()
loc_sales.plot(kind='bar', ax=ax)

st.pyplot(fig)