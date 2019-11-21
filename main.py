import os
import pymongo
from flask import Flask, jsonify, request, redirect, flash
from bson.objectid import ObjectId
from dotenv import load_dotenv


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

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
    flash('Рецепт добавлен')
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find()]))


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
        book_of_recipes_products.insert_one({'name': request.get_json()["name"],
                                             'category': request.get_json()["category"],
                                             'calorie': request.get_json()["calorie"]})
        return "Продукт добавлен"
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()
