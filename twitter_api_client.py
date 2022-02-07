"""twitter_api_client:
    A Class that will automates reputable tasks when connecting to the Twitter API.
    Made by O-Despo"""

import os
import time
import logging
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

class client():
    def __init__(script_name, temp_sub_endpoint=False, log_file=False, monog_col, auth=False):
        """Auth defaults to dotenv, temp_endpoint is the default endpoint used"""
        load_dotenv()

        if log_file != True:
            log_file = f'./logs/{script_name}.log'

        logging.basicConfig(filename=f"./logs/{log_file}.log", encoding="utf-8", level=logging.DEBUG)
        logging.debug("Client Started by $s at %s: %d", script_name, time.ctime(), time.time())

        self.TW_ENDPOINT = "https://api.twitter.com"
        
        if temp_sub_endpoint:
            self.sub_endpoint = self.TW_ENDPOINT + self.temp_sub_endpoint

        if auth == False:
            Headers = {'Authorization': os.getenv('TOKEN')}
        else
            Headers = {'Authorization': auth}
            
        client = MongoClient(os.getenv('MONGO'))
        db = client[os.getenv('MONGO_DB')]
        
        if mongo_col:
            self.col = db[mongo_col]
        else:
            self.col = db[os.getenv('MONGO_COL_TRENDS')]


    def call_one(params, sub_endpoint=False, insert=True):
        logging.debug("Call Started %s: %d", time.ctime(), time.time())

        if sub_endpoint:
            one_call_endpoint = self.TW_ENDPOINT + sub_endpoint
        else:
            one_call_endpoint = self.TW_ENDPOINT + self.sub_endpoint
        
        response = requests.get(one_call_endpoint, params=params, headers=self.Headers)


        code = response.status_code
        if 199 < response.status_code > 300:
            logging.error("API request failed with code %d", code)

        response_json = response.json()

       if insert:
            response_json = response.json()
            response_json[0]['time'] = time.ctime()
            col.insert_many(response_json)
            logging.debug("Success: Mongo insert success")

       
        logging.debug("Call finished %s: %d", time.ctime(), time.time())
        return response_json

    def many_call(params_list, sub_endpoint = False, insert = True):
        """Enables making many calls to the twitter api"""
        logging.debug("Many call started %s: %d", time.ctime(), time.time())

        for param_dict in params_list:
            self.call_one(param_dict, sub_endpoint=sub_endpoint, insert = insert)

        logging.debug("Many finished started %s: %d", time.ctime(), time.time())
