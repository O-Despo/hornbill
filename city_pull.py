"""A program to retrive the currenct trending topics and put them into a data base"""
import os
import pdb
import json
import requests
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Start mongo connection
client = MongoClient(os.getenv('MONGO'))
db = client[os.getenv('MONGO_DB')]
col = db[os.getenv('MONGO_COL')]

# API
tw_endpoint = "https://api.twitter.com/1.1/trends"
tw_ep_aval_locs = tw_endpoint + "/available.json"

Headers = {'Authorization': os.getenv('TOKEN')}

resp = requests.get(tw_ep_aval_locs, headers=Headers)

# with open('pos_locs.json', 'w+') as file:
    # json.dump(resp.json(), file)

resp_loc = resp.json()

for loc in resp_loc:
    loc['time']: datetime.time()

col.insert_many(resp_loc)
