from IGUtil import IGUtil
from InstagramScraper import InstagramScraper

import json
import time 



with open('config.json') as json_data_file:
    data = json.load(json_data_file)
ig = IGUtil(data)
IS = InstagramScraper()

while True:
    data = IS.getRecentPosts()
    if(False):
        print(f"data: {data}")
    ig.saveData(data)
    time.sleep(30)#Wait 30 secs
    #print('Working...')

