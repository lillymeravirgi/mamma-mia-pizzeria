from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy import func
from methodsORM import (get_all_orders, get_discount_info, get_pizza_menu, get_drink_menu, get_dessert_menu, 
                        SessionLocal, get_customer_by_id, create_customer, 
                        add_order, find_deliverer, get_customer_by_name_birthdate, 
                        make_deliverer_available, apply_discount_code, check_birthday_discount,
                        get_top_pizzas, get_undelivered_orders, get_earnings_by_demographics,
                        can_cancel_order, cancel_order_logic)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

app = Flask(__name__)
app.secret_key = 'pepper'

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        
        if customer_id:
            db_session = SessionLocal()
            customer = get_customer_by_id(db_session, int(customer_id))
            db_session.close()
            
            if customer:
                session['customer_id'] = customer.id
                session['customer_name'] = customer.name
                flash(f'Welcome back, {customer.name}!', 'success')
                return redirect(url_for("menu"))
            else:
                flash('Customer ID not found', 'error')
    
    return render_template("login.html")

@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        staff_code = request.form.get("staff_code")
        if staff_code == "2025":
            session['is_staff'] = True
            flash('Staff login successful!', 'success')
            return redirect(url_for("staff_dashboard"))
        else:
            flash('Invalid staff code', 'error')
            return render_template("staff_login.html", error="Invalid staff code")
    return render_template("staff_login.html")

@app.route("/staff_dashboard")
def staff_dashboard():
    if not session.get('is_staff'):
        flash('Staff access only', 'error')
        return redirect(url_for("login"))
    
    db_session = SessionLocal()
    
    top_pizzas = get_top_pizzas(db_session, limit=3, days=30)
    undelivered = get_undelivered_orders(db_session)
    earnings = get_earnings_by_demographics(db_session)
    
    db_session.close()
    
    return render_template("staff_dashboard.html",
                         top_pizzas=top_pizzas,
                         undelivered=undelivered,
                         earnings=earnings)

@app.route("/forgotID", methods=["GET", "POST"])
def forgot_id():
    if request.method == "POST":
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")
        
        if name and birthdate:
            db_session = SessionLocal()
            customer = get_customer_by_name_birthdate(
                db_session, 
                name, 
                datetime.strptime(birthdate, '%Y-%m-%d').date()
            )
            db_session.close()
            
            if customer:
                return render_template("forgotID.html", 
                                     customer_id=customer.id,
                                     customer_name=customer.name,
                                     found=True)
            else:
                flash('No customer found with this information', 'error')
    
    return render_template("forgotID.html", found=False)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")
        address = request.form.get("address")
        postcode = request.form.get("postcode")
        city = request.form.get("city")
        country = request.form.get("country")
        
        if not all([name, gender, birthdate, address, postcode]):
            flash('Please fill all required fields', 'error')
            return render_template("signup.html")
        
        db_session = SessionLocal()
        try:
            customer_id = create_customer(
                db_session, 
                name=name,
                gender=gender,
                birthdate=datetime.strptime(birthdate, '%Y-%m-%d').date(),
                address=address,
                postcode=postcode,
                city=city,
                country=country
            )
            db_session.commit()
            
            return redirect(url_for("signup_success", customer_id=customer_id))
        except Exception as e:
            db_session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            return render_template("signup.html")
        finally:
            db_session.close()
    
    return render_template("signup.html")

@app.route("/signup_success/<int:customer_id>")
def signup_success(customer_id):
    db_session = SessionLocal()
    customer = get_customer_by_id(db_session, customer_id)
    db_session.close()
    
    if customer:
        return render_template("signup_success.html", 
                             customer_id=customer_id,
                             customer_name=customer.name)
    else:
        return redirect(url_for("signup"))

@app.route("/menu", methods=["GET", "POST"])
def menu():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    db_session = SessionLocal()
    customer = get_customer_by_id(db_session, session['customer_id'])
    
    pizzas = get_pizza_menu()
    drinks = get_drink_menu()
    desserts = get_dessert_menu()
    
    birthday_info = check_birthday_discount(db_session, session['customer_id'])
    
    loyalty_eligible = customer.pizzas_ordered_count >= 10
    
    db_session.close()
    
    if request.method == "POST":
        order_items = []
        
        for item_type in ["pizza", "drink", "dessert"]:
            for key, qty in request.form.items():
                if key.startswith(item_type) and int(qty) > 0:
                    item_name = key.split("__")[1]
                    order_items.append((item_type, item_name, int(qty)))
        
        discount_code = request.form.get("discount_code", "").strip()
        
        session['order_items'] = order_items
        session['discount_code'] = discount_code if discount_code else None
        session['apply_birthday'] = birthday_info['is_birthday']
        
        return redirect(url_for("confirmation"))
    
    return render_template("menu.html", 
                         pizzas=pizzas, 
                         desserts=desserts, 
                         drinks=drinks,
                         customer_name=session.get('customer_name'),
                         customer=customer,
                         birthday_info=birthday_info,
                         loyalty_eligible=loyalty_eligible)

