/*
Usage:
    Run queries interactively in MySQL Workbench or via CLI:
        mysql -u root -p pizza_ordering < queries.sql
*/

-- 1. VIEW: Calculate pizza price dynamically (ingredients + 40% margin + 9% VAT)
DROP VIEW IF EXISTS PizzaMenu;
CREATE VIEW PizzaMenu AS
SELECT
    p.id AS pizza_id,
    p.name AS pizza_name,
    ROUND(SUM(i.cost) * 1.4 * 1.09+5,2) AS price,
    MIN(CASE WHEN i.is_vegan = FALSE THEN 0 ELSE 1 END) AS is_vegan,
    MIN(CASE WHEN i.is_vegetarian = FALSE THEN 0 ELSE 1 END) AS is_vegetarian
FROM Pizza p
JOIN PizzaIngredient pi ON p.id = pi.pizza_id
JOIN Ingredient i ON pi.ingredient_id = i.id
GROUP BY p.id, p.name;

-- 2. Show full menu
SELECT * FROM PizzaMenu;
SELECT * FROM Dessert;
SELECT * FROM Drink;

-- 3. Write complex SQL queries: Top-selling pizzas
SELECT
    pm.pizza_name,
    SUM(oi.quantity) AS total_sold
FROM OrderItem oi
JOIN PizzaMenu pm ON oi.product_type = 'pizza' AND oi.product_id = pm.pizza_id
GROUP BY pm.pizza_name
ORDER BY total_sold DESC
LIMIT 3;

-- 4. Write complex SQL queries: Undelivered orders
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.status,
    o.total,
    o.order_time
FROM `Order` o
JOIN Customer c ON o.customer_id = c.id
WHERE o.status != 'delivered';

-- 5. Write complex SQL queries: Monthly earnings by gender, age, postal code
SELECT
    s.gender,
    CASE
        WHEN TIMESTAMPDIFF(YEAR, s.birthdate, CURDATE()) < 25 THEN 'Under 25'
        WHEN TIMESTAMPDIFF(YEAR, s.birthdate, CURDATE()) BETWEEN 25 AND 35 THEN '25-35'
        WHEN TIMESTAMPDIFF(YEAR, s.birthdate, CURDATE()) BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    COALESCE(dp.postcode, 'N/A') AS postcode,
    AVG(s.salary) AS avg_salary
FROM Staff s
LEFT JOIN DeliveryPerson dp ON s.id = dp.id
GROUP BY s.gender, age_group, dp.postcode
ORDER BY s.gender, age_group, dp.postcode;