-- Ingredients
CREATE TABLE Ingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    cost DECIMAL(5,2) NOT NULL CHECK (cost > 0),
    is_vegan BOOLEAN NOT NULL,
    is_vegetarian BOOLEAN NOT NULL
);

-- Pizzas
CREATE TABLE Pizza (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- PizzaIngredient (many-to-many relationship)
CREATE TABLE PizzaIngredient (
    pizza_id INT,
    ingredient_id INT,
    PRIMARY KEY(pizza_id, ingredient_id),
    FOREIGN KEY(pizza_id) REFERENCES Pizza(id),
    FOREIGN KEY(ingredient_id) REFERENCES Ingredient(id)
);

-- Customers
CREATE TABLE Customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthdate DATE,
    address VARCHAR(255),
    postcode VARCHAR(20)
);

-- Delivery Persons
CREATE TABLE DeliveryPerson (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    postcode VARCHAR(20)
);

-- Orders
CREATE TABLE `Order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    delivery_id INT,
    total DECIMAL(8,2),
    FOREIGN KEY(customer_id) REFERENCES Customer(id),
    FOREIGN KEY(delivery_id) REFERENCES DeliveryPerson(id)
);

-- OrderItems
CREATE TABLE OrderItem (
    order_id INT,
    pizza_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY(order_id, pizza_id),
    FOREIGN KEY(order_id) REFERENCES `Order`(id),
    FOREIGN KEY(pizza_id) REFERENCES Pizza(id)
);
