import pymongo
from flask import Flask, jsonify, request, redirect
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

client = pymongo.MongoClient(
    "mongodb+srv://admin:adminqwerty@book-of-recipe-mx8jr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

book_of_recipes_database = client["book-of-recipe"]
book_of_recipes_collection = book_of_recipes_database["recipes"]


@app.route('/')
@app.route('/index')
def main():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find()]))


@app.route('/catalog')
def show_catalog():
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find()]))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        book_of_recipes_collection.insert_one({'name': request.get_json()["name"],
                                               'category': request.get_json()["category"],
                                               'ingredients': request.get_json()["ingredients"],
                                               'calorie': request.get_json()["calorie"],
                                               'recipe': request.get_json()["recipe"],
                                               'celebratory': request.get_json()["celebratory"],
                                               'photo': request.get_json()["photo"],
                                               'like': 0})
        return "Рецепт добавлен"
    return redirect('/')


@app.route('/edit_recipe', methods=['GET', 'POST'])
def edit_recipe():
    if request.method == 'POST':
        print([i for i in book_of_recipes_collection.find({"_id": ObjectId(request.get_json()["_id"])})])
        print(request.get_json()["_id"])
        result = book_of_recipes_collection.update_one({
            "_id": ObjectId(request.get_json()["_id"])

        }, {
            "$set": {'name': request.get_json()["name"],
                     'category': request.get_json()["category"],
                     'ingredients': request.get_json()["ingredients"],
                     'calorie': request.get_json()["calorie"],
                     'recipe': request.get_json()["recipe"],
                     'celebratory': request.get_json()["celebratory"],
                     'photo': request.get_json()["photo"],
                     'like': request.get_json()["like"]
                     }}, upsert=False)
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()
