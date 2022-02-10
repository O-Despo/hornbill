"""emote_pull:
    Script that collects tweets based on the emojis in the tweet.
    Made by O-Despo"""
import json
import time
import os
from dotenv.main import load_dotenv
from pymongo import MongoClient, mongo_client
import twitter_api_client

US_WOEID = 23424977

load_dotenv()

EXPANTIONS = 'author_id'

happy_base_querys = [
            '😁'
            '😀',
            '🤗',
            '😆',
            '😃',
            '🙂'
        ]

sad_base_querys = [
            '😭',
            '😭',
            '😔',
            '😥',
            '😞',
            '☹️'
        ]

emotion_to_querys_dict = {
    "happy": happy_base_querys,
    "sad": sad_base_querys
    }

def runEmoteQuerys(search_term, emotion_to_querys_dict, api_client):
    emote_reps = {}

    for emotion, base_querys in emotion_to_querys_dict.items():
        temp_query_resps = []

        for base_query in base_querys:
            query = f"({search_term}) ({base_query}) lang:en"
            json_resp = api_client.call_one({'query': query, 'expansions': EXPANTIONS}, search_endpoint)
            temp_query_resps.append(json_resp)
        
        emote_reps[emotion] = temp_query_resps
    
    return emote_reps

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

trending_search_terms = [trend['name'] for trend in trends_json[0]["trends"]]
# Happy and sad query

for trend_search_term in trending_search_terms:
    emote_query_response = runEmoteQuerys(trend_search_term, emotion_to_querys_dict, api_client)

    db['emote_query_resp'].insert_one(emote_query_response.copy())
    
    for emote_group, query_results_list in emote_query_response.items():
        emote_groups_tweets = []

        for query_results in query_results_list:
            if query_results['meta']['result_count'] == 0: continue

            for tweet in query_results['data']:
                    emote_groups_tweets.append({'tweet_id': tweet['id'],
                        'text': tweet['text'],
                        'class': emote_group,
                        'search_term': trend_search_term,
                        'author_id': tweet['author_id'],
                        'time_of_process': time.time()
                    })
    
    db['tweets'].insert_many(emote_groups_tweets)