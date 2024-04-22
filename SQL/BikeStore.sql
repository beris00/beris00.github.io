
--Creating tables for our data
Create table customers(
customer_id SMALLINT,
first_name VARCHAR(30),
last_name VARCHAR(30),
phone VARCHAR(25),
email VARCHAR(45),
street VARCHAR(30),
city VARCHAR(30),
state VARCHAR(20),
zip_code VARCHAR(10),
PRIMARY KEY(customer_id));

CREATE TABLE stores(
store_id INT,
store_name VARCHAR(25),
phone VARCHAR (25),
email VARCHAR (45),
street VARCHAR(30),
city VARCHAR(30),
state VARCHAR(20),
zip_code VARCHAR(10),
PRIMARY KEY(store_id));


CREATE TABLE orders(
order_id INT,
customer_id SMALLINT,
order_status SMALLINT,
--1 = Pending, 2 = Processing, 2 = Rejected, 4 = Completed
order_date DATE,
required_date DATE,
shipped_date VARCHAR(15),
store_id INT,
staff_id INT,
PRIMARY KEY(order_id),
FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
FOREIGN KEY(store_id) REFERENCES stores (store_id));


CREATE TABLE order_items(
order_id INT,
item_id INT,
product_id INT,
quantity SMALLINT,
list_price DECIMAL(7,2),
discount DECIMAL(4, 4),
PRIMARY KEY (order_id, item_id),
FOREIGN KEY (order_id) REFERENCES orders(order_id));


--Importing the excel files to fill our tables
COPY customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code)
FROM 'C:\Users\Public\customers.csv' DELIMITER ',' CSV HEADER;

COPY stores(store_id, store_name, phone, email, street, city, state, zip_code)
FROM 'C:\Users\Public\stores.csv' DELIMITER ',' CSV HEADER;

COPY orders(order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id)
FROM 'C:\Users\Public\orders.csv' DELIMITER ',' CSV HEADER;

COPY order_items(order_id, item_id, product_id, quantity, list_price, discount)
FROM 'C:\Users\Public\order_items.csv' DELIMITER ',' CSV HEADER;

-- The data is now available to query.

--An example is to see all orders still to be completed
SELECT order_id, order_status
FROM orders
WHERE order_status = 1 
OR order_status = 2
--We can see that the Bike Store has 125 orders to be completed.

--Supose a manager wanted to know how many orders the California store has.
SELECT COUNT (order_id)
FROM orders
JOIN stores on orders.store_id=stores.store_id
WHERE state = 'CA';

