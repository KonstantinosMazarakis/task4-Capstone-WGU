import imp
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User




@app.route("/cars/purchases/<int:id>")
def cars_purchases(id):
    user_perchases = User.user_purchases_cars({'id':id})
    return render_template("purchases.html", user_perchases = user_perchases)
