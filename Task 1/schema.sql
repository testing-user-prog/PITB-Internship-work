CREATE TABLE products (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    image VARCHAR(255),
    rating_rate DECIMAL(3, 2)
);


CREATE TABLE customers (
    id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(100),
    city VARCHAR(100),
    street VARCHAR(150),
    street_number INT,
    zipcode VARCHAR(20)
);

CREATE TABLE orders (
    id INT,          
    customer_id INT REFERENCES customers(id),
    order_date TIMESTAMP NOT NULL,
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (id, product_id)  
);

select * from orders

CREATE TABLE payments (
    id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
    order_id INT,                
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL,
    payment_date TIMESTAMP NOT null
    
);

