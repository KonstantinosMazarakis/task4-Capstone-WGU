from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.car import Car


@app.route("/cars/new")
def cars_new():
    return render_template("cars_new.html")


@app.route("/cars/new_post", methods=['POST'])
def cars_new_post():
    if not Car.validate_car(request.form):
        return redirect("/cars/new")
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
                'users_id': session['id']
        }

    Car.add_car(data)
    return redirect("/dashboard")
