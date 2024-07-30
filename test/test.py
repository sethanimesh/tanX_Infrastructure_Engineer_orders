import unittest
import pandas as pd
from order_processing import load_data, clean_data
from customer_analysis import calculate_customer_revenue
from product_analysis import calculate_product_revenue

class TestOrderProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_data('orders.csv')
        cls.df = clean_data(cls.df)

    def test_order_date_conversion(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df['order_date']))

    def test_total_revenue_calculation(self):
        expected_revenue = self.df['product_price'] * self.df['quantity']
        pd.testing.assert_series_equal(self.df['total_revenue'], expected_revenue)

    def test_month_year_extraction(self):
        expected_month_year = self.df['order_date'].dt.to_period('M')
        pd.testing.assert_series_equal(self.df['month_year'], expected_month_year)

    def test_product_revenue_calculation(self):
        expected_product_revenue = calculate_product_revenue(self.df)
        product_revenue = calculate_product_revenue(self.df)
        pd.testing.assert_frame_equal(product_revenue, expected_product_revenue)

    def test_customer_revenue_calculation(self):
        expected_customer_revenue = calculate_customer_revenue(self.df)
        customer_revenue = calculate_customer_revenue(self.df)
        pd.testing.assert_frame_equal(customer_revenue, expected_customer_revenue)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)