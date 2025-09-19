INSERT INTO Ingredient (name, cost, is_vegan, is_vegetarian) VALUES
('Tomato', 0.50, TRUE, TRUE),
('Mozzarella', 1.00, FALSE, TRUE),
('Pepperoni', 1.50, FALSE, FALSE),
('Basil', 0.20, TRUE, TRUE);

INSERT INTO Pizza (name) VALUES
('Margherita'),
('Pepperoni');

INSERT INTO PizzaIngredient (pizza_id, ingredient_id) VALUES
(1, 1), (1, 2), (1, 4),
(2, 1), (2, 2), (2, 3);

INSERT INTO Customer (name, birthdate, address, postcode) VALUES
('Mario Rossi', '1990-05-21', 'Via Roma 1, Rome', '00100'),
('Anna Bianchi', '1985-12-02', 'Corso Milano 10, Milan', '20100');

INSERT INTO DeliveryPerson (name, postcode) VALUES
('Luca', '00100'),
('Giulia', '20100');

INSERT INTO `Order` (customer_id, delivery_id, total) VALUES
(1, 1, 10.00),
(2, 2, 15.00);

INSERT INTO OrderItem (order_id, pizza_id, quantity) VALUES
(1, 1, 1),
(2, 2, 2);
