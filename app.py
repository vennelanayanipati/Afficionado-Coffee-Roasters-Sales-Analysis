import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.templates.default = "none"

st.set_page_config(page_title="Sales Trend and Time-Based Performance Analysis for Afficionado Coffee Roasters", layout="wide")

# Load Data
@st.cache_data
def load_data():

    df = pd.read_csv(r"C:\Users\venne\Downloads\Afficionado Coffee Roasters Final Project.csv")
    return df

st.title("🤎☕ Sales Trend and Time-Based Performance Analysis for Afficionado Coffee Roasters")
df = load_data()

st.sidebar.markdown(
    """
    <h1 style='text-align:left;color:black;'>
    AFFICIONADO COFFEE ROASTERS
    </h1>
    """,
    unsafe_allow_html=True
)

# ---- SIDEBAR HEADER ----
st.sidebar.image(
    r"C:\Users\venne\Downloads\PDI-Design-Coffee-Afficionado.jpg",   
    width=500
)

# Sidebar Filters

# Store location filter
store = st.sidebar.multiselect(
    "Select Store Location",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

# Day selector
# Correct weekday order
day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
day = st.sidebar.multiselect(
    "Select Day of Week",
    options=day_order,   # use ordered list
    default=day_order
)

# Hour range slider
hour_range = st.sidebar.slider(
    "Select Hour Range",
    min_value=0,
    max_value=23,
    value=(0,23)
)

# Revenue vs Quantity toggle
metric = st.sidebar.radio(
    "Select Metric",
    ["Revenue", "Quantity"]
)

# Apply Filters
filtered_df = df[
    (df["store_location"].isin(store)) &
    (df["day_of_week"].isin(day)) &
    (df["hour"] >= hour_range[0] ) &
    (df["hour"] <= hour_range[1])   
]
value_col = "revenue" if metric == "Revenue" else "transaction_qty"

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

filtered_df = filtered_df.copy()

filtered_df["day_of_week"] = pd.Categorical(
    filtered_df["day_of_week"],
    categories=day_order,
    ordered=True
)


# Calculate KPI values 
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
total_revenue = filtered_df["revenue"].sum()
total_quantity = filtered_df["transaction_qty"].sum()
total_transactions = filtered_df["transaction_id"].nunique()

col1.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">💰 Total Revenue</div>
<div class="kpi-value">${total_revenue:,.2f}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">🧾 Transactions</div>
<div class="kpi-value">{total_transactions:,}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">☕ Quantity Sold</div>
<div class="kpi-value">{total_quantity:,}</div>
</div>
""", unsafe_allow_html=True)

# Overall sales trend

st.subheader("📈 Overall Sales Trend")
daily_trend = filtered_df.groupby("date")[value_col].sum().reset_index()
fig1 = px.bar(daily_trend, x="date", y=value_col, title="Daily Sales Trend",color_discrete_sequence=["#8A5A7D"])
fig1.update_yaxes(title_font=dict(color="black", size=20))
fig1.update_xaxes(title="Date", automargin=True, title_font=dict(color="black", size=20))
fig1.update_layout(height = 500,plot_bgcolor="#d1d5db", paper_bgcolor="#d1d5db")
st.plotly_chart(fig1, width="stretch")

# Day of Week Performance

st.subheader("📅 Day of Week Performance")
dow = filtered_df.groupby("day_of_week")[value_col].sum().reset_index()
fig2 = px.bar(dow, x="day_of_week", y=value_col, title="Sales by Day of Week",color_discrete_sequence=["#5A034B", "#BD3D9B", "#896E82", "5A034B", "#BD3D9B", "#896E82", "#5A034B"])
fig2.update_yaxes(title_font=dict(color="black", size=20))
fig2.update_xaxes(title_font=dict(color="black", size=20))
fig2.update_layout(plot_bgcolor="#d1d5db", paper_bgcolor="#d1d5db")
st.plotly_chart(fig2, width="stretch")

# Location comparison

st.subheader("🏪 Store Location Comparison")
store_trend = filtered_df.groupby("store_location")[value_col].sum().reset_index()
fig3 = px.bar(store_trend, x="store_location", y=value_col, color="store_location", title="Sales by Store Location",color_discrete_sequence=["#896E82","#BD3D9B", "#5A034B"])
fig3.update_yaxes(title_font=dict(color="black", size=20))
fig3.update_xaxes(title_font=dict(color="black", size=20))
fig3.update_layout(plot_bgcolor="#d1d5db", paper_bgcolor="#d1d5db")
st.plotly_chart(fig3, width="stretch")

#Heatmap

st.subheader("🔥 Hourly Demand Heatmap")

heatmap_data = filtered_df.pivot_table(
    values="revenue",
    index="store_location",
    columns="hour",
    aggfunc="sum"
)

# Create heatmap
fig4 = px.imshow(
    heatmap_data,
    color_continuous_scale=["purple", "pink"],
    aspect="auto",
    title="Hourly Demand Heatmap"
    )

# Improve axis labels
fig4.update_xaxes(title="Hour of Day", tickmode="linear")
fig4.update_yaxes(title="Store Location",automargin=True)
fig4.update_traces(
    hovertemplate="Store: %{y}<br>Hour: %{x}<br>Revenue: %{z:,.2f}<extra></extra>"
)
# Fix Y-axis orientation
height=500,
margin=dict(l=120, r=40, t=60, b=60)
fig4.update_layout(plot_bgcolor="#d1d5db", paper_bgcolor="#d1d5db",title_font=dict(color="Black"))
st.plotly_chart(fig4, width="stretch")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #8A5A7D;
}
</style>
""", unsafe_allow_html=True
)

