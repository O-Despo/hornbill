from pyMongo import MongoClient
import numpy as np
import pandas as pd

client = MongoClient('localhost', 27717)
tweets_col = client['hornbill_v2']['tweets']

happy_count = tweets_col.documnet_count({'emotion': 'happy'})
sad_count = tweets_col.documnet_count({'emotion': 'sad'})

if happy_count < sad_count:
    tweets_to_pull = happy_count
else:
    tweets_to_pull = sad_count

happy_tweet_pull = tweets_col.document({'emotion': 'happy'})
sad_tweet_pull = tweets_col.document({'emotion': 'sad'})

data_table_format = happy_tweet_pull.update(sad_tweets)

data_table = []

def emotion(emotion):
    if emotion == "happy": return 1
    else: return 0

for obj in data_table_fromat:
    data_table.append([str(obj['tweet']), emotion(obj['emotion']))

data_as_pandas = pd.DataFrame(data=data_table, columns=('tweets', 'emotions'), dtype=(('tweets', 'str'),('emotions', 'int'))

data_as_pandas.save_as_csv('./data/tweets_unprocessed.csv')
