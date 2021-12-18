"""
A script that takes a JSON file and imports it into mongo Col.
This is be used to restore Mongo backups
"""
import sys
import json
from dotenv import dotenv_values 
from pymongo import MongoClient

config = dotenv_values()
client = MongoClient(config['MONGO'])
db = client[config['MONGO_DB']]
col = db[config['MONGO_COL_TRENDS']]

json_loc = sys.argv[1]
json_to_load = json.load(open(json_loc))

#_id is removed to prevent id error when entering into mongo
for item in json_to_load:
    del item['_id']
    col.insert_one(item)
