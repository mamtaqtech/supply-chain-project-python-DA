import pandas as pd 
df = pd.read_csv("supply_chain_inventory.csv", encoding="latin1")

print(df.head(2))
print(df.columns)

#BUSINESS PROBLEM 1:
#How many orders received less items than actually been ordered 
short_received_orders = df[df["quantity_received"] < df["quantity_ordered"]]

print(short_received_orders)

#number of orders which received less items 
print(len(short_received_orders))

#printing required columns 
print(short_received_orders[["purchase_order_id","status","supplier_id",
"quantity_ordered","quantity_received"]])

#order status and count of less received orders by each status 
print("less received orders status  :" ,short_received_orders["status"].value_counts())

"""less received orders status  : status
partial      1326
open          467
cancelled     406"""

# what we got to know is 
"""CONCLUSION:
Out of 18000 total orders, 2199 orders received fewer items than ordered.
These include 1326 partial, 467 open and 406 cancelled orders.
Partial orders indicate incomplete deliveries, while open orders may still
be in progress and cancelled orders may not have been fulfilled.
This analysis helps identify orders that need attention."""
#------------------------------------------------------------------------------------------------------##

#BUSINESS PROBLEM 2:

#partially received orders
partial_orders = df[df["status"]=="partial"]
print(partial_orders)

#Count partial orders for each supplier
suppliers_partial_orders = (partial_orders["supplier_id"].value_counts())
print("suppliars which have partial orders and their count\n",suppliers_partial_orders)


#1326 suppliers have partial order status 
#SUPPLIERS WITH THE MOST PARTIAL ORDERS

print('suppliers with most partial orders top 10 ')
print(suppliers_partial_orders.head(10))

"""CONCLUSION:
We found 1326 partially received orders across 250 suppliers
SUP0210 and SUP0178 have the highest number of partial orders,with 12 each
SUP0030,SUP0038,SUP0128 ,SUP0173 follow with 11 each
This analysis helps identify suppliers with the most incomplete deliveries
and monitor their delivery performance"""

# -------------------------------------------------------------------------------------------------------

# BUSINESS PROBLEM 3:

# Which suppliers have the highest percentage of partially received orders?

# 1.Counting the total orders for each supplier
supplier_total_orders = (df["supplier_id"].value_counts())
print("total orders by each supplier :",supplier_total_orders)

#Calculatting the percentage of partial orders for each supplier
supplier_partial_percentage = (suppliers_partial_orders/supplier_total_orders)*100
print("each suppliers partial orders in percentage :")
print(supplier_partial_percentage)

# Sorting suppliers by percentage, from highest to lowest
supplier_partial_percentage = supplier_partial_percentage.sort_values(ascending=False)
print("supplier partial percentage from highest to lowest")
print(supplier_partial_percentage)

#top 10 suppliers with highest partial orders 
print("top 10 suppliers with highest partial orders:")
print(supplier_partial_percentage.head(10))

"""CONCLUSION:
SUP0210 has the highest percentage of partial orders at 17.14%
SUP0178 follows with 16.22%, while SUP0037 has 14.93%
SUP0030 and SUP0118 also have high partial order percentages
This analysis helps identify suppliers with a higher proportion of
incomplete orders compared to their total orders"""

# ----------------------------------------------------------------------------------------------------------------

""" BUSINESS PROBLEM 4:"""

# Which suppliers have the most delayed deliveries?
print(df.columns)
print(df[["supplier_id","ordered_at","expected_at","received_at"]])

# Convert date columns into datetime format
df['ordered_at'] = pd.to_datetime(df["ordered_at"])
df["expected_at"] = pd.to_datetime(df["expected_at"])
df["received_at"] = pd.to_datetime(df["received_at"])


# Consider only orders that have been received
received_orders = df[df["received_at"].notna()].copy()
print("--------------------------------------------------")
print(received_orders)   #this is a new dataset which does not include the orders which recieved at dates are missing 

# Calculate delivery delay in days

received_orders["delivery_delay_days"] = (
received_orders["received_at"] - received_orders["expected_at"]
).dt.days

# Calculate delivery delay in days
received_orders["delivery_delay_days"] = (received_orders["received_at"]-received_orders["expected_at"]).dt.days
print(received_orders['delivery_delay_days'])

#Considering only delayed orders
delayed_orders = received_orders[received_orders['delivery_delay_days']>0]
print("delayed orders")
print(delayed_orders)

