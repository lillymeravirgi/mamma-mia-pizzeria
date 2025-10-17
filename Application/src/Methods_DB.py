import mysql.connector

from Application.src.ORMMapping import SessionLocal
from Application.src.models import OrderItem

def connectDB():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ponzano05",
    database="pizza_ordering"
)

def getDrinkMenu(): 
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, cost, is_alcoholic FROM Drink")
    rows = cursor.fetchall()
    return rows

def getDessertMenu(): 
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, cost FROM Dessert")
    rows = cursor.fetchall()
    return rows

def printMenu():
    conn = connectDB()
    cursor = conn.cursor()

    print("🍕 Pizzas:")
    pizzas = getPizzaMenu()
    for name, price, vegetarian, vegan in pizzas:
        tags = []
        if vegetarian:
            tags.append("🌱 Veggie")
        if vegan:
            tags.append("🥦 Vegan")
        tag_str = " ".join(tags) if tags else ""
        print(f"- {name}: €{price:.2f} {tag_str}")

    print("\n🥤 Drinks:")
    cursor.execute("SELECT name, cost, is_alcoholic FROM Drink")
    for name, price, is_alcoholic in cursor.fetchall():
        
        tag_str = "🍷 Alcoholic" if is_alcoholic else ""
        print(f"  - {name}: €{price} {tag_str}")

    print("\n🍰 Desserts:")
    cursor.execute("SELECT name, cost FROM Dessert")
    for name, price in cursor.fetchall():
        print(f"  - {name}: €{price}")

    cursor.close()
    conn.close()

def getPizzaMenu():
    conn = connectDB()
    cursor = conn.cursor()

    query = """
    SELECT p.id, p.name,
        ROUND(SUM(i.cost) * 1.4 * 1.09+5,2) AS pizza_price,
        MIN(i.is_vegetarian) AS is_vegetarian,
        MIN(i.is_vegan) AS is_vegan
        FROM Pizza p
    JOIN PizzaIngredient pi ON p.id = pi.pizza_id
    JOIN Ingredient i ON pi.ingredient_id = i.id
    GROUP BY p.id, p.name;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows



