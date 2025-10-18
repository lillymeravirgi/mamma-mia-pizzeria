from decimal import Decimal
from methodsORM import (get_pizza_menu, get_drink_menu, get_dessert_menu, 
                        SessionLocal, get_customer_by_id, create_customer, 
                        add_order, find_deliverer, get_customer_by_name_birthdate, make_deliverer_available)
from flask import Flask, render_template, request, redirect, url_for, session
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
            # Existing customer login
            db_session = SessionLocal()
            customer = get_customer_by_id(db_session, int(customer_id))
            db_session.close()
            
            if customer:
                session['customer_id'] = customer.id
                session['customer_name'] = customer.name
                return redirect(url_for("menu"))
            else:
                return render_template("login.html", error="Customer ID not found")
    
    return render_template("login.html")

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
                return render_template("forgotID.html", 
                                     error="No customer found with this information",
                                     found=False)
    
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
        
        # Validate required fields
        if not all([name, gender, birthdate, address, postcode]):
            return render_template("signup.html", error="Please fill all required fields")
        
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
            
            # Redirect to a page showing their new customer ID
            return redirect(url_for("signup_success", customer_id=customer_id))
        except Exception as e:
            db_session.rollback()
            return render_template("signup.html", error=f"Error creating account: {str(e)}")
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
    # Check if user is logged in
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    pizzas = get_pizza_menu()
    drinks = get_drink_menu()
    desserts = get_dessert_menu()
    
    if request.method == "POST":
        order_items = []
        
        for item_type in ["pizza", "drink", "dessert"]:
            for key, qty in request.form.items():
                if key.startswith(item_type) and int(qty) > 0:
                    item_name = key.split("__")[1]
                    order_items.append((item_type, item_name, int(qty)))
        
        # Store order_items in session for processing
        session['order_items'] = order_items
        return redirect(url_for("confirmation"))
    
    return render_template("menu.html", 
                         pizzas=pizzas, 
                         desserts=desserts, 
                         drinks=drinks,
                         customer_name=session.get('customer_name'))

@app.route("/confirmation")
def confirmation():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    order_items = session.get('order_items', [])
    customer_id = session['customer_id']
    
    if not order_items:
        return redirect(url_for("menu"))
    
    db_session = SessionLocal()
    order_id = None  # Initialize order_id
    delivery_id = None  # Initialize delivery_id
    
    try:
        # Get customer postcode
        customer = get_customer_by_id(db_session, customer_id)
        
        # Find available deliverer for this postcode
        delivery_id = find_deliverer(db_session, customer.postcode)
        
        # Create the order
        order_id = add_order(db_session, customer_id, order_items, delivery_id)
        
        db_session.commit()
        
        # Schedule deliverer to become available again after 30 minutes
        if delivery_id:
            scheduler.add_job(
                make_deliverer_available,
                'date',
                run_date=datetime.now() + timedelta(minutes=30),
                args=[delivery_id]
            )
        
        # Clear order items from session
        session.pop('order_items', None)
        
        return render_template("confirmation.html",
                             order_id=order_id,
                             customer_id=customer_id,
                             customer_name=session.get('customer_name'),
                             delivery_assigned=delivery_id is not None)
    
    except Exception as e:
        db_session.rollback()
        # Return a proper error page instead of just showing the error
        return render_template("error.html", 
                             error=f"Error processing order: {str(e)}",
                             customer_name=session.get('customer_name'))
    finally:
        db_session.close()

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)