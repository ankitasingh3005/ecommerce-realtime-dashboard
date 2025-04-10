import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# Set formal font and whitegrid style
mpl.rcParams['font.family'] = 'DejaVu Sans'
sns.set(style="whitegrid")

# Streamlit config
st.set_page_config(page_title="📦 E-commerce Dashboard", layout="wide", page_icon="🛒")
custom_palette = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1"]

st.title("🛍️ E-commerce Orders Dashboard")
st.markdown("Track performance, customers, revenue & trends for your e-commerce business.")

# Database connection
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )

conn = get_connection()
df = pd.read_sql("SELECT * FROM orders", conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['revenue'] = df['price'] * df['quantity']

# Sidebar filters
st.sidebar.header("🔍 Filter Orders")
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

# Checkbox-style filters using data_editor
region_table = pd.DataFrame({"Region": sorted(df['region'].unique()), "Include": True})
selected_region_table = st.sidebar.data_editor(region_table, hide_index=True, use_container_width=True)
selected_regions = selected_region_table[selected_region_table["Include"]]["Region"].tolist()

status_table = pd.DataFrame({"Status": sorted(df['status'].unique()), "Include": True})
selected_status_table = st.sidebar.data_editor(status_table, hide_index=True, use_container_width=True)
selected_statuses = selected_status_table[selected_status_table["Include"]]["Status"].tolist()

product_table = pd.DataFrame({"Product": sorted(df['product_name'].unique()), "Include": True})
selected_product_table = st.sidebar.data_editor(product_table, hide_index=True, use_container_width=True)
selected_products = selected_product_table[selected_product_table["Include"]]["Product"].tolist()

# Apply filters
filtered_df = df[
    (df['date'] >= start_date) &
    (df['date'] <= end_date) &
    (df['region'].isin(selected_regions)) &
    (df['status'].isin(selected_statuses)) &
    (df['product_name'].isin(selected_products))
]

# Summary metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧾 Total Orders", len(filtered_df))
revenue = filtered_df['revenue'].sum()
col2.metric("💰 Total Revenue", f"${revenue:,.2f}")
col3.metric("👤 Unique Customers", filtered_df['customer_id'].nunique())
aov = revenue / len(filtered_df) if len(filtered_df) else 0
col4.metric("📈 Avg. Order Value", f"${aov:.2f}")

# Cancellation Rate
cancel_rate = 0
if len(filtered_df) > 0:
    cancelled = filtered_df[filtered_df['status'].str.lower() == 'cancelled']
    cancel_rate = (len(cancelled) / len(filtered_df)) * 100
st.metric("❌ Cancellation Rate", f"{cancel_rate:.2f}%")

# Top Customers by Revenue
st.markdown("### 👑 Top Customers by Revenue")
top_customers = filtered_df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 5))
bars = sns.barplot(x=top_customers.values, y=top_customers.index, palette=custom_palette, ax=ax)
ax.set_title("Top 10 Customers by Spend")
ax.set_xlabel("Revenue")
ax.set_ylabel("Customer ID")
ax.bar_label(bars.containers[0], fmt="$%.0f")
st.pyplot(fig)

# Region-wise Orders
st.markdown("### 🌍 Top Regions by Orders")
region_counts = filtered_df['region'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(12, 5))
bars = sns.barplot(x=region_counts.index, y=region_counts.values, palette=custom_palette, ax=ax2)
ax2.set_title("Top 10 Regions by Order Count")
ax2.set_ylabel("Order Count")
ax2.set_xlabel("Region")
ax2.tick_params(axis='x', rotation=30)
ax2.bar_label(bars.containers[0], fmt="%d")
st.pyplot(fig2)

# Order Status Breakdown
st.markdown("### 📦 Order Status Breakdown")
status_counts = filtered_df['status'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 4))
bars = sns.barplot(x=status_counts.index, y=status_counts.values, palette=custom_palette, ax=ax3)
ax3.set_title("Order Status Distribution")
ax3.set_ylabel("Number of Orders")
ax3.bar_label(bars.containers[0], fmt="%d")
st.pyplot(fig3)

# Top Products
st.markdown("### 🛍️ Best-Selling Products")
top_products = filtered_df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10)
fig4, ax4 = plt.subplots(figsize=(10, 6))
bars = sns.barplot(x=top_products.values, y=top_products.index, palette=custom_palette, ax=ax4)
ax4.set_title("Top 10 Products by Quantity")
ax4.set_xlabel("Quantity Sold")
ax4.set_ylabel("Product Name")
ax4.bar_label(bars.containers[0], fmt="%d")
st.pyplot(fig4)

# Revenue by Region
st.markdown("### 💸 Top Revenue-Generating Regions")
rev_region = filtered_df.groupby('region')['revenue'].sum().sort_values(ascending=False).head(10)
fig5, ax5 = plt.subplots(figsize=(12, 5))
bars = sns.barplot(x=rev_region.index, y=rev_region.values, palette=custom_palette, ax=ax5)
ax5.set_title("Top 10 Regions by Revenue")
ax5.set_ylabel("Revenue")
ax5.set_xlabel("Region")
ax5.tick_params(axis='x', labelrotation=30)
ax5.bar_label(bars.containers[0], fmt="$%.0f")
st.pyplot(fig5)

# Data Table and Download
st.markdown("### 📄 Full Dataset View")
st.dataframe(filtered_df)
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="filtered_orders.csv", mime="text/csv")
