import pandas as pd

def calculate_product_revenue(df):
    return df.groupby('product_name')['total_revenue'].sum().reset_index()