"""emote_pull:
    Script that collects tweets based on the emojis in the tweet.
    Made by O-Despo"""

import os
import time
import logging
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

logging.basicConfig(filename="./logs/emote_pull.log", encoding="UTF-8", level=logging.DEBUG)
logging.debug("Time Started %s: %d", time.ctime(), time.time())

TW_ENDPOINT = "https://api.twitter.com"
TW_ENDPOINT_PLACES = TW_ENDPOINT + "/2/tweets/search/recent"
TW_US_ID = '23424977'

load_dotenv()

# Start mongo connection
client = MongoClient(os.getenv('MONGO'))
db = client[os.getenv('MONGO_DB')]
col = db[os.getenv('MONGO_COL_TRENDS')]

# API
Headers = {'Authorization': os.getenv('TOKEN')}
Params = {'id': TW_US_ID, 'query': emote_query}

response = requests.get(TW_ENDPOINT_PLACES, params=Params, headers=Headers)

code = response.status_code
if 199 < response.status_code > 300:
    logging.error("API request failed with code %d", code)

response_json = response.json()
response_json[0]['time'] = time.ctime()

try:
    col.insert_many(response_json)
    logging.debug("Sucsess with code %d", code)
except:
    logging.error("Failed: mongo insert failed withe err")

logging.debug("Time Finished %s: %d", time.ctime(), time.time())
