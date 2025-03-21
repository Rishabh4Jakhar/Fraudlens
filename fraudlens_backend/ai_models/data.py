import pandas as pd

# Load the dataset
df = pd.read_csv("transactions.csv")

# Display dataset info
print("Dataset Information:")
print(df.info())

# Display first few rows
print("\nFirst 5 rows:")
print(df.head())

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())



# Check for unique values in each column
print("\nUnique Values Per Column:")
print(df.nunique())
