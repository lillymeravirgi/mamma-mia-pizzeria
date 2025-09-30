from sqlalchemy import func
from ORMMapping import Dessert, Drink, Ingredient, Order, Pizza, PizzaIngredient, SessionLocal 


def get_pizza_menu():
    session = SessionLocal()
    pizzas = (
        session.query(
            Pizza.id,
            Pizza.name,
            (func.round(func.sum(Ingredient.cost) * 1.4 * 1.09 + 5, 2)).label("pizza_price"),
            func.min(Ingredient.is_vegetarian).label("is_vegetarian"),
            func.min(Ingredient.is_vegan).label("is_vegan")
        )
        .join(PizzaIngredient, Pizza.id == PizzaIngredient.pizza_id)
        .join(Ingredient, PizzaIngredient.ingredient_id == Ingredient.id)
        .group_by(Pizza.id, Pizza.name)
        .all()
    )
    session.close()
    return pizzas

def get_drink_menu():
    session = SessionLocal()
    drinks = session.query(Drink).all()
    session.close()
    return drinks

def get_dessert_menu():
    session = SessionLocal()
    desserts = session.query(Dessert).all()
    session.close()
    return desserts

def add_order(order_items):
    session = SessionLocal()
    for name, qty in order_items:
        order = Order(item_name=name, quantity=qty)
        session.add(order)
    session.commit()
    session.close()

def print_menu():
    pizzas = get_pizza_menu()
    print("🍕 Pizzas:")
    for name, price, vegetarian, vegan in pizzas:
        tags = []
        if vegetarian:
            tags.append("🌱 Veggie")
        if vegan:
            tags.append("🥦 Vegan")
        print(f"- {name}: €{price:.2f} {' '.join(tags)}")

    print("\n🥤 Drinks:")
    for drink in get_drink_menu():
        tag = "🍷 Alcoholic" if drink.is_alcoholic else ""
        print(f"- {drink.name}: €{drink.cost:.2f} {tag}")

    print("\n🍰 Desserts:")
    for dessert in get_dessert_menu():
        print(f"- {dessert.name}: €{dessert.cost:.2f}")


