import pandas as pd

# How can we load the supply chain dataset into Python?
df = pd.read_csv("supply_chain_inventory.csv", encoding="latin1")
# - encoding → Specifies how characters are encoded in a file.
# - latin1 → One character maps to each possible byte value, 
# so it can avoid many decoding errors.
# - Why you're using it → 
# To read your supply_chain_inventory CSV file without the Unicode decoding 
# error you encountered.
# Important: latin1 can prevent a decoding error, 
# but it doesn't guarantee that every character will display 
# correctly if the file uses a different encoding.

# What are the first five records in the dataset?
print(df.head())

# What columns and data types are present?
print("\nDataset Information:")
print(df.info())

# How many rows and columns does the dataset contain?
print("\nDataset Shape:")
print(df.shape)
print("number of rows = ",df.shape[0])
print("number of  = columns",df.shape[1])

# What are the names of all columns?
print(df.columns)

# What are the average, minimum, and maximum values of the numeric columns?
print(df.describe())


# Are there missing values in the dataset?
print(df.isna())
print(df.isnull().sum())

# How many complete rows are duplicated?
print("duplicated rows = ",df.duplicated().sum())

# What are the first three records?
print(df.head(3))

## What are the different order statuses?
print(df["status"].value_counts(dropna=False))


#working on missing values .. ie 873 received_at (date) missing values 
# What is the status of orders that have no received_at date?
# First, select rows where received_at is missing
missing_received_dates = df[df["received_at"].isna()]

# Then, count the statuses of those orders
print("missing :" ,missing_received_dates["status"].value_counts())

#we have 467 open orders have no received_at dates 
#and we have 406 cancelled orders which have no received_at dates 

# dates appear reasonable given the order statuses.
# Therefore, we will retain these rows and leave the missing dates unchanged.