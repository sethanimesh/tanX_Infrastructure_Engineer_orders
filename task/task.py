import pandas as pd
import numpy as np
import unittest

# Load the data
df = pd.read_csv('tasks/orders.csv')

# Step 1: Rename Columns
# Define a mapping for column names to more convenient ones
column_mapping = {
    'Order Number': 'order_id',
    'Order Date': 'order_date',
    'Item Name': 'product_name',
    'Quantity': 'quantity',
    'Product Price': 'product_price',
    'Total products': 'total_products'
}

# Rename the columns
df.rename(columns=column_mapping, inplace=True)

# Step 2: Assign Product IDs
# Create a mapping from product names to unique product IDs
unique_products = df['product_name'].unique()
product_id_mapping = {product: idx + 1 for idx, product in enumerate(unique_products)}

# Add a new column 'product_id' using the mapping
df['product_id'] = df['product_name'].map(product_id_mapping)

# Step 3: Generate Customer IDs and Map to Orders
# Generate hypothetical customer IDs
num_customers = 100  # Adjust based on the desired number of unique customers
customer_ids = [f'cust_{i:04d}' for i in range(num_customers)]

# Map order IDs to customer IDs ensuring some customers are repeated
order_ids = df['order_id'].unique()
assigned_customer_ids = np.random.choice(customer_ids, size=len(order_ids), replace=True)
order_to_customer_map = dict(zip(order_ids, assigned_customer_ids))

# Assign customer IDs to the dataset
df['customer_id'] = df['order_id'].map(order_to_customer_map)

# Step 4: Rearrange Columns
df = df[['order_id', 'customer_id', 'order_date', 'product_name', 'product_price', 'quantity']]

# Step 5: Data Cleaning
# Check for missing values
missing_values = df.isnull().sum()

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()

# Convert 'order_date' to datetime format
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Check for conversion issues
date_conversion_issues = df['order_date'].isna().sum()

# Check for negative or zero values in 'product_price' and 'quantity'
negative_product_price = df[df['product_price'] <= 0].shape[0]
negative_quantity = df[df['quantity'] <= 0].shape[0]

# Save the cleaned data
df.to_csv('orders_rearranged.csv', index=False)

# Task 1: Calculate Monthly Revenue
df['total_revenue'] = df['product_price'] * df['quantity']
df['month_year'] = df['order_date'].dt.to_period('M')
monthly_revenue = df.groupby('month_year')['total_revenue'].sum().reset_index()
print(monthly_revenue)

# Task 2: Calculate Product Revenue
product_revenue = df.groupby('product_name')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
print(product_revenue)

# Task 3: Calculate Customer Revenue
customer_revenue = df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
print(customer_revenue)

# Task 4: Top 10 Customers by Revenue
top_10_customers = customer_revenue.head(10)
print(top_10_customers)