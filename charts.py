import pandas as pd 
import matplotlib.pyplot as plt 
import squarify
df = pd.read_csv("supply_chain_inventory.csv", encoding="latin1")

# Convert date columns into datetime format  (to avoid further complications )
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
df["received_at"] = pd.to_datetime(df["received_at"])


# Chart 1: #BUSINESS PROBLEM 1:
#How many orders received less items than actually been ordered 
short_received_orders = df[df["quantity_received"] < df["quantity_ordered"]]

# Count how many orders fall under each status
status_counts = short_received_orders["status"].value_counts()
print(status_counts)


# """less received orders status  : status
# partial      1326
# open          467
# cancelled     406"""

# Create a bar chart
status_counts.plot(
    kind="bar",
    figsize=(10, 6),
    color=["#264653", "#E76F51", "#E9C46A"]
)

# Display exact counts on top of each bar
plt.bar_label(plt.gca().containers[0])

# Add chart title and axis labels
plt.title("Orders with Fewer Items Received Than Ordered")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

# Adjust chart spacing
plt.tight_layout()

# Display the chart
plt.show()

#-----------------------------------------------------------
# chart 2

# Top 10 Suppliers with the Most Partial Orders

#partially received orders
partial_orders = df[df["status"]=="partial"]

# Count partial orders for each supplier
suppliers_partial_orders_count = partial_orders["supplier_id"].value_counts()

# Select the top 10 suppliers
top_10_suppliers_partial  = suppliers_partial_orders_count.head(10)
print(top_10_suppliers_partial)
#creating a horizontal bar chart 
top_10_suppliers_partial.plot(kind = "barh", color=[
    "#264653", "#2A9D8F", "#E9C46A", "#E76F51",
    "#6D597A", "#457B9D", "#BC4749", "#8A9A5B",
    "#F4A261", "#9D4EDD"
], figsize= (10,6) )

# Add chart title and axis labels
plt.title("Top 10 Suppliers with the Most Partial Orders", fontsize=14)
plt.xlabel("Number of Partial Orders")
plt.ylabel("Supplier ID")

#display exact counts on /bar
plt.bar_label(plt.gca().containers[0])

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------------

# Chart 3

# Which suppliers have the highest percentage of partially received orders?

# Count total orders for each supplier
supplier_total_orders = df["supplier_id"].value_counts()

# Calculate the percentage of partial orders for each supplier
supplier_partial_percentage = (suppliers_partial_orders_count / supplier_total_orders) * 100

# Sort percentages and select the top 10 suppliers
top_10_partial_percentage = supplier_partial_percentage.sort_values(ascending=False).head(10)

print(top_10_partial_percentage)

# Create a horizontal bar chart
top_10_partial_percentage.plot(kind="barh",color=[
    "#386641", "#6A994E", "#A7C957", "#F2E8CF",
    "#BC4749", "#DDA15E", "#588157", "#3A5A40",
    "#A3B18A", "#E9C46A"
],figsize=(10, 6))

# Add chart title and labels
plt.title("Top 10 Suppliers by Partial-Order Percentage")
plt.xlabel("Partial Orders (%)")
plt.ylabel("Supplier ID")

# Display percentage values on bars
plt.bar_label(plt.gca().containers[0], fmt="%.2f%%")

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------
# chart 4

