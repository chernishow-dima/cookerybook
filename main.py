import os
import pymongo
from modules.usdaSearchEnergy import *
from flask import Flask, jsonify, request, redirect
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    output = []
    for item in book_of_recipes_collection.find(limit=3).sort("like", -1):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']
                       })
    return jsonify({'result' : output, 'status': 200})


@app.route('/options', methods=['GET'])
def get_options():
    output_kitchens = []
    output_categories = []
    output_menus = []
    output_ingredients = []
    status = 200
    for item in book_of_recipes_collection.find():
        if item['kitchen'] not in output_kitchens:
            output_kitchens.append(item['kitchen'])
        if item['category'] not in output_categories:
            output_categories.append(item['category'])
        if item['menu'] not in output_menus:
            output_menus.append(item['menu'])
        for ingredient in item['ingredients']:
            if ingredient not in output_ingredients:
                output_ingredients.append(ingredient)
    
    return jsonify({'kitchens': output_kitchens,
                    'categories' : output_categories,
                    'menus': output_menus,
                    'ingredients': output_ingredients,
                    'status': status})


@app.route('/catalog', methods=['GET'])
def show_catalog():
    output = []
    for item in book_of_recipes_products.find():
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})


@app.route('/recipe', methods=['GET'])
def get_recipe():      
    output = []
    print(request.get_json()["_id"])
    for item in book_of_recipes_collection.find({"_id": ObjectId(request.get_json()["_id"])}):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})




@app.route('/recipe', methods=['POST'])
def add_recipe():
    request_body = request.get_json()
    id_recipe= None
    output = []
    id_recipe = book_of_recipes_collection.insert_one({'name': request_body["name"],
                                           'category': request_body["category"],
                                           'ingredients': request_body["ingredients"],
                                           'calorie': request_body["calorie"],
                                           'recipe': request_body["recipe"],
                                           'celebratory': request_body["celebratory"],
                                           'photo': request_body["photo"],
                                           'like': 0,
                                           'kitchen': request_body["kitchen"],
                                           'menu':request_body['menu']}).inserted_id
    if id_recipe != None:
        output.append({'_id': str(id_recipe) , 
                       'name' : request_body['name'],
                       'category' : request_body['category'],
                       'ingredients' : request_body['ingredients'],
                       'calorie':request_body['calorie'],
                       'recipe':request_body['recipe'],
                       'celebratory':request_body['celebratory'],
                       'photo':request_body['photo'],
                       'like':request_body['like'],
                       'kitchen':request_body['kitchen'],
                       'menu':request_body['menu']})
    return jsonify({'result' : output, 'status': 201})
    


@app.route('/recipe', methods=['PATCH'])
def edit_recipe():
    request_body = request.get_json()
    output = []
    id_object = ObjectId( request.get_json()["_id"])
    print(id_object)
    book_of_recipes_collection.update_one({
        "_id": id_object
    }, {
        "$set": {'name': request_body["name"],
                 'category': request_body["category"],
                 'ingredients': request_body["ingredients"],
                 'calorie': request_body["calorie"],
                 'recipe': request_body["recipe"],
                 'celebratory': request_body["celebratory"],
                 'photo': request_body["photo"],
                 'like': request_body["like"],
                 'kitchen': request_body["kitchen"],
                 'menu':request_body['menu']}
                 }, upsert=False)    
    
    num_id = book_of_recipes_collection.find({ "_id": id_object }).count() 
    print(num_id)            
    if num_id != 0:
        output.append({'_id': str(id_object) , 
                       'name' : request_body['name'],
                       'category' : request_body['category'],
                       'ingredients' : request_body['ingredients'],
                       'calorie':request_body['calorie'],
                       'recipe':request_body['recipe'],
                       'celebratory':request_body['celebratory'],
                       'photo':request_body['photo'],
                       'like':request_body['like'],
                       'kitchen':request_body['kitchen'],
                       'menu':request_body['menu']})
    return jsonify({'result' : output, 'status': 200})
    
    


@app.route('/recipe', methods=['DELETE'])
def del_recipe():
    book_of_recipes_collection.delete_one({"_id": ObjectId(request.get_json()["_id"])})
    return jsonify({'status': 200})


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    item = book_of_recipes_products.find_one({"name": request.get_json()["name"]})
    if item is None:
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

        return jsonify({"result": usda_result_energy})
    else:
        return jsonify({"result": item['calorie']})


@app.route('/search_by_popularity', methods=['GET'])
def search_by_popularity():    
    output = []
    for item in book_of_recipes_collection.find().sort("like", -1):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})


@app.route('/search_by_kitchen', methods=['GET'])
def search_by_kitchen():     
    output = []
    for item in book_of_recipes_collection.find({"kitchen": request.get_json()["kitchen"]}):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})


@app.route('/search_by_name', methods=['GET'])
def search_by_name():     
    output = []
    for item in book_of_recipes_collection.find({"name": request.get_json()["name"]}):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})


@app.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    request_body = request.get_json()
    request_body_values = request_body.values()
    flag = 1     
    output = []

    for item in book_of_recipes_collection.find() :
        for elem in request_body_values :               
            if elem not in item.get("ingredients").values() :
                flag = 0
        if flag == 1 :                        
            output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})    
        flag = 1   
    return jsonify({'result' : output, 'status': 200})      


@app.route('/search', methods=['GET'])
def general_search():    
    output = []
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
            output.append({'_id': str(item['_id']) , 
                           'name' : item['name'],
                           'category' : item['category'],
                           'ingredients' : item['ingredients'],
                           'calorie':item['calorie'],
                           'recipe':item['recipe'],
                           'celebratory':item['celebratory'],
                           'photo':item['photo'],
                           'like':item['like'],
                           'kitchen':item['kitchen'],
                           'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})
      


@app.route('/sort_calories_ascending', methods=['GET'])
def sort_calories_ascending():    
    output = []
    for item in book_of_recipes_collection.find().sort("calorie", 1):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})


@app.route('/sort_calories_descending', methods=['GET'])
def sort_calories_descending():    
    output = []
    for item in book_of_recipes_collection.find().sort("calorie", -1):
        output.append({'_id': str(item['_id']) , 
                       'name' : item['name'],
                       'category' : item['category'],
                       'ingredients' : item['ingredients'],
                       'calorie':item['calorie'],
                       'recipe':item['recipe'],
                       'celebratory':item['celebratory'],
                       'photo':item['photo'],
                       'like':item['like'],
                       'kitchen':item['kitchen'],
                       'menu':item['menu']})
    return jsonify({'result' : output, 'status': 200})



if __name__ == '__main__':
    app.debug = True
    app.run()
