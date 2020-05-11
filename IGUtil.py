import requests
import json
from pymongo import MongoClient
import time
import os
from bs4 import BeautifulSoup
from random import choice
 

#token = '6ha3tGKyJqphGt43ATmGPq2CE'

#runRequestURL = f'https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/run-sync?token={token}'
#getDataURL = f'https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs/last/dataset/items?token={token}'

debug = True

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

class InstagramScraper:
 
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy
 
    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)
 
    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text
 
    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)
 
    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results
 
    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results


class IGUtil:
    def __init__(self, config):
        self.client = MongoClient(config['mongo_url'], 27017)#os.environ['MONGODB_HOSTNAME']#config['mongo_url']
        self.db = self.client[config['database']]
        self.home_collection = self.db[config['Home_Collection']]
        self.data = None

    def saveData(self, data):
        self.data = data
        self.resetHomeScreen()

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

    def newGetIGOnce(self):
        IS = InstagramScraper()
        data = IS.profile_page_recent_posts("https://www.instagram.com/doomsdaycoffee/")

        cleanData = []
        for d in data:
            cleanData.append({k: d[k] for k in ("taken_at_timestamp", "display_url", "edge_media_to_caption")})

        self.data = cleanData
        self.resetHomeScreen()

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
            self.newGetIGOnce()
            print('test..')
            time.sleep(30)#1800)#Wait for 30 mins
