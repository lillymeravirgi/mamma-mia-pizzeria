from sqlalchemy import func, create_engine, Date
from sqlalchemy.orm import Session, sessionmaker
from models import (DeliveryPerson, Dessert, Drink, Ingredient, Order, Pizza, 
                    OrderItem, PizzaIngredient, Customer, DiscountCode, OrderDiscount)
from decimal import Decimal
from datetime import datetime, timedelta 

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
    try:
       
        customer =  session.query(Customer).filter(
            Customer.name == name,
            Customer.birthdate == date
            ).first()
        
        return customer
    finally:
        session.close()

def add_order(session, customer_id: int, order_items: list[tuple], delivery_id: int | None, apply_birthday: bool = False):
    """
    Create a new order with items, apply loyalty & birthday discounts, and return details.
    """
    try:
        customer = session.query(Customer).get(customer_id)
        birthday_applied = False
        loyalty_applied = False
        
        # 1️⃣ Calculate base total (paid items only)
        total_price = Decimal("0.00")
        pizza_count = 0
        
        for product_type, product_name, qty in order_items:
            if product_type == "pizza":
                pizza = session.query(Pizza).filter(Pizza.name == product_name).first()
                if pizza:
                    pizza_price = get_price_for_Pizza(pizza.id, session)
                    total_price += pizza_price * qty
                    pizza_count += qty
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
        
        # 2️⃣ Apply birthday discount (free items - NO cost added)
        if apply_birthday:
            birthday_applied = True
            
            # Add cheapest pizza (FREE)
            cheapest_pizza = (
                session.query(Pizza.id, Pizza.name)
                .join(PizzaIngredient)
                .join(Ingredient)
                .group_by(Pizza.id, Pizza.name)
                .order_by(func.sum(Ingredient.cost))
                .first()
            )
            if cheapest_pizza:
                order_items.append(("pizza", cheapest_pizza.name, 1))
            
            # Add cheapest drink (FREE)
            cheapest_drink = session.query(Drink.id, Drink.name).order_by(Drink.cost).first()
            if cheapest_drink:
                order_items.append(("drink", cheapest_drink.name, 1))
        
        # Update customer pizza count and check loyalty discount
        customer.pizzas_ordered_count += pizza_count
        
        if customer.pizzas_ordered_count >= 10:
            total_price *= Decimal("0.90")  # 10% discount
            customer.pizzas_ordered_count = 0  # Reset counter
            loyalty_applied = True
        


        # Round final total
        total_price = total_price.quantize(Decimal("0.01"))
        
        #Create the Order record
        new_order = Order(
            customer_id=customer_id,
            delivery_id=delivery_id,
            total=total_price,
            status="pending",
            order_time=datetime.now()
        )
        session.add(new_order)
        session.flush()

        # 6️⃣ Add all order items (including free birthday items)
        for product_type, product_name, qty in order_items:
            product_id = get_product_id_by_name(product_type, product_name, session)
            order_item = OrderItem(
                order_id=new_order.id,
                product_type=product_type,
                product_id=product_id,
                quantity=qty
            )
            session.add(order_item)

        # 7️⃣ Update delivery person availability
        if delivery_id is not None:
            deliverer = session.query(DeliveryPerson).get(delivery_id)
            if deliverer:
                deliverer.available = 0

        session.commit()
        return {
            'order_id': new_order.id,
            'birthday_applied': birthday_applied,
            'loyalty_applied': loyalty_applied
        }

    except Exception as e:
        session.rollback()
        print(f"Order failed, rolled back: {e}")
        raise


