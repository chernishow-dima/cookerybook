import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

client = pymongo.MongoClient("mongodb+srv://admin:adminqwerty@book-of-recipe-mx8jr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

book_of_recipes_database = client["book-of-recipe"]
book_of_recipes_collection = book_of_recipes_database["recipes"]


@app.route('/')
@app.route('/index')
def main():
    return jsonify(', '.join([str(item.get('text')) for item in book_of_recipes_collection.find()]))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.get_json()["name"]
        category = request.get_json()["category"]
        ingredients = request.get_json()["ingredients"]
        calorie = request.get_json()["calorie"]
        recipe = request.get_json()["recipe"]
        celebratory = request.get_json()["celebratory"]
        photo_url = request.get_json()["photo"]
        like = 0
        book_of_recipes_collection.insert_one({'name': name,
                                               'category': category,
                                               'ingredients': ingredients,
                                               'calorie': calorie,
                                               'recipe': recipe,
                                               'celebratory': celebratory,
                                               'photo': photo_url,
                                               'like': like})
        return "Рецепт добавлен"
    return jsonify(', '.join([str(item) for item in book_of_recipes_collection.find()]))

