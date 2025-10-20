from sqlalchemy import func, create_engine, Date
from sqlalchemy.orm import Session, sessionmaker
from models import DeliveryPerson, Dessert, Drink, Ingredient, Order, Pizza, OrderItem, PizzaIngredient, Customer
from decimal import Decimal
from datetime import datetime


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

def find_deliverer(session: Session, customer_postcode: str):
    """Find an available deliverer for the given postcode"""
    deliverer = (
        session.query(DeliveryPerson)
        .filter(
            DeliveryPerson.postcode == customer_postcode,
            DeliveryPerson.available == True 
        )
        .first() 
    )
    
    return deliverer.id if deliverer else None


def get_customer_by_name_birthdate(session: Session, name: str, date: Date):
    """Get customer by name and birthdate"""
    customer = session.query(Customer).filter(
        Customer.name == name,
        Customer.birthdate == date
    ).first()
    
    return customer


def add_order(session, customer_id: int, order_items: list[tuple], delivery_id: int | None):
    """
    Create a new order and its order items in the database.
    
    Args:
        session: SQLAlchemy session
        customer_id: ID of the customer placing the order
        order_items: list of tuples like (product_type, product_name, quantity)
        delivery_id: ID of assigned DeliveryPerson or None
    
    Returns:
        int: ID of the newly created order
    """
    try:
        # 1️⃣ Calculate total
        total_price = Decimal("0.00")
        for product_type, product_name, qty in order_items:
            if product_type == "pizza":
                pizza = session.query(Pizza).filter(Pizza.name == product_name).first()
                if pizza:
                    pizza_price = get_price_for_Pizza(pizza.id, session)
                    total_price += pizza_price * qty
            elif product_type == "drink":
                drink = session.query(Drink).filter(Drink.name == product_name).first()
                if drink:
                    total_price += drink.cost * qty
            elif product_type == "dessert":
                dessert = session.query(Dessert).filter(Dessert.name == product_name).first()
                if dessert:
                    total_price += dessert.cost * qty
            else:
                raise ValueError(f"Unknown product type: {product_type}")
        
        # 2️⃣ Create the Order record
        new_order = Order(
            customer_id=customer_id,
            delivery_id=delivery_id,
            total=total_price,
            status="pending",
            order_time=datetime.now()
        )
        session.add(new_order)
        session.flush()  # Ensures order.id is generated

        # 3️⃣ Add each order item
        for product_type, product_name, qty in order_items:
            product_id = get_product_id_by_name(product_type, product_name, session)
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_type=product_type,
                product_id=product_id,
                quantity=qty
            )
            session.add(order_item)

        # 4️⃣ Update delivery person availability
        if delivery_id is not None:
            deliverer = session.query(DeliveryPerson).get(delivery_id)
            if deliverer:
                deliverer.available = 0  # mark unavailable

        session.commit()
        return new_order.id

    except Exception as e:
        session.rollback()
        print(f"Error creating order: {e}")
        raise


def get_product_id_by_name(product_type: str, product_name: str, session: Session):
    """Get product ID by name and type"""
    if product_type == "pizza":
        product = session.query(Pizza).filter(Pizza.name == product_name).first()
    elif product_type == "drink":
        product = session.query(Drink).filter(Drink.name == product_name).first()
    elif product_type == "dessert":
        product = session.query(Dessert).filter(Dessert.name == product_name).first()
    else:
        raise ValueError(f"Unknown product type: {product_type}")
    
    if product:
        return product.id
    else:
        raise ValueError(f"{product_type} '{product_name}' not found in database")



def make_deliverer_available(delivery_id: int):
    """Marks a deliverer available again (used by APScheduler)."""
    db_session = SessionLocal()
    try:
        deliverer = db_session.get(DeliveryPerson, delivery_id)
        if deliverer:
            deliverer.available = 1
            db_session.commit()
            print(f"Deliverer #{delivery_id} is now available again.")
    except Exception as e:
        db_session.rollback()
        print(f"Error making deliverer available: {e}")
    finally:
        db_session.close()

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


    
            

def get_price_for_Pizza(pizza_id: int, session: Session):
    """Calculate pizza price based on ingredients"""
    ingredient_ids = (
        session.query(PizzaIngredient.ingredient_id)
        .filter(PizzaIngredient.pizza_id == pizza_id)
        .all()
    )

    # `.all()` returns a list of tuples like [(1,), (2,), (3,)]
    ingredient_ids = [id_tuple[0] for id_tuple in ingredient_ids]

    if not ingredient_ids:
        return Decimal("0.00")

    # Calculate total ingredient cost
    total_cost = (
        session.query(func.sum(Ingredient.cost))
        .filter(Ingredient.id.in_(ingredient_ids))
        .scalar()
    )
    if total_cost:
        price = (Decimal(str(total_cost)) * Decimal("1.4") * Decimal("1.09")) + Decimal("5")
        return price.quantize(Decimal("0.01"))
    
    return Decimal("0.00")




def get_customer_by_id(session: Session, customer_id: int):
    
   
    return session.query(Customer).filter_by(id=customer_id).first()

def create_customer(session: Session, name: str, gender: str, birthdate, 
                   address: str, postcode: str, city: str = None, country: str = None) -> int:
    """Create a new customer and return their ID"""
  
    
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