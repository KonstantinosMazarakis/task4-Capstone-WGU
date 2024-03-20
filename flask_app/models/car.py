
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash



class Car:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.on_users = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars join users on cars.users_id = users.id;"
        results = connectToMySQL('exam_schema').query_db(query)
        cars = []
        for item in results:
            new_car = Car(item)

            user_data = {
                'id': item ['users.id'],
                'first_name': item ['first_name'],
                'last_name': item ['last_name'],
                'email': item ['email'],
                'password': item ['password'],
                "created_at" : item ["users.created_at"],
                "updated_at" : item ["users.updated_at"]
            }
            new_car.user = user.User(user_data)
            
            cars.append(new_car)
            
        return cars



    @classmethod
    def add_car(cls,data):
        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, users_id) VALUES ( %(price)s, %(model)s, %(make)s, %(year)s,  %(description)s, NOW(), NOW(), %(users_id)s );"
        return connectToMySQL('exam_schema').query_db( query, data )


    @classmethod
    def get_car(cls,data):
        query = "SELECT * FROM cars join users on cars.users_id = users.id WHERE cars.id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        car = Car(results[0])

        user_data = {
                'id': results[0] ['users.id'],
                'first_name': results[0] ['first_name'],
                'last_name': results[0] ['last_name'],
                'email': results[0] ['email'],
                'password': results[0] ['password'],
                "created_at" : results[0] ["users.created_at"],
                "updated_at" : results[0] ["users.updated_at"]
        }
        car.user = user.User(user_data)
        return car


    @classmethod
    def edit_car(cls,data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s  WHERE id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        return results


    @classmethod
    def search_by_make(cls, data):
        query = "SELECT * FROM cars join users on cars.users_id = users.id WHERE cars.make = %(make)s;"
        results = connectToMySQL('exam_schema').query_db(query, data)
        cars = []
        for item in results:
            new_car = Car(item)

            user_data = {
                'id': item ['users.id'],
                'first_name': item ['first_name'],
                'last_name': item ['last_name'],
                'email': item ['email'],
                'password': item ['password'],
                "created_at" : item ["users.created_at"],
                "updated_at" : item ["users.updated_at"]
            }
            new_car.user = user.User(user_data)
            
            cars.append(new_car)
            
        return cars

    @classmethod
    def search_by_model(cls, data):
        query = "SELECT * FROM cars join users on cars.users_id = users.id WHERE cars.model = %(model)s;"
        results = connectToMySQL('exam_schema').query_db(query, data)
        cars = []
        for item in results:
            new_car = Car(item)

            user_data = {
                'id': item ['users.id'],
                'first_name': item ['first_name'],
                'last_name': item ['last_name'],
                'email': item ['email'],
                'password': item ['password'],
                "created_at" : item ["users.created_at"],
                "updated_at" : item ["users.updated_at"]
            }
            new_car.user = user.User(user_data)
            
            cars.append(new_car)
            
        return cars

    @classmethod
    def delete_car(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        results = connectToMySQL('exam_schema').query_db(query,data)
        return results

    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car['price']) < 1:
            flash("please add a price.")
            is_valid = False
        elif int(car['price']) < 1:
            flash("Price has to be greater than 0.")
            is_valid = False
        if len(car['model']) < 1:
            flash("please add a model")
            is_valid = False
        if len(car['make']) < 1:
            flash("instructions must be at least 3 characters.")
            is_valid = False
        if len(car['year']) < 1:
            flash("please add a year.")
            is_valid = False
        elif int(car['year']) < 1:
            flash("year has to be greater than 0")
            is_valid = False
        if len(car['description']) < 1:
            flash("please add a description")
            is_valid = False
        return is_valid