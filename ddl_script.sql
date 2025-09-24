/*
Usage: 
    Run this script in MySQL to create the database schema.
Example:
    mysql -u root -p pizza_ordering < ddl_script.sql
*/

-- INGREDIENTS
CREATE TABLE Ingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    cost DECIMAL(5,2) NOT NULL CHECK (cost > 0),
    is_vegan BOOLEAN NOT NULL,
    is_vegetarian BOOLEAN NOT NULL
);

-- PIZZAS
CREATE TABLE Pizza (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- MANY-TO-MANY: Pizza ↔ Ingredient
CREATE TABLE PizzaIngredient (
    pizza_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    PRIMARY KEY(pizza_id, ingredient_id),
    FOREIGN KEY(pizza_id) REFERENCES Pizza(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(ingredient_id) REFERENCES Ingredient(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- DESSERTS
CREATE TABLE Dessert (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    cost DECIMAL(5,2) NOT NULL CHECK (cost > 0)
);

-- DRINKS
CREATE TABLE Drink (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    cost DECIMAL(5,2) NOT NULL CHECK (cost > 0),
    is_alcoholic BOOLEAN NOT NULL DEFAULT FALSE
);

-- CUSTOMERS
CREATE TABLE Customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('male','female','other') NOT NULL,
    birthdate DATE NOT NULL,  -- removed CHECK (birthdate < CURDATE())
    address VARCHAR(255) NOT NULL,
    postcode VARCHAR(20) NOT NULL,
    city VARCHAR(50),
    country VARCHAR(50),
    pizzas_ordered_count INT NOT NULL DEFAULT 0
);

-- STAFF (parent table for all employees)
CREATE TABLE Staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('male','female','other') NOT NULL,
    role ENUM('chef','driver','cashier','manager') NOT NULL,
    salary DECIMAL(8,2) NOT NULL CHECK (salary >= 0)
);

-- DELIVERY PERSONS (subset of Staff, linked by shared ID)
CREATE TABLE DeliveryPerson (
    id INT PRIMARY KEY,
    postcode VARCHAR(20) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY(id) REFERENCES Staff(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ORDERS
CREATE TABLE 'Order' (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    delivery_id INT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending','in preparation','prepared','in delivery','delivered','cancelled')
        NOT NULL DEFAULT 'pending',
    total DECIMAL(8,2),
    FOREIGN KEY(customer_id) REFERENCES Customer(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(delivery_id) REFERENCES DeliveryPerson(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- ORDER ITEMS (supports pizzas, drinks, desserts)
CREATE TABLE OrderItem (
    order_id INT NOT NULL,
    product_type ENUM('pizza','drink','dessert') NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY(order_id, product_type, product_id),
    FOREIGN KEY(order_id) REFERENCES `Order`(id) ON DELETE CASCADE ON UPDATE CASCADE
    -- product_id references depend on product_type (handled at application/query level)
);

-- DISCOUNT CODES
CREATE TABLE DiscountCode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    is_valid BOOLEAN NOT NULL DEFAULT TRUE,
    expiry_date DATE
);

-- TABLE TO LINK DISCOUNTS WITH ORDERS
CREATE TABLE OrderDiscount (
    order_id INT NOT NULL,
    discount_id INT NOT NULL,
    PRIMARY KEY(order_id, discount_id),
    FOREIGN KEY(order_id) REFERENCES `Order`(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(discount_id) REFERENCES DiscountCode(id) ON DELETE CASCADE ON UPDATE CASCADE
);
