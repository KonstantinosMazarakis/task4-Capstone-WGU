from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.car import Car



@app.route("/cars/<int:id>/edit")
def car_edit(id):
    car = Car.get_car({'id':id})
    return render_template("cars_edit.html", car = car)




@app.route("/cars/edit_post", methods=['POST'])
def cars_edit_post():
    data = request.form
    if not Car.validate_car(data):
        return redirect(f"/cars/{data['id']}/edit")

    Car.edit_car(data)
    return redirect ("/dashboard")