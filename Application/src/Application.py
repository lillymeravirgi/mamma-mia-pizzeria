
from methodsORM import get_pizza_menu, get_drink_menu, get_dessert_menu, add_order

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def menu():
    pizzas = get_pizza_menu()
    drinks = get_drink_menu()
    desserts = get_dessert_menu()

    if request.method == "POST":
        
        order_items = []

        for item_type in ["pizza", "drink", "dessert"]:
            for key, qty in request.form.items():
                if key.startswith(item_type) and int(qty) > 0:
                    item_name = key.split("__")[1]
                    order_items.append((item_name, int(qty)))

        #if order_items:
            #add_order(order_items)
            
            #  return redirect(url_for("userLogin"))

    return render_template("Menu.html", pizzas=pizzas, desserts=desserts,drinks=drinks)


@app.route("/userLogin/confirmation")
def confirmation():
    return "<h1>✅ Your order has been received!</h1>"
@app.route("/userLogin")
def login():
    return "<h1>Please login:</h1>"

if __name__ == "__main__":
    app.run(debug=True)
