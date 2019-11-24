import os
import pymongo
import json
import requests
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
@app.route('/index')
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
                                           'like': 0})
    return "Рецепт добавлен"


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
                 'like': request_body["like"]
                 }}, upsert=False)
    return "Рецепт изменен"


@app.route('/recipe', methods=['DELETE'])
def del_recipe():
    book_of_recipes_collection.delete_one({"_id": ObjectId(request.get_json()["_id"])})
    return "Рецепт удален"


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if request.method == 'POST':
        if book_of_recipes_products.find_one({"name": request.get_json()["name"]}) == None:
            yandex_translate_api_string = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=" + os.environ.get("YANDEX_API_KEY", None) + "&text=" + request.get_json()["name"] + "&lang=en"
            usda_api_search_request_string = "https://api.nal.usda.gov/fdc/v1/search?api_key=" + os.environ.get("USDA_API_KEY", None)
            try:
                yandex_translate_result = json.loads(requests.get(yandex_translate_api_string).content)["text"][0]
                usda_search_result = str(int(json.loads(requests.post(usda_api_search_request_string, None,{"generalSearchInput": yandex_translate_result}).content)["foods"][0]["fdcId"]))

                usda_api_food_inf_result = "https://api.nal.usda.gov/fdc/v1/" + usda_search_result + "?api_key=" + os.environ.get("USDA_API_KEY", None)

                usda_result_energy_json = json.loads(requests.get(usda_api_food_inf_result).content)['foodNutrients']
                usda_result_energy = '-1.0'

                for i in range(len(usda_result_energy_json)):
                    if usda_result_energy_json[i]["nutrient"]["name"] == 'Energy' :
                        usda_result_energy = str(usda_result_energy_json[i]["amount"])

                if usda_result_energy == '-1.0':
                    return jsonify({"result": "Please enter energy of {}".format(request.get_json()["name"]),
                                    "name": request.get_json()["name"],
                                    "category": request.get_json()["category"]})
            except IndexError:
                return jsonify({"result": "Please enter energy of {}".format(request.get_json()["name"])})

            book_of_recipes_products.insert_one({'name': request.get_json()["name"],
                                                 'category': request.get_json()["category"],
                                                 'calorie' : usda_result_energy
                                                 })
            return jsonify({"result": "Success"})
        else:
            return jsonify({"result": "This item has been recently create"})
    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    app.run()