def apply_discount_code(session: Session, order_id: int, code: str, customer_id: int) -> bool:
    """
    Apply discount code if valid and not already used by this customer.
    Returns True if discount was applied successfully.
    """
    
    # Find the discount code
    discount = session.query(DiscountCode).filter(
        DiscountCode.code == code.upper(),  # Case-insensitive comparison
        DiscountCode.is_valid == True
    ).first()
    
    if not discount:
        print(f"!!! Discount code '{code}' not found or invalid")
        return False
    
    # Check if customer already used this discount code
    already_used = session.query(OrderDiscount).join(Order).filter(
        OrderDiscount.discount_id == discount.id,
        Order.customer_id == customer_id
    ).first()
    
    if already_used:
        print(f"!!! Customer {customer_id} already used discount code '{code}'")
        return False
    
    # Check if discount code has expired
    if discount.expiry_date and discount.expiry_date < datetime.now().date():
        print(f"!!!Discount code '{code}' expired on {discount.expiry_date}")
        return False
    
    # Get the order
    order = session.query(Order).get(order_id)
    if not order:
        print(f"!!! Order {order_id} not found")
        return False
    
    # Store original total for logging
    original_total = order.total
    
    # Apply 10% discount to order total
    order.total = (order.total * Decimal("0.90")).quantize(Decimal("0.01"))
    
    # Link discount to order
    order_discount = OrderDiscount(
        order_id=order_id,
        discount_id=discount.id
    )
    session.add(order_discount)
    
    print(f"✅ Applied discount code '{code}': €{original_total} → €{order.total}")
    return True



def check_birthday_discount(session: Session, customer_id: int) -> dict:
    """
    Check if today is customer's birthday and return info about free items.
    """
    customer = session.query(Customer).get(customer_id)
    if not customer:
        return {'is_birthday': False}
    
    today = datetime.now().date()
    
    # Check if today matches birthday (month and day)
    if (customer.birthdate.month == today.month and 
        customer.birthdate.day == today.day):
        
        # Get cheapest pizza
        cheapest_pizza = (
            session.query(Pizza)
            .join(PizzaIngredient)
            .join(Ingredient)
            .group_by(Pizza.id, Pizza.name)
            .order_by(func.sum(Ingredient.cost))
            .first()
        )
        
        # Get cheapest drink
        cheapest_drink = (
            session.query(Drink)
            .order_by(Drink.cost)
            .first()
        )
        
        return {
            'is_birthday': True,
            'free_pizza': cheapest_pizza,
            'free_drink': cheapest_drink
        }
    
    return {'is_birthday': False}

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

def get_top_pizzas(session, limit=3, days=30):
    """Return top pizzas in last X days"""
    from models import OrderItem, Order, Pizza
    cutoff = datetime.now() - timedelta(days=days)
    result = (
        session.query(Pizza.name, func.sum(OrderItem.quantity).label("total_sold"))
        .join(OrderItem, Pizza.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(OrderItem.product_type == "pizza", Order.order_time >= cutoff)
        .group_by(Pizza.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return result

def get_undelivered_orders(session):
    """Return orders not yet delivered"""
    from models import Order
    return session.query(Order).filter(Order.status != "delivered").all()

def get_earnings_by_demographics(session):
    """Return total earnings grouped by gender"""
    return (
        session.query(Customer.gender, func.sum(Order.total))
        .join(Order, Customer.id == Order.customer_id)
        .group_by(Customer.gender)
        .all()
    )

def can_cancel_order(order):
    """
    Returns True if the order can still be cancelled.
    For example: only if order status is 'pending' or 'in preparation'.
    """
    return order.status in ['pending', 'in preparation']

def cancel_order_logic(session, order_id: int, customer_id: int):
    """
    Cancels an order if allowed and returns a result dict.
    """
    from models import Order, DeliveryPerson

    order = session.query(Order).filter_by(id=order_id, customer_id=customer_id).first()
    if not order:
        return {'success': False, 'message': 'Order not found'}

    if not can_cancel_order(order):
        return {'success': False, 'message': 'Cannot cancel this order anymore'}

    order.status = 'cancelled'

    if order.delivery_id:
        deliverer = session.query(DeliveryPerson).get(order.delivery_id)
        if deliverer:
            deliverer.available = 1

    return {'success': True, 'message': f'Order #{order_id} cancelled successfully'}

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

def get_discount_info(session: Session, code: str) -> dict:
    """
    Get information about a discount code without applying it.
    Useful for validation before order creation.
    """
    from models import DiscountCode
    
    discount = session.query(DiscountCode).filter(
        DiscountCode.code == code.upper(),
        DiscountCode.is_valid == True
    ).first()
    
    if not discount:
        return {'valid': False, 'message': 'Invalid discount code'}
    
    if discount.expiry_date and discount.expiry_date < datetime.now().date():
        return {'valid': False, 'message': 'Discount code has expired'}
    
    return {
        'valid': True,
        'code': discount.code,
        'expiry_date': discount.expiry_date,
        'message': '10% discount will be applied'
    }

