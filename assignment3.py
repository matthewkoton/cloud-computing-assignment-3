from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import json

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

class dish():  
    def api_call(self, query):
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        query = query
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'JTNwmSBjEi97fQhVG0cWuQ==FgDuQk8zsrFueEyU'})
        if (response.text == "[]"):
            return response.json() , 422, -3
        elif (response.status_code == requests.codes.ok):
            return response.json(), 200, 0  # third value is irrelavent for now
        else:
            print("Error:", response.status_code, response.text)
            return response.json() , 504, -4 

    def __init__(self, query, id_num):
        self.dish_json = {
                "name" : query,
                "ID" : id_num,
                "cal" : 0,
                "size" : 0,
                "sodium" : 0,
                "sugar" : 0
                }

        response_json, code, value = self.api_call(query)
        
        for i in range(len(response_json)):
            self.dish_json["cal"] += response_json[0]["calories"]
            self.dish_json["size"] += response_json[0]["serving_size_g"]
            self.dish_json["sodium"] += response_json[0]["sodium_mg"]
            self.dish_json["sugar"] += response_json[0]["sugar_g"]

class dishes_collection():
    def __init__(self):
        self.id_num = 1
        self.dishes = dict()

    def insert_dish(self, dish_name):

        for key in self.dishes.keys():
            if dish_name ==  self.dishes[key].dish_json["name"]:
                print("dish already exists")
                return -2, 422

        new_dish = dish(dish_name, self.id_num)
        response, code, value = new_dish.api_call(dish_name)
        if code == 422:
            return -3, 422
        else:
            self.dishes[self.id_num] = new_dish
            self.id_num += 1
            return self.id_num - 1, 201
    
    def get_dish_by_id(self, id_to_get):
        if id_to_get not in self.dishes.keys():
            return -5, 404
        else:
            return self.dishes[id_to_get].dish_json, 200
        
    def get_dish_by_name(self, name_to_get):
        for key in self.dishes.keys():
            if self.dishes[key].dish_json["name"] == name_to_get:
                return self.dishes[key].dish_json, 200
        return -5, 404
        

    def delete_dish_by_id(self, id_to_delete, meals):

        if int(id_to_delete) not in self.dishes.keys():
            return -5,404
        else:
            for meal in meals.meals.keys():
                pass
                if meals.meals[meal]["appetizer"] == int(id_to_delete):
                    meals.meals[meal]["appetizer"] = None    
                if meals.meals[meal]["main"] == int(id_to_delete):
                    meals.meals[meal]["main"] = None
                if meals.meals[meal]["dessert"] == int(id_to_delete):
                    meals.meals[meal]["dessert"] = None
            
            del self.dishes[int(id_to_delete)]
            return id_to_delete, 200
        
    def delete_dish_by_name(self, name_to_delete, meals):
        id = -1
        for key in self.dishes.keys():
            if self.dishes[key].dish_json["name"] == name_to_delete:
                id = key
                break
        if id == -1:
            return -5,404
        else:
            for meal in meals.meals.keys():
                pass
                if meals.meals[meal]["appetizer"] == id:
                    meals.meals[meal]["appetizer"] = None    
                if meals.meals[meal]["main"] == id:
                    meals.meals[meal]["main"] = None
                if meals.meals[meal]["dessert"] == id:
                    meals.meals[meal]["dessert"] = None
            
            del self.dishes[id]
            return id, 200
        
class meals_collection():
    def __init__(self, dishes):
        self.id_num = 1
        self.meals = {}
        self.dishes = dishes

    def add_meal(self, meal_name, starter_ID, main_ID, dessert_ID):
        dishes_IDs = self.dishes.dishes.keys()
        if not ((starter_ID in dishes_IDs) and (main_ID in dishes_IDs) and (dessert_ID in dishes_IDs)):
            return -6, 422
        
        for meal_id, existing_meal in self.meals.items():
            if existing_meal["name"] == meal_name:
                return -2, 422
     
        cal = sum([dishes_col.dishes[starter_ID].dish_json["cal"] ,dishes_col.dishes[main_ID].dish_json["cal"], dishes_col.dishes[dessert_ID].dish_json["cal"]])
        sodium = sum([dishes_col.dishes[starter_ID].dish_json["sodium"] ,dishes_col.dishes[main_ID].dish_json["sodium"], dishes_col.dishes[dessert_ID].dish_json["sodium"]])
        sugar = sum([dishes_col.dishes[starter_ID].dish_json["sugar"] ,dishes_col.dishes[main_ID].dish_json["sugar"], dishes_col.dishes[dessert_ID].dish_json["sugar"]])
        self.meals[self.id_num] = {"name" : meal_name,
                        "ID": self.id_num,
                        "appetizer" : starter_ID,
                        "main" : main_ID,
                        "dessert" : dessert_ID, 
                        "cal" : cal ,
                        "sodium" : sodium,
                        "sugar" : sugar
                        }
        self.id_num += 1
        return self.id_num-1, 201

    def get_meal_by_id(self, meal_id):
        if meal_id in self.meals.keys():
            return self.meals[meal_id], 200
        else:
            return -5, 404
        
    def get_meal_by_name(self, meal_name):
        for key in self.meals.keys():
            if self.meals[key]["name"] == meal_name:
                return self.meals[key], 200
        return -5, 404
    
    def delete_meal_by_id(self, meal_id):
        if meal_id in self.meals.keys():
            del self.meals[meal_id]
            return meal_id, 200
        return -5,404
    
    def delete_meal_by_name(self, name_to_delete):
        id = -1
        for key in self.meals.keys():
            if self.meals[key]["name"] == name_to_delete:
                id = key
                break
        if id == -1:
            return -5,404
        else:
            del self.meals[id]
            return id, 200
        
    def put_update(self, meal_name, starter_ID, main_ID, dessert_ID, meal_id):
        dishes_IDs = self.dishes.dishes.keys()
        if (not ((starter_ID in dishes_IDs) and (main_ID in dishes_IDs) and (dessert_ID in dishes_IDs)) or ((meal_id not in self.meals.keys()))):
            return -5, 422
        else:
            #self.meals[meal_id] = {"name" : meal_name,            
            #                "appetizer" : starter_ID,
            #                "main" : main_ID,
            #                "dessert" : dessert_ID
            #                }
            #return meal_id, 200
            cal = sum([dishes_col.dishes[starter_ID].dish_json["cal"] ,dishes_col.dishes[main_ID].dish_json["cal"], dishes_col.dishes[dessert_ID].dish_json["cal"]])
            sodium = sum([dishes_col.dishes[starter_ID].dish_json["sodium"] ,dishes_col.dishes[main_ID].dish_json["sodium"], dishes_col.dishes[dessert_ID].dish_json["sodium"]])
            sugar = sum([dishes_col.dishes[starter_ID].dish_json["sugar"] ,dishes_col.dishes[main_ID].dish_json["sugar"], dishes_col.dishes[dessert_ID].dish_json["sugar"]])
            self.meals[meal_id] = {"name" : meal_name,
                            "ID": meal_id,
                            "appetizer" : starter_ID,
                            "main" : main_ID,
                            "dessert" : dessert_ID, 
                            "cal" : cal ,
                            "sodium" : sodium,
                            "sugar" : sugar
                            }
            return meal_id, 200
            
