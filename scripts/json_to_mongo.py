#!/bin/python
"""
A script that takes a JSON file and imports it into mongo Col.
This is be used to restore Mongo backups
"""
import sys
import os
import json
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values('../.env')

client = MongoClient(config.MONGO)
db = client[config.MONGO_DB]
col = db[config.MONGO_COL_TRENDS]

json_loc = sys.argv[1]
json_to_load = json.load(open(json_loc))

col.insert_many(json_to_load)
