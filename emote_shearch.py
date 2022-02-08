"""emote_pull:
    Script that collects tweets based on the emojis in the tweet.
    Made by O-Despo"""
import json
import os
from dotenv.main import load_dotenv
from pymongo import MongoClient, mongo_client
import twitter_api_client

US_WOEID = 23424977

load_dotenv()

def runQuerys(input_query, api_client):
    all_querys_json = {}

    happy_query = f'(😁 OR 😀 OR 🤗 OR 😺 OR 😆 OR 😃 OR 🙂 OR 🤩 OR 😆) {input_query} lang:en'
    sad_query = f'(😭 OR 😢 OR 😔 OR ☹️ OR 😟 OR 😥) {input_query} lang:en'
    
    happy_params = {'query': happy_query, 'max_results': 10}
    sad_params = {'query': sad_query, 'max_results': 10}
    
    params = {
        "happy": happy_params, 
        "sad": sad_params
        }
    
    for param in params.items():
        json_resp = api_client.call_one(param[1], search_endpoint)
        all_querys_json[param[0]] = json_resp
    
    return all_querys_json

client = MongoClient(os.getenv('MONGO'))  
db = client[os.getenv('MONGO_DB')]  

default_col = os.getenv('MONGO_COL_TRENDS')  

trending_endpoint = "/1.1/trends/place.json"
search_endpoint = "/2/tweets/search/recent"

api_client = twitter_api_client.client(__name__)

# Trending hashtags
trends_params = {'id': US_WOEID}
trends_json = api_client.call_one(trends_params, trending_endpoint)

db['tends_v2'].insert_one(trends_json[0])

trending_querys = [trend['name'] for trend in trends_json[0]["trends"]]
# Happy and sad query

for trend_query in [trending_querys[4]]:
    all_querys_json = runQuerys(trend_query, api_client)
    db['emote_query_resp'].insert_one(all_querys_json.copy())
    
    for query_group in all_querys_json.items():
        for tweet in query_group[1]['data']:
            db['tweets'].insert_one({'tweet_id': tweet['id'],
                    'text': tweet['text'],
                    'class': query_group[0]
                })
