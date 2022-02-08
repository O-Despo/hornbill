"""twitter_api_client:
    A Class that will automates reputable tasks when connecting to the Twitter API.
    Made by O-Despo"""

import os
import time
import bson
import json
import logging
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

class client():
    def __init__(self, script_name, temp_sub_endpoint=False, log_file=False, auth=False):
        """Auth defaults to dotenv, temp_endpoint is the default endpoint used"""
        load_dotenv()

        if log_file:
            log_file = log_file
        else:
            log_file = f'./logs/{script_name}.log'

        if os.path.isfile(log_file) == False:
            file = open(log_file, 'w+')
            file.close()

        if temp_sub_endpoint:
            self.sub_endpoint = self.TW_ENDPOINT + temp_sub_endpoint

        if auth:
            self.Headers = {'Authorization': auth}
        else:
            self.Headers = {'Authorization': os.getenv('TOKEN')}
        
        logging.basicConfig(filename=log_file, encoding="UTF-8", level=logging.DEBUG)
        logging.debug("Client Started by %s at %s: %d", script_name, time.ctime(), time.time())

        breakpoint()
        self.TW_ENDPOINT = "https://api.twitter.com"
             
        client = MongoClient(os.getenv('MONGO'))
        self.db = client[os.getenv('MONGO_DB')]

        self.default_col = os.getenv('MONGO_COL_TRENDS')



    def call_one(self, params, sub_endpoint=False, insert=True, mongo_col=False):
        logging.debug("Call Started %s: %d", time.ctime(), time.time())

        if mongo_col == False: mongo_col = self.default_col

        if sub_endpoint:
            one_call_endpoint = self.TW_ENDPOINT + sub_endpoint
        else:
            one_call_endpoint = self.TW_ENDPOINT
        
        response = requests.get(one_call_endpoint, params=params, headers=self.Headers)

        code = response.status_code
        if 199 < response.status_code > 300:
            logging.error("API request failed with code %d", code)

        response_json = response.json()
        return_json = response_json.copy()

        if insert:
            if type(response_json) == list: 
                if len(response_json) == 1:
                    response_json = response_json[0]
                else:
                    response_json = {'data': response_json}
            
            self.db[mongo_col].insert_one(response_json)
            logging.debug("Success: Mongo insert success")

        logging.debug("Call finished %s: %s", time.ctime(), time.time())
        return return_json 

    def many_call(self, params_list, sub_endpoint = False, insert = True):
        """Enables making many calls to the twitter api"""
        logging.debug("Many call started %s: %s", time.ctime(), time.time())

        for param_dict in params_list:
            self.call_one(param_dict, sub_endpoint=sub_endpoint, insert = insert)

        logging.debug("Many finished started %s: %d", time.ctime(), time.time())