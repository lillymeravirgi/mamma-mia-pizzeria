import mysql.connector

def connectDB():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="HimPfSQL",
    database="pizza_ordering"
)

def getMenu(): 
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pizzamenu")
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM Drink")
    rows += cursor.fetchall()
    cursor.execute("SELECT * FROM Dessert")
    rows += cursor.fetchall()
    conn.close()
    return rows

def printMenu():
    conn = connectDB()
    cursor = conn.cursor()

    print("🍕 Pizzas:")
    pizzas = getPizzaInfo()
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

def getPizzaInfo():
    conn = connectDB()
    cursor = conn.cursor()

    query = """
    SELECT p.name,
       ROUND(SUM(i.cost) * 1.4 * 1.02, 2) AS pizza_price,
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

