import pandas as pd
from order_processing import load_data, generate_customer_ids, clean_data, save_data
from customer_analysis import calculate_customer_revenue, top_customers
from product_analysis import calculate_product_revenue

def main():
    df = load_data('/task/orders.csv')
    df = generate_customer_ids(df)
    df = clean_data(df)
    save_data(df, 'orders_processed.csv')

    # Monthly Revenue
    monthly_revenue = df.groupby('month_year')['total_revenue'].sum().reset_index()
    print("Monthly Revenue:\n", monthly_revenue)

    # Product Revenue
    product_revenue = calculate_product_revenue(df)
    print("Product Revenue:\n", product_revenue)

    # Customer Revenue
    customer_revenue = calculate_customer_revenue(df)
    print("Customer Revenue:\n", customer_revenue)

    # Top 10 Customers
    top_10_customers = top_customers(customer_revenue)
    print("Top 10 Customers:\n", top_10_customers)

if __name__ == "__main__":
    main()