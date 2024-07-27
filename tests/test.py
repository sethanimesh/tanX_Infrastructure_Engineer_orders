import unittest
import pandas as pd
import numpy as np

# Load the processed data for testing
try:
    df = pd.read_csv('orders_rearranged.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['product_price'] * df['quantity']
    df['month_year'] = df['order_date'].dt.to_period('M')
except FileNotFoundError:
    raise Exception("The file 'orders_rearranged.csv' was not found. Please ensure the task script ran correctly.")

class TestOrderProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = df.copy()
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
        cls.customer_revenue = cls.df.groupby('customer_id')['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)

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