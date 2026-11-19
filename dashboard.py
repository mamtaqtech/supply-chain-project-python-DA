
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Page settings
st.set_page_config(
    page_title="Supply Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the dataset
df = pd.read_csv("supply_chain_inventory.csv", encoding="latin1")

# Convert date columns
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
df["received_at"] = pd.to_datetime(df["received_at"])

# Create year and month columns
df["year"] = df["ordered_at"].dt.year
df["month"] = df["ordered_at"].dt.month

# Dashboard title
st.title("Supply Chain & Inventory Analysis")
st.caption("Overview of orders, suppliers, warehouses and deliveries")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

selected_country = st.sidebar.multiselect(
    "Select Supplier Country",
    sorted(df["supplier_country"].dropna().unique()),
    default=sorted(df["supplier_country"].dropna().unique())
)

selected_status = st.sidebar.multiselect(
    "Select Order Status",
    sorted(df["status"].dropna().unique()),
    default=sorted(df["status"].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df["year"].isin(selected_year)) &
    (df["supplier_country"].isin(selected_country)) &
    (df["status"].isin(selected_status))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# KPI calculations
total_orders = filtered_df["purchase_order_id"].nunique()
total_suppliers = filtered_df["supplier_id"].nunique()
total_warehouses = filtered_df["warehouse_id"].nunique()
total_order_value = filtered_df["order_value"].sum()

# KPI cards
st.subheader("Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Orders", f"{total_orders:,}")
k2.metric("Total Suppliers", f"{total_suppliers:,}")
k3.metric("Total Warehouses", f"{total_warehouses:,}")
k4.metric("Total Order Value", f"{total_order_value / 1000000:,.2f}M")

st.divider()

# --------------------------------------------------
# CHART 1 AND CHART 2
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("1. Order Status Overview")

    status_counts = filtered_df["status"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        status_counts.index,
        status_counts.values,
        color=["#264653", "#E76F51", "#E9C46A", "#2A9D8F"]
    )

    ax.set_ylabel("Number of Orders")
    ax.set_title("Orders by Status")
    ax.tick_params(axis="x", rotation=0)

    for container in ax.containers:
        ax.bar_label(container, fmt="%d", fontsize=9)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    st.subheader("2. Top 10 Suppliers - Partial Orders")

    partial_orders = filtered_df[
        filtered_df["status"] == "partial"
    ]

    supplier_counts = (
        partial_orders.groupby("supplier_id")["purchase_order_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    supplier_counts.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#E76F51"
    )

    ax.set_xlabel("Partial Orders")
    ax.set_ylabel("Supplier")
    ax.set_title("Top 10 Suppliers")

    for container in ax.containers:
        ax.bar_label(container, fontsize=8)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


st.divider()

# --------------------------------------------------
# CHART 3 AND CHART 4
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("3. Suppliers with Highest Partial Order %")

    total_supplier_orders = (
        filtered_df.groupby("supplier_id")["purchase_order_id"]
        .nunique()
    )

    partial_supplier_orders = (
        partial_orders.groupby("supplier_id")["purchase_order_id"]
        .nunique()
    )

    partial_percentage = (
        partial_supplier_orders / total_supplier_orders * 100
    ).sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(6, 4))

    partial_percentage.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#2A9D8F"
    )

    ax.set_xlabel("Partial Orders (%)")
    ax.set_ylabel("Supplier")
    ax.set_title("Top 10 Suppliers")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    st.subheader("4. Suppliers with Most Delayed Deliveries")

    delivered_orders = filtered_df[
        filtered_df["received_at"].notna()
    ].copy()

    delayed_orders = delivered_orders[
        delivered_orders["received_at"] > delivered_orders["expected_at"]
    ]

    delayed_counts = (
        delayed_orders.groupby("supplier_id")["purchase_order_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    delayed_counts.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#E9C46A"
    )

    ax.set_xlabel("Delayed Orders")
    ax.set_ylabel("Supplier")
    ax.set_title("Top 10 Suppliers")

    for container in ax.containers:
        ax.bar_label(container, fontsize=8)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


st.divider()

# --------------------------------------------------
# CHART 5 AND CHART 6
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("5. Suppliers with Longest Delivery Time")

    delivered_orders["delivery_days"] = (
        delivered_orders["received_at"] -
        delivered_orders["ordered_at"]
    ).dt.days

    avg_delivery = (
        delivered_orders.groupby("supplier_id")["delivery_days"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    avg_delivery.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#457B9D"
    )

    ax.set_xlabel("Average Delivery Days")
    ax.set_ylabel("Supplier")
    ax.set_title("Top 10 Suppliers")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    st.subheader("6. Countries with Most Orders")

    country_counts = (
        filtered_df.groupby("supplier_country")["purchase_order_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    # Keep the top 6 countries and group the rest
    top_countries = country_counts.head(6)
    other_count = country_counts.iloc[6:].sum()

    if other_count > 0:
        top_countries.loc["Other"] = other_count

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.pie(
        top_countries,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.75,
        wedgeprops={"width": 0.4},
        textprops={"fontsize": 9}
    )

    ax.legend(
        top_countries.index,
        title="Country",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=8
    )

    ax.set_title("Orders by Supplier Country")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


st.divider()

# --------------------------------------------------
# CHART 7 AND CHART 8
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("7. Warehouses with Highest Quantity Ordered")

    warehouse_quantity = (
        filtered_df.groupby("warehouse_id")["quantity_ordered"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    warehouse_quantity.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#6D597A"
    )

    ax.set_xlabel("Quantity Ordered")
    ax.set_ylabel("Warehouse")
    ax.set_title("Quantity by Warehouse")

    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(
        [f"{x / 1000000:.1f}M" for x in ax.get_xticks()]
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            labels=[f"{v / 1000000:.1f}M" for v in container.datavalues],
            fontsize=8
        )

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    st.subheader("8. Suppliers with Highest Order Value")

    supplier_value = (
        filtered_df.groupby("supplier_id")["order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    squarify.plot(
        sizes=supplier_value.values,
        label=[
            f"{supplier}\n{value / 1000000:.1f}M"
            for supplier, value in supplier_value.items()
        ],
        alpha=0.85,
        color=[
            "#264653", "#E76F51", "#E9C46A", "#2A9D8F",
            "#6D597A", "#F4A261", "#457B9D", "#BC4749",
            "#8A9A5B", "#9D4EDD"
        ],
        text_kwargs={"fontsize": 8},
        ax=ax
    )

    ax.set_title("Top 10 Suppliers by Order Value")
    ax.axis("off")

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


st.divider()

# --------------------------------------------------
# CHART 9 AND CHART 10
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("9. Overall Order Status Distribution")

    status_counts = filtered_df["status"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.pie(
        status_counts,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.75,
        wedgeprops={"width": 0.4},
        textprops={"fontsize": 9}
    )

    ax.legend(
        status_counts.index,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=9
    )

    ax.set_title("Order Status Distribution")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


with col2:
    st.subheader("10. Monthly Order Trend by Year")

    monthly_orders = (
        filtered_df.groupby(
            ["month", "year"]
        )["purchase_order_id"]
        .nunique()
        .unstack(fill_value=0)
    )

    monthly_orders = monthly_orders.reindex(range(1, 13), fill_value=0)

    fig, ax = plt.subplots(figsize=(6, 4))

    year_colors = [
        "#264653", "#E76F51", "#E9C46A", "#2A9D8F",
        "#6D597A", "#F4A261", "#457B9D", "#BC4749",
        "#8A9A5B", "#9D4EDD"
    ]

    monthly_orders.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=[
            year_colors[i % len(year_colors)]
            for i in range(len(monthly_orders.columns))
        ],
        width=0.7
    )

    ax.set_title("Monthly Orders by Year")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")

    ax.set_xticklabels(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        rotation=0
    )

    ax.legend(
        title="Year",
        fontsize=8
    )

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# Footer
st.divider()
st.caption("Supply Chain & Inventory Analysis | Python & Streamlit")

#.\.venv\Scripts\python.exe -m streamlit run dashboard.py