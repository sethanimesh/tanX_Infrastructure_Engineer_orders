import pandas as pd

def calculate_customer_revenue(df):
    return df.groupby('customer_id')['total_revenue'].sum().reset_index()

def top_customers(customer_revenue, top_n=10):
    return customer_revenue.sort_values(by='total_revenue', ascending=False).head(top_n)