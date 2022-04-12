"""emote_pull:
    Script that collects tweets based on the emojis in the tweet.
    Made by O-Despo"""
import json
import time
import sys
import os
from better_profanity import profanity
from dotenv import load_dotenv
import twitter_api_client
from termcolor import colored

US_WOEID = 23424977
EXPANTIONS = 'author_id'

load_dotenv()

happy_base_querys = [
            '😁',
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
            '☹️']

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
            json_resp = api_client.call_one({'max_results': 100, 'query': query, 'expansions': EXPANTIONS}, search_endpoint)
            temp_query_resps.append(json_resp)
        
        emote_reps[emotion] = temp_query_resps
    
    return emote_reps

trending_endpoint = "/1.1/trends/place.json"
search_endpoint = "/2/tweets/search/recent"

api_client = twitter_api_client.client(__name__)

# Trending hashtags
trends_params = {'id': US_WOEID}
trends_json = api_client.call_one(trends_params, trending_endpoint)

# Inserts trends into Mongo
trending_search_terms = [trend['name'] for trend in trends_json[0]["trends"]]

for trend_search_term in trending_search_terms[0:37]:
    #Emote querys
    emote_query_response = runEmoteQuerys(trend_search_term, emotion_to_querys_dict, api_client)

    c = 0
    for emote_group, query_results_list in emote_query_response.items():
        emote_groups_tweets = []

        #print(emote_groups_tweets)
        for query_results in query_results_list:
            if 'status' in query_results.keys() and query_results['status'] == 429:
                twitter_api_client.logging.error(f"to many requets {trend_search_term} at {time.time()}")
                print('to many requests')
                sys.exit()

            if query_results['meta']['result_count'] == 0: continue

            for tweet in query_results['data']:
                    emote_groups_tweets.append({'tweet_id': tweet['id'],
                        'text': tweet['text'],
                        'class': emote_group,
                        'search_term': trend_search_term,
                        'author_id': tweet['author_id'],
                        'time_of_process': time.time()
                    })
   
    if emote_groups_tweets != []:
        for tweet in emote_groups_tweets:
            tweet['text'] = tweet['text'].replace('\n', '')
            clean_tweet_text = profanity.censor(tweet['text'])
            csrt (= ('0' * (4 - len(str(c)))) + str(c)
            print(f"{csrt} : {clean_tweet_text} : {tweet['class']} : term = {tweet['search_term']}")
            time.sleep(0.1)
            c += 1
    
    print(f'Completed shearch term: {trend_search_term}')
    twitter_api_client.logging.debug(f'Completed: {trend_search_term} at {time.time()}')