dishes_col = dishes_collection()
meals_col = meals_collection(dishes_col)

class dishes(Resource):
    global dishes_col
    global meals_col

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Content-Type', location='headers')
        args_1 = parser.parse_args()
        content_type = args_1.get('Content-Type')
        if content_type != 'application/json':
            return 0, 415


        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dishes_col.id_num)
        response = requests.get(api_url, headers={'X-Api-Key': 'JTNwmSBjEi97fQhVG0cWuQ==FgDuQk8zsrFueEyU'})
        if (response.headers.get('content-type') != 'application/json'):
            return 0, 415
        
        parser.add_argument('name', location='json', required = False)
        args = parser.parse_args()
        if args["name"] == None:
            return -1, 422
        else:
            return dishes_col.insert_dish(args["name"])
        
    def get(self):
        outputDict = {}
        for key, dish in dishes_col.dishes.items():
            outputDict[key] = dish.dish_json
        return outputDict, 200

class meals(Resource):
    global meals_col

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Content-Type', location='headers')
        args_1 = parser.parse_args()
        content_type = args_1.get('Content-Type')
        if content_type != 'application/json':
            return 0, 415



        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(dishes_col.id_num)
        response = requests.get(api_url, headers={'X-Api-Key': 'JTNwmSBjEi97fQhVG0cWuQ==FgDuQk8zsrFueEyU'})
        if (response.headers.get('content-type') != 'application/json'):
            return 0, 415
        parser.add_argument('name', location='json', required=False)
        parser.add_argument('appetizer', location='json', required=False)
        parser.add_argument('main', location='json', required=False)
        parser.add_argument('dessert', location='json', required=False)
        args = parser.parse_args()
        if ((args["name"] == None) or (args["appetizer"] == None) or (args["main"] == None) or (args["dessert"] == None)):
            return -1, 422
        else:
            appetizer_int = int(args["appetizer"])
            main_int = int(args["main"])
            dessert_int = int(args["dessert"])
            return meals_col.add_meal(args["name"],appetizer_int, main_int, dessert_int)

    def get(self):
        return meals_col.meals, 200
        
class dishKey(Resource):
    global meals_col

    def get(self, key):
        return dishes_col.get_dish_by_id(key)
    
    def delete(self, key):
        return dishes_col.delete_dish_by_id(key, meals_col)

class dishName(Resource):
    global meals_col

    def get(self, name):
        return dishes_col.get_dish_by_name(name)
    
    def delete(self, name):
        return dishes_col.delete_dish_by_name(name, meals_col)

class mealKey(Resource):
    global dishes_col

    def get(self, key):
        return meals_col.get_meal_by_id(key)
    
    def delete(self, key):
        return meals_col.delete_meal_by_id(key)
    
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('appetizer', location='json', required=True)
        parser.add_argument('main', location='json', required=True)
        parser.add_argument('dessert', location='json', required=True)
        args = parser.parse_args()
        appetizer_int = int(args["appetizer"])
        main_int = int(args["main"])
        dessert_int = int(args["dessert"])
        return meals_col.put_update(args["name"], appetizer_int, main_int, dessert_int, key)

class mealName(Resource):
    global dishes_col

    def get(self, name):
        return meals_col.get_meal_by_name(name)
    
    def delete(self, name):
        return meals_col.delete_meal_by_name(name)

if __name__ == '__main__':
    api.add_resource(dishes, '/dishes')
    api.add_resource(meals, '/meals')
    api.add_resource(dishKey, '/dishes/<int:key>')
    api.add_resource(dishName, '/dishes/<string:name>')
    api.add_resource(mealKey, '/meals/<int:key>')
    api.add_resource(mealName, '/meals/<string:name>')
    print("running my app")
    app.run(host='0.0.0.0', port=8000, debug=True)
    