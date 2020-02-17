
from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
from IGUtil import IGUtil

application = Flask(__name__)

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
print(data)

client = MongoClient(os.environ['MONGODB_HOSTNAME'], 27017)

db = client[data['database']]
drink_collection = db[data['Drink_Collection']]
food_collection = db[data['Food_Collection']]
home_collection = db[data['Home_Collection']]

igUtil = IGUtil(data)


@application.route("/foods", methods=['GET'])
def get_foods():
    try:
        values = food_collection.find()
        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


@application.route("/drinks", methods=['GET'])
def get_drinks():
    try:
        values = drink_collection.find()
        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


@application.route("/home", methods=['GET'])
def get_home():
    try:
        values = home_collection.find()
        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


@application.route("/", methods=['GET'])
def get_all():
    try:
        values = None
        collections = db.get_collection()
        for coll in collections:
            values = values + db[coll].find()

        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