# Count delayed orders for each supplier
supplier_delayed_orders = delayed_orders["supplier_id"].value_counts()
print("supplier delayed orders ")
print(supplier_delayed_orders)

#top 10 suppliers with the most delayed deliveries
print("suppliers with most delayed delieveries :")
print(supplier_delayed_orders.head(10))

"""CONCLUSION:
SUP0170 has the highest number of delayed deliveries,with 70 orders
SUP0150 follows with 69 delayed orders,while SUP0234 and SUP0244 have
68 each
This analysis helps identify suppliers with frequent delivery delays
and monitor their delivery performance"""

#-----------------------------------------------------------------------------------------------------------------
"""BUSINESS PROBLEM 5"""

#Which suppliers have the longest average delivery time?

#Calculating delivery time in days

received_orders["delivery_time_days"] = (received_orders["received_at"] - received_orders["ordered_at"]).dt.days
print(received_orders['delivery_delay_days'])

#Calculating the average delivery time for each supplier

supplier_avg_delivery_time = (received_orders.groupby("supplier_id")["delivery_time_days"].mean())
print("suppliers average delievery Time : ")
print(supplier_avg_delivery_time)
#Sorting suppliers by average delivery time from hifhest to lowest 

supplier_avg_delivery_time = supplier_avg_delivery_time.sort_values(ascending=False)
print("suppliers avg delievery time from hgest to lowest :")
print(supplier_avg_delivery_time)

#top 10 suppliers with the longest average delivery time
print("top 10 suppliers who took longest average Time : ")
print(supplier_avg_delivery_time.head(10))

"""CONCLUSION:
SUP0093 has the longest average delivery time of approximately 65.73 days
SUP0118 follows with 65.23 days,while SUP0090 takes approximately 64.91 days
SUP0142 and SUP0086 are also among the suppliers with the longest
average delivery times
This analysis helps identify suppliers who take longer to deliver orders
and improve delivery planning"""

# ----------------------------------------------------------------------------------------------------

"""BUSINESS PROBLEM 6:"""

# Which countries have he most orders?
# ---------------
# Count the total orders from each supplier country
country_orders = df["supplier_country"].value_counts()
print("total orders from each supplier country :")
print(country_orders)

# top 10 countries with the most orders
print("top 10 supplier countries with highest orders ")
print(country_orders.head(10))

"""CONCLUSION:
Germany (DE) has the highest number of orders, with 3038
Poland (PL) follows with 2786 orders, while China (CN) has 2703 orders
Canada (CA), Vietnam (VN), the United States (US) and Mexico (MX)
are the other supplier countries in the results
This analysis helps identify the main sourcing countries
and understand where most orders come from"""
 
# -------------------------------------------------------------------------------------------------

"""BUSINESS PROBLEM 7"""

# Which warehouses receive the highest order quantities?"""
# calculating total quantity ordered for each warehouse

warehouse_order_quantity = (df.groupby("warehouse_id")["quantity_ordered"].sum())
print("warehouse order quantity by each warehouse :")
print(warehouse_order_quantity)

# Sorting warehouses from highest to lowest quantity
warehouse_order_quantity = warehouse_order_quantity.sort_values(ascending=False)
print("warehouse order quantities from highest to lowest :")
print(warehouse_order_quantity)

#Displaying the top 10 warehouses
print("top 10 warehouese which recieve highest orders :")
print(warehouse_order_quantity.head(10))

"""CONCLUSION:
W001 has the highest total order quantity with 1454460 units
W010 and W004 are the next highest warehouses
This analysis helps identify warehouses with the highest workload and plan 
storage space and resources accordingly"""

# ---------------------------------------------------------------------------------------------------------------

"""BUSINESS PROBLEM 8"""
# Which suppliers have the highest total order value?
# -----

#Calculating total order value for each supplier
supplier_order_value = df.groupby ('supplier_id')["order_value"].sum()
print("total order value by each supplier ;")
print(supplier_order_value)

#Sort suppliers from highest to lowest order value
supplier_order_value = supplier_order_value.sort_values(ascending=False)
print("sorting supplie with highest to lowest order value ;")
print(supplier_order_value)

#top 10 suppliers with highest order value 
print ('print top 10 suppliers with highest order value :')
print(supplier_order_value.head(10))

"""CONCLUSION:

SUP0141 has the highest total order value of 44444255.30
SUP0188 and SUP0017 are the next highest suppliers
This analysis helps identify suppliers with the highest purchase value
and understand where the business spends the most money"""

# --------------------------------------------------------------------------------------------------------------