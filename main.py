import pymongo
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

client = pymongo.MongoClient("mongodb+srv://admin:adminqwerty@cookerybook-mx8jr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

cookery_database = client["cookerybook"]
cookery_list_collection = cookery_database["cookery-list"]


@app.route('/')
@app.route('/index')
def main():
    return jsonify(', '.join([str(item.get('text')) for item in cookery_list_collection.find()]))
