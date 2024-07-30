CREATE DATABASE IF NOT EXISTS orders;
USE orders;

-- Table schema for orders
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(255),
    customer_id VARCHAR(255),
    order_date DATE,
    product_name VARCHAR(255),
    product_price DECIMAL(10, 2),
    quantity INT,
    total_revenue DECIMAL(10, 2),
    PRIMARY KEY (order_id)
);

-- Load data from the CSV file
LOAD DATA INFILE '/Users/animesh/Documents/Applications/tanX Complete/tanX/task/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;