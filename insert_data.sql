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
('Vegan Special');

INSERT INTO PizzaIngredient (pizza_id, ingredient_id) VALUES
-- Margherita: Tomato, Mozzarella, Basil
(1,1),(1,2),(1,4),
-- Pepperoni: Tomato, Mozzarella, Pepperoni
(2,1),(2,2),(2,3),
-- Funghi: Tomato, Mozzarella, Mushrooms, Onions
(3,1),(3,2),(3,5),(3,6),
-- Vegan Special: Tomato, Vegan Cheese, Olives, Basil
(4,1),(4,10),(4,9),(4,4);

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
('Lorenzo Ranchetti', 'male', '2005-02-14', 'Treviso Fiera', '31100', 'Treviso', 'Italy')
('Mario Rossi', 'male', '1990-05-21', 'Via Roma 1', '00100', 'Rome', 'Italy'),
('Anna Bianchi', 'female', '1985-12-02', 'Corso Milano 10', '20100', 'Milan', 'Italy'),
('John Smith', 'male', '1992-03-14', 'Baker Street 221B', 'NW16XE', 'London', 'UK'),
('Paul Peter Turnschuh', 'male', '1998-10-19', 'Kloßstraße 12', '10101', 'Bremen', 'Germany'),
('Kevin McCallister', 'male', '1990-08-26', '671 Lincoln Avenue', '10001', 'Winnetka', 'USA'),
('Emma Johnson', 'female', '1998-07-09', '5th Avenue 101', '10001', 'New York', 'USA'),
('Sven Marquardt', 'male', '1962-02-03', 'Hauptstrasse 15', '10115', 'Berlin', 'Germany');

INSERT INTO Staff (name, gender, role, salary, birthdate) VALUES
('Giovanni Verdi', 'male', 'chef', 2500.00, '1980-06-15'),
('Pippi Langstrumpf', 'female', 'manager', 4000.00, '1996-02-20'),
('Giulia Rosa', 'female', 'driver', 1850.00, '1992-08-05'),
('Sofia Blu', 'female', 'driver', 1900.00, '1975-03-25'),
('Einstein', 'male', 'driver', 1800.00, '1879-03-14'),
('Harry Potter', 'male', 'driver', 1800.00, '1999-02-02'),
('Harold Töpfer', 'male', 'driver', 1900.00, '1999-02-02'),
('Marco Gialli', 'male', 'cashier', 1700.00, '1988-11-10'),
;

INSERT INTO DeliveryPerson (id, postcode, available) VALUES
(7, '00100', TRUE), 
(6, 'NW16XE', TRUE),
(5, '10101', TRUE), 
(8, '20100', TRUE),
(4, '10115', TRUE);

INSERT INTO DiscountCode (code, is_valid, expiry_date) VALUES
('WELCOME10', TRUE, '2025-12-31'),
('BIRTHDAYFREE', TRUE, '2026-01-01'),
('LOYALTY2025', TRUE, '2025-12-31');

INSERT INTO `Order` (customer_id, delivery_id, status, total) VALUES
(1, 2, 'delivered', 12.50),
(1, 3, 'delivered', 18.20),
(1, 2, 'in delivery', 9.80),
(1, 3, 'pending', 15.00),
(1, 2, 'cancelled', 7.50),


(2, 3, 'delivered', 20.00),
(2, 2, 'in delivery', 14.50),
(2, 3, 'prepared', 16.30),
(2, 2, 'delivered', 25.00),
(2, 3, 'pending', 11.80),


(3, 2, 'delivered', 22.50),
(3, 3, 'in delivery', 17.00),
(3, 2, 'delivered', 19.80),
(3, 3, 'pending', 13.20),
(3, 2, 'prepared', 21.50),


(4, 3, 'delivered', 15.50),
(4, 2, 'in delivery', 12.70),
(4, 3, 'delivered', 23.00),
(4, 2, 'pending', 18.40),
(4, 3, 'cancelled', 9.50);

INSERT INTO OrderItem (order_id, product_type, product_id, quantity) VALUES

(1, 'pizza', 1, 1), (1, 'drink', 1, 1), (1, 'dessert', 1, 1),
(2, 'pizza', 2, 2), (2, 'drink', 3, 1),
(3, 'pizza', 3, 1),
(4, 'pizza', 4, 1), (4, 'dessert', 2, 1),
(5, 'pizza', 1, 1),


(6, 'pizza', 2, 1), (6, 'drink', 2, 2),
(7, 'pizza', 3, 2),
(8, 'pizza', 3, 1), (8, 'dessert', 3, 1), (8, 'drink', 4, 1),
(9, 'pizza', 4, 1), (9, 'drink', 1, 1),
(10, 'pizza', 1, 1),


(11, 'pizza', 4, 1), (11, 'dessert', 3, 1),
(12, 'pizza', 1, 2), (12, 'drink', 2, 1),
(13, 'pizza', 2, 1), (13, 'dessert', 1, 1),
(14, 'pizza', 3, 1), (14, 'drink', 1, 1),
(15, 'pizza', 2, 1),


(16, 'pizza', 1, 1), (16, 'dessert', 2, 1),
(17, 'pizza', 2, 1), (17, 'drink', 3, 1),
(18, 'pizza', 4, 1), (18, 'dessert', 3, 1),
(19, 'pizza', 3, 2),
(20, 'pizza', 2, 1), (20, 'drink', 1, 1);

INSERT INTO OrderDiscount (order_id, discount_id) VALUES
(1, 1), (2, 3), (6, 2), (11, 1), (18, 2);