# Consider only orders that have been received
# Convert date columns into datetime format
df["received_at"] = pd.to_datetime(df["received_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
received_orders = df[df["received_at"].notna()].copy()

# Calculate delivery delay in days

received_orders["delivery_delay_days"] = (
received_orders["received_at"] - received_orders["expected_at"]).dt.days

#Considering only delayed orders
delayed_orders = received_orders[received_orders['delivery_delay_days']>0]

# Count delayed orders for each supplier
supplier_delayed_counts = delayed_orders["supplier_id"].value_counts()

# Select top 10 suppliers
top_10_delayed_suppliers = supplier_delayed_counts.head(10)

print(top_10_delayed_suppliers)

# Create a vertical bar chart
top_10_delayed_suppliers.plot(kind="barh",color=[
    "#9B2226", "#AE2012", "#BB3E03", "#CA6702",
    "#EE9B00", "#0A9396", "#005F73", "#94D2BD",
    "#6D597A", "#457B9D"
],figsize=(10, 5))

print(top_10_delayed_suppliers)

# Add chart title and labels
plt.title("Top 10 Suppliers with the Most Delayed Deliveries")
plt.xlabel("Supplier ID")
plt.ylabel("Number of Delayed Orders")

# Display exact counts on bars
plt.bar_label(plt.gca().containers[0])

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------------------------------------

# Chart 5: Which suppliers have the longest average delivery time?

# Convert date columns into datetime format
df["ordered_at"] = pd.to_datetime(df["ordered_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
df["received_at"] = pd.to_datetime(df["received_at"])

# Consider only orders that have been received
received_orders = df[df["received_at"].notna()].copy()

# Calculate delivery time in days
received_orders["delivery_time_days"] = (
    received_orders["received_at"] - received_orders["ordered_at"]
).dt.days

# Calculate average delivery time for each supplier
supplier_avg_delivery_time = received_orders.groupby(
    "supplier_id"
)["delivery_time_days"].mean()

# Select top 10 suppliers
top_10_avg_delivery = supplier_avg_delivery_time.sort_values(
    ascending=False
).head(10)

print(top_10_avg_delivery)

# Create a horizontal bar chart
top_10_avg_delivery.plot(kind="barh",color=[
    "#5A189A", "#7B2CBF", "#9D4EDD", "#C77DFF",
    "#E0AAFF", "#4361EE", "#4895EF", "#4CC9F0",
    "#560BAD", "#3F37C9"
],figsize=(10, 5))

# Add chart title and labels
plt.title("Top 10 Suppliers with the Longest Average Delivery Time")
plt.xlabel("Average Delivery Time (Days)")
plt.ylabel("Supplier ID")

# Display exact counts on bars
plt.bar_label(plt.gca().containers[0],fmt="%.2f")

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------------------------------

# Chart 6: Which countries have the highest number of orders?

# Count the number of orders from each country
country_order_counts = df["supplier_country"].value_counts()

# Create a donut chart
plt.figure(figsize=(8, 8))
plt.pie(
    country_order_counts,labels=country_order_counts.index,autopct="%1.1f%%",startangle=90,colors=[
    "#264653", "#E76F51", "#E9C46A", "#2A9D8F",
    "#6D597A", "#F4A261", "#457B9D", "#BC4749",
    "#8A9A5B", "#9D4EDD"
],
    wedgeprops={"width": 0.4})

# Add chart title
plt.title("Orders by Supplier Country")

plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------------------------------------------

# Chart 7: Which warehouses have the highest order quantities?

# Calculate the total quantity ordered by each warehouse
warehouse_order_quantities = df.groupby("warehouse_id")["quantity_ordered"].sum()

# Sort the warehouses and select the top 10
top_10_warehouses = warehouse_order_quantities.sort_values(ascending=False).head(10)

# Create a vertical bar chart
top_10_warehouses.plot(
    kind="bar",
    color=[
    "#003049", "#D62828", "#F77F00", "#FCBF49",
    "#588157", "#6A4C93", "#1982C4", "#8AC926",
    "#FF595E", "#6D597A"
],
    figsize=(12, 6)
)

# Add chart title and labels
plt.title("Top 10 Warehouses by Total Order Quantity")
plt.xlabel("Warehouse ID")
plt.ylabel("Total Quantity Ordered")

# Display values in millions to avoid overlapping labels
labels = [f"{value / 1000000:.2f}M" for value in top_10_warehouses]

plt.bar_label(plt.gca().containers[0], labels=labels, padding=3)

# Display full numbers on the Y-axis instead of scientific notation
plt.ticklabel_format(axis="y", style="plain")

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------------------------


# Chart 8: Which suppliers have the highest total order value?

# Calculate the total order value for each supplier
supplier_order_value = df.groupby("supplier_id")["order_value"].sum()

# Sort suppliers and select the top 10
top_10_suppliers_value = supplier_order_value.sort_values(
    ascending=False
).head(10)

# Prepare supplier names and order values in millions
labels = [
    f"{supplier}\n{value / 1000000:.2f}M"
    for supplier, value in top_10_suppliers_value.items()
]

# Create a treemap chart
plt.figure(figsize=(12, 7))

squarify.plot(
    sizes=top_10_suppliers_value.values,
    label=labels,
  
   color=[
    "#264653",  # Dark teal
    "#E76F51",  # Coral
    "#E9C46A",  # Mustard yellow
    "#2A9D8F",  # Green teal
    "#6D597A",  # Purple
    "#F4A261",  # Orange
    "#457B9D",  # Steel blue
    "#BC4749",  # Red
    "#8A9A5B",  # Olive green
    "#9D4EDD"   # Violet
],
    alpha=0.9,
    text_kwargs={"fontsize": 9}
)

# Add chart title
plt.title("Top 10 Suppliers by Total Order Value")

# Remove axes
plt.axis("off")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------------------------------------------
# Chart 9: What is the overall distribution of order statuses?

# Count the number of orders in each status
order_status_counts = df["status"].value_counts()

# Create a donut chart
plt.figure(figsize=(8, 8))

plt.pie(
    order_status_counts,
    labels=order_status_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#264653", "#E76F51", "#E9C46A", "#2A9D8F"],
    wedgeprops={"width": 0.4}
)

# Add chart title
plt.title("Overall Order Status Distribution")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------------------------



# Chart 10: How do monthly order volumes compare across years?

# Extract year and month from order date
df["year"] = df["ordered_at"].dt.year
df["month"] = df["ordered_at"].dt.month

# Group orders by year and month
monthly_orders = df.groupby(
    ["month", "year"]
)["purchase_order_id"].nunique().unstack(fill_value=0)

# Create a stacked column chart
monthly_orders.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    color=["#264653", "#E76F51", "#E9C46A"]
)

# Display values on each section of the stacked bars
for container in plt.gca().containers:
    plt.bar_label(container, label_type="center", fontsize=8)

# Add chart title and labels
plt.title("Monthly Order Comparison Across Years", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Number of Orders")

# Display month names instead of numbers
plt.xticks(
    range(12),
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    rotation=0
)

# Display year legend
plt.legend(title="Year")

# Adjust chart layout
plt.tight_layout()

# Display the chart
plt.show()

# -------------------------------------------------------------------------------


# Chart 11: Overall Supply Chain Performance (KPI Metrics)

# Calculate key business metrics
total_orders = df["purchase_order_id"].nunique()
total_suppliers = df["supplier_id"].nunique()
total_warehouses = df["warehouse_id"].nunique()
total_order_value = df["order_value"].sum()

# Display KPI values
print("\n--- Supply Chain Overview ---")
print(f"Total Orders: {total_orders:,}")
print(f"Total Suppliers: {total_suppliers:,}")
print(f"Total Warehouses: {total_warehouses:,}")
print(f"Total Order Value: {total_order_value:,.2f}")
