import numpy as np
import csv
import pandas as pd
import re
from string import punctuation

AT_PATTERN = re.compile('(@.*?)')
LINK_PATTERN = re.compile('https?\S*')
QUOTE_PATTERN = re.compile('&quot.*?&quot')

TWEETS_FOR_TEST = 1000

file = open('./Data/training.1600000.processed.noemoticon.csv', 'r', encoding="utf8", errors='ignore')
csv_read = csv.reader(file)

test_out_file = open('./Data/sent140-test.csv', 'w+')
test_csv_write = csv.writer(test_out_file)

train_out_file = open('./Data/sent140-train.csv', 'w+')
train_csv_write = csv.writer(train_out_file)

test_score_counts_dict = {0: 0, 1:0}
tweets_per_score = int(TWEETS_FOR_TEST/2)

for line in csv_read:
    tweet = line[-1]
    tweet = re.sub(AT_PATTERN, ' atuser ', tweet)
    tweet = re.sub(LINK_PATTERN, ' url ', tweet)
    tweet = re.sub(QUOTE_PATTERN, ' userquote ', tweet)
    tweet = ''.join([c for c in tweet if c not in punctuation])

    #Score
    if line[0] == "4": score = 1
    else: score = 0

    if test_score_counts_dict[score] < tweets_per_score:
        test_csv_write.writerow([score, tweet])        
    else:
        train_csv_write.writerow([score, tweet])

    test_score_counts_dict[score] += 1