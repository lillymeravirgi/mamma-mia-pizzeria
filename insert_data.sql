/*
Usage:
    Run this script AFTER creating the schema with ddl_script.sql:
        mysql -u root -p pizza_ordering < insert_data.sql
*/

INSERT INTO Ingredient (name, cost, is_vegan, is_vegetarian) VALUES
('Tomato Sauce', 0.50, TRUE, TRUE),
('Mozzarella', 1.00, FALSE, TRUE),
('Pepperoni', 1.50, FALSE, FALSE),
('Basil', 0.20, TRUE, TRUE),
('Mushrooms', 0.70, TRUE, TRUE),
('Onions', 0.40, TRUE, TRUE),
('Ham', 1.40, FALSE, FALSE),
('Pineapple', 0.80, TRUE, TRUE),
('Olives', 0.60, TRUE, TRUE),
('Vegan Cheese', 1.20, TRUE, TRUE);

INSERT INTO Pizza (name) VALUES
('Margherita'),
('Pepperoni'),
('Funghi'),
('Hawaiian'),
('Vegan Special');

-- Link pizzas ↔ ingredients
INSERT INTO PizzaIngredient (pizza_id, ingredient_id) VALUES
-- Margherita: Tomato, Mozzarella, Basil
(1,1),(1,2),(1,4),
-- Pepperoni: Tomato, Mozzarella, Pepperoni
(2,1),(2,2),(2,3),
-- Funghi: Tomato, Mozzarella, Mushrooms, Onions
(3,1),(3,2),(3,5),(3,6),
-- Hawaiian: Tomato, Mozzarella, Ham, Pineapple
(4,1),(4,2),(4,7),(4,8),
-- Vegan Special: Tomato, Vegan Cheese, Olives, Basil
(5,1),(5,10),(5,9),(5,4);


INSERT INTO Dessert (name, cost) VALUES
('Tiramisu', 3.50),
('Panna Cotta', 3.00),
('Gelato', 2.80);

INSERT INTO Drink (name, cost, is_alcoholic) VALUES
('Coca Cola', 2.00, FALSE),
('Sparkling Water', 1.50, FALSE),
('Beer', 3.50, TRUE),
('Red Wine', 4.50, TRUE);

INSERT INTO Customer (name, gender, birthdate, address, postcode, city, country) VALUES
('Mario Rossi', 'male', '1990-05-21', 'Via Roma 1', '00100', 'Rome', 'Italy'),
('Anna Bianchi', 'female', '1985-12-02', 'Corso Milano 10', '20100', 'Milan', 'Italy'),
('John Smith', 'male', '1992-03-14', 'Baker Street 221B', 'NW16XE', 'London', 'UK'),
('Emma Johnson', 'female', '1998-07-09', '5th Avenue 101', '10001', 'New York', 'USA'),
('Lucas Müller', 'male', '1988-11-23', 'Hauptstrasse 15', '10115', 'Berlin', 'Germany');

INSERT INTO Staff (name, gender, role, salary) VALUES
('Giovanni Verdi', 'male', 'chef', 2500.00),
('Luca Neri', 'male', 'driver', 1800.00),
('Giulia Rosa', 'female', 'driver', 1850.00),
('Sofia Blu', 'female', 'cashier', 1700.00),
('Marco Gialli', 'male', 'manager', 3000.00);

-- Delivery persons (linked to Staff IDs 2 and 3)
INSERT INTO DeliveryPerson (id, postcode, available) VALUES
(2, '00100', TRUE),
(3, '20100', TRUE);

INSERT INTO DiscountCode (code, is_valid, expiry_date) VALUES
('WELCOME10', TRUE, '2025-12-31'),
('BIRTHDAYFREE', TRUE, '2026-01-01'),
('LOYALTY2025', TRUE, '2025-12-31');

INSERT INTO `Order` (customer_id, delivery_id, status, total) VALUES
(1, 2, 'delivered', 10.00),
(2, 3, 'in delivery', 15.00),
(3, 2, 'pending', 20.00);

INSERT INTO OrderItem (order_id, product_type, product_id, quantity) VALUES
-- Order 1 (Mario Rossi): 1 Margherita, 1 Coke
(1, 'pizza', 1, 1),
(1, 'drink', 1, 1),

-- Order 2 (Anna Bianchi): 2 Pepperoni, 1 Beer
(2, 'pizza', 2, 2),
(2, 'drink', 3, 1),

-- Order 3 (John Smith): 1 Vegan Special, 1 Gelato, 1 Water
(3, 'pizza', 5, 1),
(3, 'dessert', 3, 1),
(3, 'drink', 2, 1);

-- Link discounts to orders
INSERT INTO OrderDiscount (order_id, discount_id) VALUES
(1, 1),
(3, 2);
