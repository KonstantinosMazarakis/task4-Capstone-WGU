from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login_and_registration.html")


@app.route("/new_user", methods=['POST'])
def new_user():
    if not User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash,
    }
    user_id = User.create_user(data)
    session['id'] = user_id
    session['user_first_name'] = data["first_name"]
    session['loged_in'] = True
    return redirect ("/dashboard")


@app.route("/login", methods=['POST'])
def login():
    data = request.form
    results = User.login(data)
    if not results:
        flash("Invalid Email/Password!",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(results.password, request.form['password']):
        flash("Invalid Email/Password!", 'login')
        return redirect('/')
    session['id'] = results.id
    session['user_first_name'] = results.first_name
    session['loged_in'] = True
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if not "loged_in" in session:
        return redirect("/")
    
    cars = Car.get_all()
    sold_cars = User.all_sold_cars()
    return render_template("dashboard.html",cars = cars, sold_cars = sold_cars)

@app.route("/clear_session", methods=["POST"])
def clear_session():
    session.clear()
    return redirect("/")


@app.route("/cars/<int:id>/delete")
def delete(id):
    Car.delete_car({'id':id})
    return redirect("/dashboard")


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    search_type = request.args.get('type')

    if not search_query:
        print("Search bar is empty")
        cars = Car.get_all()
    elif search_type == 'make':
        print("Searching by make")
        data = {"make": search_query}
        cars = Car.search_by_make(data)
    elif search_type == 'model':
        print("Searching by model")
        data = {"model": search_query}
        cars = Car.search_by_model(data)
    else: 
        print("Getting all cars")
        cars = Car.get_all()
    
    sold_cars = User.all_sold_cars()
    return render_template("dashboard.html", cars=cars, sold_cars=sold_cars)