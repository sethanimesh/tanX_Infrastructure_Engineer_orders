import pandas as pd
import mysql.connector
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection settings
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'orders')

# Establish a connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    logger.info("Connected to the database")
except mysql.connector.Error as err:
    logger.error(f"Error connecting to the database: {err}")
    exit(1)

try:
    # Load the data from the MySQL database
    query = "SELECT * FROM orders_table"
    df = pd.read_sql(query, connection)

    # Process the data
    # Step 1: Rename Columns (if necessary)
    column_mapping = {
        'order_id': 'order_id',
        'order_date': 'order_date',
        'product_name': 'product_name',
        'quantity': 'quantity',
        'product_price': 'product_price'
    }

    df.rename(columns=column_mapping, inplace=True)

    # Step 2: Assign Product IDs
    unique_products = df['product_name'].unique()
    product_id_mapping = {product: idx + 1 for idx, product in enumerate(unique_products)}
    df['product_id'] = df['product_name'].map(product_id_mapping)

    # Step 3: Generate Customer IDs and Map to Orders
    num_customers = 100
    customer_ids = [f'cust_{i:04d}' for i in range(num_customers)]
    order_ids = df['order_id'].unique()
    assigned_customer_ids = np.random.choice(customer_ids, size=len(order_ids), replace=True)
    order_to_customer_map = dict(zip(order_ids, assigned_customer_ids))
    df['customer_id'] = df['order_id'].map(order_to_customer_map)

    # Step 4: Data Cleaning
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df.dropna(subset=['order_date'], inplace=True)
    df = df[df['product_price'] > 0]
    df = df[df['quantity'] > 0]

    # Task: Calculate Metrics
    df['total_revenue'] = df['product_price'] * df['quantity']
    df['month_year'] = df['order_date'].dt.to_period('M')

    monthly_revenue = df.groupby('month_year')['total_revenue'].sum().reset_index()
    product_revenue = df.groupby('product_name')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
    customer_revenue = df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)

    # Output the metrics (you can also save these to the database or a file if needed)
    logger.info("Monthly Revenue:")
    logger.info(monthly_revenue)
    logger.info("\nProduct Revenue:")
    logger.info(product_revenue)
    logger.info("\nCustomer Revenue:")
    logger.info(customer_revenue)

except pd.io.sql.DatabaseError as db_err:
    logger.error(f"Error querying the database: {db_err}")
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    # Close the database connection
    try:
        connection.close()
        logger.info("Database connection closed")
    except mysql.connector.Error as err:
        logger.error(f"Error closing the database connection: {err}")
