CREATE DATABASE IF NOT EXISTS orders;

USE orders;

CREATE TABLE IF NOT EXISTS orders_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(255),
    order_date DATE,
    product_name VARCHAR(255),
    quantity INT,
    product_price DECIMAL(10, 2)
);