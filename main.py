import pymongo
from flask import Flask, jsonify

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
