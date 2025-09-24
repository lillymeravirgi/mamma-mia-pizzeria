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
    ROUND(SUM(i.cost) * 1.4 * 1.09,2) AS price,
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

