"""trending_pull:
    a script to get the current trending topics in the US
    the responses will be entered into the mongo db
    will be run on a hourly interval as cron job
    Made by O-Despo"""

import os
import time
import logging
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

logging.basicConfig(filename="./logs/trending_pull.log", encoding="utf-8", level=logging.DEBUG)
logging.debug("Time Started %s: %d", time.ctime(), time.time())

TW_ENDPOINT = "https://api.twitter.com/1.1/trends"
TW_ENDPOINT_PLACES = TW_ENDPOINT + "/place.json"
TW_US_ID = '23424977'

# Env
load_dotenv()

# Start mongo connection
client = MongoClient(os.getenv('MONGO'))
db = client[os.getenv('MONGO_DB')]
col = db[os.getenv('MONGO_COL_TRENDS')]

# API
Headers = {'Authorization': os.getenv('TOKEN')}
Params = {'id': TW_US_ID}

response = requests.get(TW_ENDPOINT_PLACES, params=Params, headers=Headers)

code = response.status_code
if code > 300 or code < 199:
    logging.error("API request failed with code %d", code)

response_json = response.json()
response_json[0]['time'] = time.ctime()

try:
    col.insert_many(response_json)
    logging.debug("Sucsess with code %d", code)
except:
    logging.error("Failed: mongo insert failed withe err")

logging.debug("Time Finished %s: %d", time.ctime(), time.time())
