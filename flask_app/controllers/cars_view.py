from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models import user

@app.route("/cars/<int:id>")
def cars_view(id):
    car = Car.get_car({'id':id})
    return render_template("cars_view.html", car = car)

@app.route("/cars/purchase/post", methods=['POST'])
def cars_purchase_post():
    data = request.form
    user.User.add_purchases(data)
    return redirect("/dashboard")
    
