import pandas as pd
import numpy as np

# Load the data
try:
    df = pd.read_csv('orders.csv')
except FileNotFoundError:
    raise Exception("The file 'orders.csv' was not found. Please check the file path and try again.")

# Step 1: Rename Columns
try:
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
except KeyError as e:
    raise Exception(f"Column not found during renaming: {e}")

# Step 2: Assign Product IDs
try:
    # Create a mapping from product names to unique product IDs
    unique_products = df['product_name'].unique()
    product_id_mapping = {product: idx + 1 for idx, product in enumerate(unique_products)}

    # Add a new column 'product_id' using the mapping
    df['product_id'] = df['product_name'].map(product_id_mapping)
except KeyError:
    raise Exception("Column 'product_name' not found. Ensure the dataset contains the correct columns.")

# Step 3: Generate Customer IDs and Map to Orders
try:
    # Generate hypothetical customer IDs
    num_customers = 100  # Adjust based on the desired number of unique customers
    customer_ids = [f'cust_{i:04d}' for i in range(num_customers)]

    # Map order IDs to customer IDs ensuring some customers are repeated
    order_ids = df['order_id'].unique()
    assigned_customer_ids = np.random.choice(customer_ids, size=len(order_ids), replace=True)
    order_to_customer_map = dict(zip(order_ids, assigned_customer_ids))

    # Assign customer IDs to the dataset
    df['customer_id'] = df['order_id'].map(order_to_customer_map)
except KeyError:
    raise Exception("Column 'order_id' not found. Ensure the dataset contains the correct columns.")

# Step 4: Rearrange Columns
try:
    df = df[['order_id', 'customer_id', 'order_date', 'product_name', 'product_price', 'quantity']]
except KeyError as e:
    raise Exception(f"Column not found during rearranging: {e}")

# Step 5: Data Cleaning
# Check for missing values
missing_values = df.isnull().sum()
print("Missing values:\n", missing_values)

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
print("Duplicate rows:", duplicate_rows)

# Convert 'order_date' to datetime format
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Check for conversion issues
date_conversion_issues = df['order_date'].isna().sum()
print("Date conversion issues:", date_conversion_issues)

# Check for negative or zero values in 'product_price' and 'quantity'
negative_product_price = df[df['product_price'] <= 0].shape[0]
negative_quantity = df[df['quantity'] <= 0].shape[0]
print("Negative or zero product prices:", negative_product_price)
print("Negative or zero quantities:", negative_quantity)

# Save the cleaned data
df.to_csv('orders_rearranged.csv', index=False)

# Task 1: Calculate Monthly Revenue
try:
    df['total_revenue'] = df['product_price'] * df['quantity']
    df['month_year'] = df['order_date'].dt.to_period('M')
    monthly_revenue = df.groupby('month_year')['total_revenue'].sum().reset_index()
    print(monthly_revenue)
except KeyError as e:
    raise Exception(f"Error in calculating monthly revenue: {e}")

# Task 2: Calculate Product Revenue
try:
    product_revenue = df.groupby('product_name')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
    print(product_revenue)
except KeyError as e:
    raise Exception(f"Error in calculating product revenue: {e}")

# Task 3: Calculate Customer Revenue
try:
    customer_revenue = df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
    print(customer_revenue)
except KeyError as e:
    raise Exception(f"Error in calculating customer revenue: {e}")

# Task 4: Top 10 Customers by Revenue
try:
    top_10_customers = customer_revenue.head(10)
    print(top_10_customers)
except KeyError as e:
    raise Exception(f"Error in identifying top 10 customers: {e}")
