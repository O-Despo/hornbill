import twitter_api_client
from pymongo import MongoClient
from dotenv import load_dotenv
import time
import os
import sys
import json

api_client = twitter_api_client.client(__name__)

queries_base = {
"happy": [
            '😁',
            '😀',
            '😆',
            '😃',
            '🙂'
        ],
"sad":[
            '😭',
            '😭',
            '😥',
            '😞',
            '☹️']
}

def assemble_queries(queries_base):
    """Makes more compelx queries string from a dirctionary indexed by emtions 
    each containing a list of chraters revevant to the emotion."""
    
    #Goes through each emote and makes a more compelx query string
    final_query_list = []

    for emotion, emoji_list in queries_base.items():
        print(emoji_list)
        #A string of all the emojis not for this emotion to be excluded
        exclude_str = " "
        for exclude_list in queries_base.values():
            if emoji_list != exclude_list:
                for exclude_emoji in exclude_list:
                    exclude_str += f" -{exclude_emoji} "

        for emoji in emoji_list:
            query = f"{emoji} {exclude_str}"
            final_query_list.append({"emoji": emoji, "emotion": emotion, "query": query})

    return final_query_list

NUMBER_OF_TRENDS = 37

def get_trends(api_client, cut_off):
    """Retrives a list of currect trends and returns a concatated form"""
    US_WOEID = 23424977
    EXPANTIONS = 'author_id'
    trending_endpoint = "/1.1/trends/place.json"
    
    trends_params = {'id': US_WOEID}
    trends_json = api_client.call_one(trends_params, trending_endpoint)

    trends_search_terms = [trend['name'] for trend in trends_json[0]["trends"]]
    
    return trends_search_terms[:cut_off], trends_json

class trend_query_genertor():
    def __init__(self, emoji_querys, trends) -> None:
        self.emoji_querys = emoji_querys
        self.trends = trends.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        query_obj_list = []

        trend_search_term = self.trends.__next__()
        output_objs = []

        for emoji_obj in self.emoji_querys:
            trend_obj = emoji_obj.copy()

            trend_obj['query'] = f"{trend_search_term} {emoji_obj['query']} -is:retweet"            
            trend_obj['trend'] = trend_search_term

            output_objs.append(trend_obj)

        return  output_objs

def get_trends(api_client, cap):
    US_WOEID = 23424977
    EXPANTIONS = 'author_id'

    trending_endpoint = "/1.1/trends/place.json"
    trends_params = {'id': US_WOEID}

    trends_json = api_client.call_one(trends_params, trending_endpoint)
    trends_search_terms = [trend['name'] for trend in trends_json[0]["trends"]]
    
    return trends_search_terms[:cap], trends_json

def run_query(query, api_client):
    search_endpoint = "/2/tweets/search/recent"

    query = {"query": f"{query['query']} lang:en", "max_results": 100}
    query_resp = api_client.call_one(query, search_endpoint)

    return query_resp 

assembled_emoji_qrys = assemble_queries(queries_base)
trend_list, trend_pure_json = get_trends(api_client, 10)
trend_qry_gen = trend_query_genertor(assembled_emoji_qrys, trend_list)

load_dotenv()
db_client = MongoClient(os.getenv('MONGO'))
hornbill_db = db_client['hornbill_v2_test']

trend_id = hornbill_db['trend_pure_json'].insert_one(trend_pure_json[0])

for query_obj_list in trend_qry_gen:

    for query in query_obj_list: 
        tweets_bulk = []

        query_resp = run_query(query, api_client)

        #Check for "to many request error"
        if 'status' in query_resp.keys() and query_resp['status'] == 429:
            twitter_api_client.logging.error(f"to many requets at {time.time()}")
            sys.exit()
        elif query_resp['meta']['result_count'] == 0:
            sys.exit()

        #Extra data
        hornbill_db['extra_data'].insert_one(
            {'type': 'len', 
            'len': query_resp['meta']['result_count'],
            'emoji': query['emoji'],
            'trend': query['trend']
            })
        data = query_resp['data']

        for tweet in data:
            tweet_json = {
                'text': tweet['text'],
                'tweet_id': tweet['id'],
                'emotion': query['emotion'],
                'trend': query['trend'],
                'time': time.time(),
                'query_id': trend_id.inserted_id,
                'query': query['query'],
                'emoji': query['emoji']
            }

            hornbill_db['tweets'].insert_one(tweet_json)
        


