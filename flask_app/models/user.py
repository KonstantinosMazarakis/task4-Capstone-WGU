import imp
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import car
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z]).{8,45}$')
FIRST_LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]{3,45}$')


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.on_cars = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s ,NOW() , NOW())"
        results = connectToMySQL('exam_schema').query_db( query, data )
        return results

    @classmethod
    def login(cls,data):
        query = "SELECT * from users WHERE email = %(email)s"
        results = connectToMySQL('exam_schema').query_db( query, data )
        if len(results) < 1:
            return False
        return User(results[0])


    @classmethod
    def add_purchases(cls,data):
        query = "INSERT INTO purchases (user_id, car_id) VALUES (%(user_id)s, %(car_id)s);"
        return connectToMySQL('exam_schema').query_db( query, data )


    @classmethod
    def all_sold_cars(cls):
        query = "SELECT * FROM purchases"
        result = connectToMySQL('exam_schema').query_db( query)
        car_ids = []
        for row in result:
            car_ids.append(row['car_id'])
        return car_ids

    @classmethod
    def all_purchased_cars(cls):
        query = "SELECT * FROM purchases"
        result = connectToMySQL('exam_schema').query_db( query)
        return result

    @classmethod
    def user_purchases_cars(cls,data):
        query = "SELECT * FROM users left join purchases ON purchases.user_id = users.id left join cars ON purchases.car_id = cars.id WHERE users.id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db( query, data )
        user = User(results[0])
        for row_from_db in results:
            car_data = {
            "id" : row_from_db["cars.id"],
            "price" : row_from_db["price"],
            "model" : row_from_db["model"],
            "make" : row_from_db["make"],
            "year" : row_from_db["year"],
            "description" : row_from_db["description"],
            "users_id" : row_from_db["users_id"],
            "created_at" : row_from_db["cars.created_at"],
            "updated_at" : row_from_db["cars.updated_at"]
            }
            user.on_cars.append(car.Car(car_data))
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not FIRST_LAST_NAME_REGEX.match(user['first_name']):
            flash("First name must be at least 3 characters and only letters.", 'create_user')
            is_valid = False
        if not FIRST_LAST_NAME_REGEX.match(user['last_name']):
            flash("Last name must be at least 3 characters and only letters.", 'create_user')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'create_user')
            is_valid = False
        if User.login(user) != False:
            flash("Email address already exist!", 'create_user')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Passwords must have a least 1 number and 1 uppercase letter and minimum of 8 digits length", 'create_user')
            print(f"Validating password: '{user['password']}'")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password and Confirm Password has to be the same", 'create_user')
            is_valid = False
        return is_valid