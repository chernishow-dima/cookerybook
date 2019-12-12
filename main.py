import os
import pymongo
from modules.usdaSearchEnergy import *
from flask import Flask, jsonify, request, redirect
from bson.objectid import ObjectId
from dotenv import load_dotenv

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

load_dotenv("venv/.env")
MONGO_URI = os.environ.get('MONGO_URI', None)

client = pymongo.MongoClient(MONGO_URI)
db = client.test

book_of_recipes_database = client["book-of-recipe"]
book_of_recipes_collection = book_of_recipes_database["recipes"]
book_of_recipes_products = book_of_recipes_database["products"]


@app.route('/')
def main():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find()]))


@app.route('/catalog', methods=['GET'])
def show_catalog():
    return jsonify(', '.join([str(item) for item in book_of_recipes_products.find()]))


@app.route('/recipe', methods=['GET'])
def get_recipe():
    return jsonify(str(book_of_recipes_collection.find_one({'_id': ObjectId(request.args.get('id'))})))


@app.route('/recipe', methods=['POST'])
def add_recipe():
    request_body = request.get_json()
    book_of_recipes_collection.insert_one({'name': request_body["name"],
                                           'category': request_body["category"],
                                           'ingredients': request_body["ingredients"],
                                           'calorie': request_body["calorie"],
                                           'recipe': request_body["recipe"],
                                           'celebratory': request_body["celebratory"],
                                           'photo': request_body["photo"],
                                           'like': 0,
                                           'kitchen': request_body["kitchen"]})
    # Вернуть полученные данные + статус(201)
    return jsonify()


@app.route('/recipe', methods=['PATCH'])
def edit_recipe():
    request_body = request.get_json()
    book_of_recipes_collection.update_one({
        "_id": ObjectId(request.args.get('id'))
    }, {
        "$set": {'name': request_body["name"],
                 'category': request_body["category"],
                 'ingredients': request_body["ingredients"],
                 'calorie': request_body["calorie"],
                 'recipe': request_body["recipe"],
                 'celebratory': request_body["celebratory"],
                 'photo': request_body["photo"],
                 'like': request_body["like"],
                 'kitchen': request_body["kitchen"]
                 }}, upsert=False)
    return "Рецепт изменен"


@app.route('/recipe', methods=['DELETE'])
def del_recipe():
    book_of_recipes_collection.delete_one({"_id": ObjectId(request.get_json()["_id"])})
    return "Рецепт удален"


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if request.method == 'POST':
        if book_of_recipes_products.find_one({"name": request.get_json()["name"]}) is None:
            try:
                usda_result_energy = find_energy(request.get_json()["name"])
                if usda_result_energy == '-1.0':
                    return jsonify({"result": "Please enter energy of {}".format("name"),
                                    "name": request.get_json()["name"],
                                    "category": request.get_json()["category"]})
            except IndexError:
                return jsonify({"result": "Please enter energy of {}".format("name")})

            book_of_recipes_products.insert_one({'name': request.get_json()["name"],
                                                 'category': request.get_json()["category"],
                                                 'calorie': usda_result_energy
                                                 })

            return jsonify({"result": "Success"})
        else:
            return jsonify({"result": "This item has been recently create"})
    return redirect('/')


@app.route('/search_by_popularity', methods=['GET'])
def search_by_popularity():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find().sort("like", -1)]))


@app.route('/search_by_kitchen', methods=['GET'])
def search_by_kitchen(): 
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find({"kitchen": request.get_json()["kitchen"]})]))


@app.route('/search_by_name', methods=['GET'])
def search_by_name(): 
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find({"name": request.get_json()["name"]})]))


@app.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    request_body = request.get_json()
    request_body_values = request_body.values()
    flag =1 
    json_output = ""

    for item in book_of_recipes_collection.find() :
        for elem in request_body_values :               
            if elem not in item.get("ingredients").values() :
                flag=0
        if flag == 1 : json_output += ', '.join([str(item)])
        flag =1   
    return jsonify(json_output)    


@app.route('/general_search', methods=['GET'])
def general_search():
    json_output = ""
    array_id =[]
    number_id = 0
    flag = 0
    if request.get_json()["name"] != None:
        for item in book_of_recipes_collection.find({"name": request.get_json()["name"]}):
            array_id.append(item.get("_id"))
            flag = 1
        if flag == 1 : number_id +=1
        flag = 0    
    if request.get_json()["category"] != None:
        for item in book_of_recipes_collection.find({"category": request.get_json()["category"]}):
            array_id.append(item.get("_id"))
            flag = 1
        if flag == 1 : number_id +=1
        flag = 0
    if request.get_json()["kitchen"] != None:
        for item in book_of_recipes_collection.find({"kitchen": request.get_json()["kitchen"]}):
            array_id.append(item.get("_id"))
            flag = 1
        if flag == 1 : number_id +=1
        flag = 0  
    if request.get_json()["celebratory"] != None:
        for item in book_of_recipes_collection.find({"celebratory": request.get_json()["celebratory"]}):
            array_id.append(item.get("_id"))
            flag = 1
        if flag == 1 : number_id +=1
        flag = 0 

    for item in book_of_recipes_collection.find():
        if array_id.count(item.get("_id")) == number_id:
            json_output += ', '.join([str(item)])

    return jsonify(json_output)        


@app.route('/sort_calories_ascending', methods=['GET'])
def sort_calories_ascending():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find().sort("calorie", 1)]))

@app.route('/sort_calories_descending', methods=['GET'])
def sort_calories_descending():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find().sort("calorie", -1)]))



if __name__ == '__main__':
    app.debug = True
    app.run()
