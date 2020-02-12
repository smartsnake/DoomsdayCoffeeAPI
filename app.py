
from flask import Flask
from threading import Thread
from pymongo import MongoClient
from bson.json_util import dumps
import json
from IGUtil import IGUtil

app = Flask(__name__)

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
print(data)

client = MongoClient(data['mongo_url'], int(data['mongo_port']))

db = client[data['database']]
drink_collection = db[data['Drink_Collection']]
food_collection = db[data['Food_Collection']]
home_collection = db[data['Home_Collection']]

igUtil = IGUtil(data)


@app.route("/foods", methods=['GET'])
def get_foods():
    try:
        values = food_collection.find()
        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


@app.route("/drinks", methods=['GET'])
def get_drinks():
    try:
        values = drink_collection.find({'Is_Drink': True})
        return dumps(values)
    except Exception as e:
        return dumps({'error': str(e)})


@app.route("/", methods=['GET'])
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
    thread = Thread(target=igUtil.getIGforHomeScreen)
    thread.start()
    thread.join()

    app.debug = True
    app.run(host='0.0.0.0')
