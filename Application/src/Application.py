from decimal import Decimal
from methodsORM import get_pizza_menu, get_drink_menu, get_dessert_menu, SessionLocal, get_customer_by_id, create_customer
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime


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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")  # format: YYYY-MM-DD
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
            
            session['customer_id'] = customer_id
            session['customer_name'] = name
            return redirect(url_for("menu"))
        except Exception as e:
            db_session.rollback()
            return render_template("signup.html", error=f"Error creating account: {str(e)}")
        finally:
            db_session.close()
    
    return render_template("signup.html")

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
    
    return render_template("Menu.html", 
                         pizzas=pizzas, 
                         desserts=desserts, 
                         drinks=drinks,
                         customer_name=session.get('customer_name'))

@app.route("/confirmation")
def confirmation():
    if 'customer_id' not in session:
        return redirect(url_for("login"))
    
    # Missing: order processing
    order_items = session.get('order_items', [])
    customer_id = session['customer_id']
    # add_order()
    
    return "<h1>Your order has been received!</h1>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)