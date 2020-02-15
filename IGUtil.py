import requests
import json
from pymongo import MongoClient
import time
import os

token = '6ha3tGKyJqphGt43ATmGPq2CE'

runRequestURL = f'https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/run-sync?token={token}'
getDataURL = f'https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs/last/dataset/items?token={token}'

debug = True


class IGUtil:
    def __init__(self, config):
        self.client = MongoClient(os.environ['MONGODB_HOSTNAME'], 27017)
        self.db = self.client[config['database']]
        self.home_collection = self.db[config['Home_Collection']]
        self.data = None

    def resetHomeScreen(self):
        self.home_collection.drop()
        self.home_collection.insert_many(self.data)

    def getLastRun(self):
        responseData = requests.get(getDataURL, headers={"Content-Type": "application/json"})
        if debug:
            print(f'Response: {responseData}')
        if responseData.ok:
            data = json.loads(responseData.content)
            cleanData = []
            for d in data:
                cleanData.append({k: d[k] for k in ("timestamp", "url", "imageUrl", "firstComment")})
            return cleanData

        else:
            print(f'Error: {responseData.content}')
            return None

    def getIGOnce(self):
        if debug:
            print(f'URL: {runRequestURL}')

        body = json.loads('''{
          "search": "Doomsday Coffee Cantina",
          "searchType": "user",
          "resultsType": "posts",
          "proxy": {
            "useApifyProxy": true
          }
        }''')
        response = requests.post(runRequestURL, headers={"Content-Type": "application/json"}, json=body)
        if debug:
            print(f'Response: {response}')
        if response.ok:
            if debug:
                print(f'URL: {getDataURL}')
                cleanData = self.getLastRun()
                self.data = cleanData
                self.resetHomeScreen()

        else:
            print(f'Error: {response.content}')

    def getIGforHomeScreen(self):
        while True:
            self.getIGOnce()
            time.sleep(30)
