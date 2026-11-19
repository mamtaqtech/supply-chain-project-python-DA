
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

# Load dataset
df = pd.read_csv("supply_chain_inventory.csv", encoding="latin1")

# Convert date columns
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
df["received_at"] = pd.to_datetime(df["received_at"])

# Create year and month columns
df["year"] = df["ordered_at"].dt.year
df["month"] = df["ordered_at"].dt.month


# ---------------- FILTERS ----------------

st.sidebar.header("Dashboard Filters")

year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

country = st.sidebar.multiselect(
    "Select Country",
    sorted(df["supplier_country"].dropna().unique()),
    default=sorted(df["supplier_country"].dropna().unique())
)

status = st.sidebar.multiselect(
    "Select Status",
    sorted(df["status"].dropna().unique()),
    default=sorted(df["status"].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df["year"].isin(year)) &
    (df["supplier_country"].isin(country)) &
    (df["status"].isin(status))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()


# ---------------- DASHBOARD TITLE ----------------

st.title("Supply Chain & Inventory Analysis")


# ---------------- KPI CARDS ----------------

total_orders = filtered_df["purchase_order_id"].nunique()
total_suppliers = filtered_df["supplier_id"].nunique()
total_warehouses = filtered_df["warehouse_id"].nunique()
total_order_value = filtered_df["order_value"].sum()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Orders", f"{total_orders:,}")
k2.metric("Total Suppliers", f"{total_suppliers:,}")
k3.metric("Total Warehouses", f"{total_warehouses:,}")
k4.metric("Total Order Value", f"{total_order_value / 1000000:,.2f}M")

st.divider()


# ---------------- PREPARE DATA ----------------

partial_orders = filtered_df[
    filtered_df["status"] == "partial"
]

supplier_partial = (
    partial_orders.groupby("supplier_id")["purchase_order_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

supplier_total = (
    filtered_df.groupby("supplier_id")["purchase_order_id"]
    .nunique()
)

supplier_partial_all = (
    partial_orders.groupby("supplier_id")["purchase_order_id"]
    .nunique()
)

partial_percentage = (
    supplier_partial_all / supplier_total * 100
).sort_values(ascending=False).head(10)

delivered = filtered_df[
    filtered_df["received_at"].notna()
].copy()

delayed = delivered[
    delivered["received_at"] > delivered["expected_at"]
]

delayed_suppliers = (
    delayed.groupby("supplier_id")["purchase_order_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

delivered["delivery_days"] = (
    delivered["received_at"] - delivered["ordered_at"]
).dt.days

avg_delivery = (
    delivered.groupby("supplier_id")["delivery_days"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)


# ==================================================
# FIRST ROW - CHARTS 1 TO 5
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)


# CHART 1: ORDER STATUS

with col1:

    st.subheader("1. Order Status")

    status_count = filtered_df["status"].value_counts()

    fig, ax = plt.subplots(figsize=(3, 2.5))

    status_count.plot(
        kind="bar",
        ax=ax,
        color=["#264653", "#E76F51", "#E9C46A", "#2A9D8F"]
    )

    ax.set_ylabel("Orders", fontsize=7)
    ax.tick_params(axis="both", labelsize=7)

    for container in ax.containers:
        ax.bar_label(container, fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 2: TOP PARTIAL ORDER SUPPLIERS

with col2:

    st.subheader("2. Partial Orders")

    fig, ax = plt.subplots(figsize=(3, 2.5))

    supplier_partial.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#E76F51"
    )

    ax.set_xlabel("Orders", fontsize=7)
    ax.tick_params(axis="both", labelsize=6)

    for container in ax.containers:
        ax.bar_label(container, fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 3: PARTIAL ORDER PERCENTAGE

with col3:

    st.subheader("3. Partial Order %")

    fig, ax = plt.subplots(figsize=(3, 2.5))

    partial_percentage.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#2A9D8F"
    )

    ax.set_xlabel("Percentage", fontsize=7)
    ax.tick_params(axis="both", labelsize=6)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 4: DELAYED DELIVERIES

with col4:

    st.subheader("4. Delayed Orders")

    fig, ax = plt.subplots(figsize=(3, 2.5))

    delayed_suppliers.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#E9C46A"
    )

    ax.set_xlabel("Orders", fontsize=7)
    ax.tick_params(axis="both", labelsize=6)

    for container in ax.containers:
        ax.bar_label(container, fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 5: AVERAGE DELIVERY TIME

with col5:

    st.subheader("5. Delivery Time")

    fig, ax = plt.subplots(figsize=(3, 2.5))

    avg_delivery.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#457B9D"
    )

    ax.set_xlabel("Days", fontsize=7)
    ax.tick_params(axis="both", labelsize=6)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


st.divider()


# ==================================================
# SECOND ROW - CHARTS 6 TO 10
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)


# CHART 6: COUNTRY-WISE ORDERS

with col1:

    st.subheader("6. Orders by Country")

    country_count = (
        filtered_df.groupby("supplier_country")["purchase_order_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    top_country = country_count.head(6).copy()

    other = country_count.iloc[6:].sum()

    if other > 0:
        top_country.loc["Other"] = other

    fig, ax = plt.subplots(figsize=(3, 2.5))

    ax.pie(
        top_country,
        labels=None,
        autopct="%1.0f%%",
        startangle=90,
        colors=["#264653", "#E76F51", "#E9C46A",
                "#2A9D8F", "#6D597A", "#F4A261", "#457B9D"],
        wedgeprops={"width": 0.4},
        textprops={"fontsize": 6}
    )

    ax.legend(
        top_country.index,
        fontsize=5,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=2
    )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 7: WAREHOUSE QUANTITY

with col2:

    st.subheader("7. Warehouse Quantity")

    warehouse_quantity = (
        filtered_df.groupby("warehouse_id")["quantity_ordered"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(3, 2.5))

    warehouse_quantity.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#6D597A"
    )

    ax.set_xlabel("Quantity (Millions)", fontsize=7)
    ax.tick_params(axis="both", labelsize=6)

    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels([
        f"{x / 1000000:.1f}" for x in ax.get_xticks()
    ])

    for container in ax.containers:
        ax.bar_label(
            container,
            labels=[f"{v / 1000000:.1f}M"
                    for v in container.datavalues],
            fontsize=5
        )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 8: SUPPLIER ORDER VALUE

with col3:

    st.subheader("8. Supplier Order Value")

    supplier_value = (
        filtered_df.groupby("supplier_id")["order_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(3, 2.5))

    squarify.plot(
        sizes=supplier_value.values,
        label=[
            f"{supplier}\n{value / 1000000:.1f}M"
            for supplier, value in supplier_value.items()
        ],
        color=[
            "#264653", "#E76F51", "#E9C46A", "#2A9D8F",
            "#6D597A", "#F4A261", "#457B9D", "#BC4749",
            "#8A9A5B", "#9D4EDD"
        ],
        text_kwargs={"fontsize": 5},
        ax=ax
    )

    ax.axis("off")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 9: ORDER STATUS DISTRIBUTION

with col4:

    st.subheader("9. Status Distribution")

    status_count = filtered_df["status"].value_counts()

    fig, ax = plt.subplots(figsize=(3, 2.5))

    ax.pie(
        status_count,
        labels=None,
        autopct="%1.0f%%",
        startangle=90,
        colors=["#264653", "#E76F51", "#E9C46A", "#2A9D8F"],
        wedgeprops={"width": 0.4},
        textprops={"fontsize": 6}
    )

    ax.legend(
        status_count.index,
        fontsize=6,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=2
    )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# CHART 10: MONTHLY ORDER TREND

with col5:

    st.subheader("10. Monthly Orders")

    monthly_orders = (
        filtered_df.groupby(["month", "year"])["purchase_order_id"]
        .nunique()
        .unstack(fill_value=0)
    )

    monthly_orders = monthly_orders.reindex(
        range(1, 13),
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(3, 2.5))

    monthly_orders.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=["#264653", "#E76F51", "#E9C46A",
               "#2A9D8F", "#6D597A"]
    )

    ax.set_xlabel("Month", fontsize=7)
    ax.set_ylabel("Orders", fontsize=7)

    ax.set_xticklabels(
        ["J", "F", "M", "A", "M", "J",
         "J", "A", "S", "O", "N", "D"],
        rotation=0
    )

    ax.tick_params(axis="both", labelsize=6)
    ax.legend(title="Year", fontsize=5, title_fontsize=6)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ---------------- FOOTER ----------------

st.divider()
st.caption("Supply Chain & Inventory Analysis | Python & Streamlit")


#.\.venv\Scripts\python.exe -m streamlit run dashboard.py