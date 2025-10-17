from sqlalchemy import func, create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Dessert, Drink, Ingredient, Order, Pizza, OrderItem, PizzaIngredient
from decimal import Decimal


engine = create_engine("mysql+pymysql://root:HimPfSQL@localhost/pizza_ordering", echo=True)
SessionLocal = sessionmaker(bind=engine)





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
"""
def find_deliverer(customer_id: int):
    session: Session = SessionLocal()   
    try:
        Postcode = session.get(postcode, customer_id)
        DeliveryID = 
    finally:
        session.close()
"""


def add_order(session: Session, customer_id: int, order_items: list[tuple[str, str, int]], delivery_id: int | None = None) -> int:
    """
    Adds an order and its items.

    :param session: SQLAlchemy session
    :param customer_id: ID of the customer placing the order
    :param order_items: List of tuples (item_type, item_name, quantity)
                        item_type = 'pizza' | 'drink' | 'dessert'
    :param delivery_id: Optional delivery person ID
    :return: ID of the created order
    """


    new_order = Order(customer_id=customer_id, delivery_id=delivery_id)
    session.add(new_order)
    session.flush()  # to get new_order.id

    total = Decimal("0.00")

    # Step 2: Add order items
    for item_type, item_name, qty in order_items:
        if item_type == "pizza":
            product = session.query(Pizza).filter_by(name=item_name).first()
        elif item_type == "drink":
            product = session.query(Drink).filter_by(name=item_name).first()
        elif item_type == "dessert":
            product = session.query(Dessert).filter_by(name=item_name).first()
        else:
            continue  # skip unknown types

        if not product:
            print(f"⚠️ Item '{item_name}' not found in {item_type}")
            continue

        order_item = OrderItem(
            order_id=new_order.id,
            product_type=item_type,
            product_id=product.id,
            quantity=qty
        )
        session.add(order_item)

        # Add to total
        total += product.cost * qty

    # Step 3: Update total
    new_order.total = total

    # Step 4: Commit
    session.commit()
    return new_order.id



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


def get_customer_by_id(session: Session, customer_id: int):
    """Get customer by ID"""
    from models import Customer
    return session.query(Customer).filter_by(id=customer_id).first()

def create_customer(session: Session, name: str, gender: str, birthdate, 
                   address: str, postcode: str, city: str = None, country: str = None) -> int:
    """Create a new customer and return their ID"""
    from models import Customer
    
    new_customer = Customer(
        name=name,
        gender=gender,
        birthdate=birthdate,
        address=address,
        postcode=postcode,
        city=city,
        country=country
    )
    session.add(new_customer)
    session.flush()
    return new_customer.id