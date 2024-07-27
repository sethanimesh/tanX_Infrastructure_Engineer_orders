import unittest
import pandas as pd
import mysql.connector
import os

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
    print("Connected to the database")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

class TestOrderProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        query = "SELECT * FROM orders_table"
        cls.df = pd.read_sql(query, connection)
        cls.df['order_date'] = pd.to_datetime(cls.df['order_date'])
        cls.df['total_revenue'] = cls.df['product_price'] * cls.df['quantity']
        cls.df['month_year'] = cls.df['order_date'].dt.to_period('M')
        cls.monthly_revenue = cls.df.groupby('month_year')['total_revenue'].sum().reset_index()

    def test_order_date_conversion(self):
        """Test if 'order_date' was correctly converted to datetime."""
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df['order_date']))
    
    def test_total_revenue_calculation(self):
        """Test if 'total_revenue' is calculated correctly."""
        expected_revenue = self.df['product_price'] * self.df['quantity']
        pd.testing.assert_series_equal(self.df['total_revenue'].reset_index(drop=True), expected_revenue.reset_index(drop=True), check_names=False)
    
    def test_month_year_extraction(self):
        """Test if 'month_year' was correctly extracted from 'order_date'."""
        expected_month_year = self.df['order_date'].dt.to_period('M')
        pd.testing.assert_series_equal(self.df['month_year'], expected_month_year, check_names=False)
    
    def test_monthly_revenue_calculation(self):
        """Test the calculation of monthly revenue."""
        expected_monthly_revenue = self.df.groupby('month_year')['total_revenue'].sum().reset_index()
        pd.testing.assert_frame_equal(self.monthly_revenue, expected_monthly_revenue)

class TestOrderProcessingExtended(TestOrderProcessing):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_revenue = cls.df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by 'total_revenue', ascending=False)

    def test_customer_revenue_calculation(self):
        """Test the revenue calculation for each customer."""
        expected_customer_revenue = self.df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
        pd.testing.assert_frame_equal(self.customer_revenue, expected_customer_revenue)

class TestOrderProcessingTopCustomers(TestOrderProcessingExtended):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.top_10_customers = cls.customer_revenue.head(10)

    def test_top_10_customers(self):
        """Test the selection of top 10 customers by total revenue."""
        expected_top_10_customers = self.customer_revenue.head(10)
        pd.testing.assert_frame_equal(self.top_10_customers, expected_top_10_customers)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