@app.route("/confirmation")
def confirmation():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    order_items = session.get('order_items', [])
    customer_id = session['customer_id']
    discount_code = session.get('discount_code')
    apply_birthday = session.get('apply_birthday', False)
    
    if not order_items:
        flash('No items in cart', 'error')
        return redirect(url_for("menu"))
    
    db_session = SessionLocal()
    order_id = None
    delivery_id = None
    discount_applied = False
    birthday_applied = False
    loyalty_applied = False
    
    try:
        # Get customer info
        customer = get_customer_by_id(db_session, customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Find available deliverer for customer's postcode
        delivery_id = find_deliverer(db_session, customer.postcode)
        
        # Create the order
        order_result = add_order(
            db_session, 
            customer_id, 
            order_items, 
            delivery_id,
            apply_birthday=apply_birthday
        )
        
        order_id = order_result['order_id']
        birthday_applied = order_result.get('birthday_applied', False)
        loyalty_applied = order_result.get('loyalty_applied', False)
        
        # Apply discount code if provided (BEFORE commit)
        if discount_code:
            discount_applied = apply_discount_code(
                db_session, 
                order_id, 
                discount_code, 
                customer_id
            )
            if discount_applied:
                flash(f'Discount code "{discount_code}" applied successfully! 🎉', 'success')
            else:
                flash(f'Could not apply discount code "{discount_code}"', 'warning')
        
        # Commit everything
        db_session.commit()
        
        # Schedule deliverer to become available again (AFTER commit)
        if delivery_id:
            scheduler.add_job(
                make_deliverer_available,
                'date',
                run_date=datetime.now() + timedelta(minutes=30),
                args=[delivery_id],
                id=f'deliverer_{delivery_id}_{order_id}',
                replace_existing=True
            )
        
        # Clear session data
        session.pop('order_items', None)
        session.pop('discount_code', None)
        session.pop('apply_birthday', None)
        
        # Get final order details (with updated total if discount applied)
        from models import Order
        order = db_session.query(Order).get(order_id)
        
        return render_template("confirmation.html",
                             order_id=order_id,
                             order_total=order.total,
                             customer_id=customer_id,
                             customer_name=session.get('customer_name'),
                             delivery_assigned=delivery_id is not None,
                             discount_applied=discount_applied,
                             birthday_applied=birthday_applied,
                             loyalty_applied=loyalty_applied)
    
    except Exception as e:
        db_session.rollback()
        print(f"❌ Error processing order: {e}")
        flash(f'Error processing order: {str(e)}', 'error')
        return redirect(url_for("menu"))
    finally:
        db_session.close()

@app.route("/validate_discount", methods=["POST"])
def validate_discount():
    """AJAX endpoint to validate discount code before order submission"""
    if 'customer_id' not in session:
        return {'valid': False, 'message': 'Not logged in'}, 401
    
    code = request.json.get('code', '').strip()
    
    if not code:
        return {'valid': False, 'message': 'Please enter a discount code'}
    
    db_session = SessionLocal()
    try:
        info = get_discount_info(db_session, code)
        
        # Check if customer already used this code
        from models import DiscountCode, OrderDiscount, Order
        discount = db_session.query(DiscountCode).filter(
            DiscountCode.code == code.upper()
        ).first()
        
        if discount and info['valid']:
            already_used = db_session.query(OrderDiscount).join(Order).filter(
                OrderDiscount.discount_id == discount.id,
                Order.customer_id == session['customer_id']
            ).first()
            
            if already_used:
                return {'valid': False, 'message': 'You have already used this discount code'}
        
        return info
    finally:
        db_session.close()

@app.route("/my_orders")
def my_orders():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    db_session = SessionLocal()
    from models import Order
    
    orders = db_session.query(Order).filter(
        Order.customer_id == session['customer_id']
    ).order_by(Order.order_time.desc()).all()
    
    orders_with_cancel = []
    for order in orders:
        can_cancel = can_cancel_order(order)
        orders_with_cancel.append({
            'order': order,
            'can_cancel': can_cancel
        })
    
    db_session.close()
    
    return render_template("my_orders.html", 
                         orders=orders_with_cancel,
                         customer_name=session.get('customer_name'))

@app.route("/cancel_order/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    db_session = SessionLocal()
    
    try:
        result = cancel_order_logic(db_session, order_id, session['customer_id'])
        
        if result['success']:
            db_session.commit()
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    
    except Exception as e:
        db_session.rollback()
        flash(f'Error cancelling order: {str(e)}', 'error')
    finally:
        db_session.close()
    
    return redirect(url_for("my_orders"))

@app.route("/customer_profile")
def customer_profile():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    db_session = SessionLocal()
    customer = get_customer_by_id(db_session, session['customer_id'])
    
    birthday_info = check_birthday_discount(db_session, session['customer_id'])
    
  
    total_orders = get_all_orders(session['customer_id'])

    db_session.close()
    
    return render_template("customer_profile.html",
                         customer=customer,
                         birthday_info=birthday_info,
                         total_orders=total_orders)

@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for("login"))

@app.route("/staff_logout")
def staff_logout():
    session.pop('is_staff', None)
    flash('Staff logged out', 'success')
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)