st.markdown("""
<style>

/* Filter titles */
[data-testid="stSidebar"] label {
    color: black !important;
    font-weight: 800;
}

/* Multiselect / selectbox background */
[data-baseweb="select"] > div {
    background-color: #f5f5f5 !important;
}

/* Selected option tags */
[data-baseweb="tag"] {
    background-color: white !important;
    color: black !important;
    border: 1px solid #d1d5db !important;
}

/* Dropdown arrow */          
[data-baseweb="select"] svg {
    color: #6b7280 !important;
    fill: #6b7280 !important;
}


/* Radio button option text */
div[role="radiogroup"] label {
    color: black !important;
}
                  
/* Radio button title */
div[role="radiogroup"] p {
    color: black !important;
            
/* Slider track (background line) */
[data-testid="stSlider"] .st-bd {
    background-color: #c084fc !important;
}

/* Active slider range */
[data-testid="stSlider"] .st-be {
    background-color: #a855f7 !important;
}

/* Slider track */
 div[data-baseweb="slider"] > div {
    background-color: #d1d5db !important;
}

/* Selected range */
.stSlider [data-baseweb="slider"] div[role="presentation"] {
    background-color: #9ca3af !important;
}            

/* Slider handle (circle) */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #6b7280 !important;
    border: 2px solid solid white !important;
}

</style>
""", unsafe_allow_html=True)

#Add KPI cards css
st.markdown("""
<style>

.kpi-card {
    background-color: #fff5f7;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border-left: 6px solid #8A5A7D;
    border-top: 6px solid #8A5A7D;
    box-shadow: 0px 4px 12px rgba(138, 90, 125, 0.65);
}

.kpi-title {
    font-size:16px;
    color:#6b7280;
}

.kpi-value {
    font-size:28px;
    font-weight:bold;
    color:#111827;
}

</style>
""", unsafe_allow_html=True)

# Page background
st.markdown("""
<style>
.stApp {
    background-color: #d1d5db;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    👩‍💻  Developed by ** Vennela Nayanipati**\n
    💻 GitHub: https://github.com/vennelanayanipati\n
    
    """,
    unsafe_allow_html=True
    )