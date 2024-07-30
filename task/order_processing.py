import pandas as pd
import numpy as np

def load_data(filepath):
    df = pd.read_csv(filepath)
    column_mapping = {
        'Order Number': 'order_id',
        'Order Date': 'order_date',
        'Item Name': 'product_name',
        'Quantity': 'quantity',
        'Product Price': 'product_price',
        'Total products': 'total_products'
    }
    df.rename(columns=column_mapping, inplace=True)
    return df

def generate_customer_ids(df, num_customers=100):
    customer_ids = [f'cust_{i:04d}' for i in range(num_customers)]
    order_ids = df['order_id'].unique()
    assigned_customer_ids = np.random.choice(customer_ids, size=len(order_ids), replace=True)
    order_to_customer_map = dict(zip(order_ids, assigned_customer_ids))
    df['customer_id'] = df['order_id'].map(order_to_customer_map)
    return df

def clean_data(df):
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df[df['product_price'] > 0]
    df = df[df['quantity'] > 0]
    df['total_revenue'] = df['product_price'] * df['quantity']
    df['month_year'] = df['order_date'].dt.to_period('M')
    return df

def save_data(df, filepath):
    df.to_csv(filepath, index=False)