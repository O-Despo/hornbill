import requests
import os
import time 
from termcolor import cprint, colored
import random
from dotenv import load_dotenv

load_dotenv()
headers = {'Authorization': os.getenv('TOKEN')}

url = 'https://api.twitter.com/1.1/trends/place.json'
params = {'id': 1}

def runPosibleLocations():
    locUrl = "https://api.twitter.com/1.1/trends/available.json"
    resp = requests.get(locUrl, headers=headers)
    all_locs = resp.json()
    return all_locs

def runRequest():
    loc = random.choice(all_locs)
    
    params = {'id': loc['woeid']}
    resp = requests.get(url, params=params,  headers=headers)
    trends = resp.json()[0]['trends']
    
    title = colored(f"New Trends as of {resp.json()[0]['as_of']}", 'grey', 'on_red', attrs=['blink'])
    print(title)
    title = colored(f"From {loc['name']} in {loc['country']}, weoid {loc['woeid']}", 'grey', 'on_blue', attrs=['blink'])
    print(title)
    for trend in trends:
        print(f"TREND: {trend['name']} - Promoted {trend['promoted_content']} - Tweet Volume {trend['tweet_volume']}")
        time.sleep(0.8)
    
    time.sleep(30)
    runRequest()

all_locs = runPosibleLocations()
trends = runRequest()


