set -e

while ! mysqladmin ping -h"$DB_HOST" --silent; do
    sleep 1
done

mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<EOF
LOAD DATA INFILE 'task/orders.csv'
INTO TABLE orders_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_date, product_name, quantity, product_price);
EOF
