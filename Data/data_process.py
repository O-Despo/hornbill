import numpy as np
import csv
import pandas as pd
import re

AT_PATTERN = re.compile('(@.*?)')
LINK_PATTERN = re.compile('https?\S*')
QUOTE_PATTERN = re.compile('&quot.*?&quot')

file = open('./Data/training.1600000.processed.noemoticon.csv', 'r', encoding="utf8", errors='ignore')
csv_read = csv.reader(file)

out_file = open('./Data/sent140.csv', 'w+')
write_csv = csv.writer(out_file)

tweet = "@MissXu sorry! bed time came here (GMT+1)   http://is.gd/fNge"
tweet = re.sub(AT_PATTERN, ' atuser ', tweet)
tweet = re.sub(LINK_PATTERN, ' url ', tweet)
tweet = re.sub(QUOTE_PATTERN, ' userquote ', tweet)
tweet = re.sub(re.compile('[[:punct:]]'), ' ', tweet)


i = 0
for line in csv_read:
    #Text
    tweet = line[-1]
    tweet = re.sub(AT_PATTERN, ' atuser ', tweet)
    tweet = re.sub(LINK_PATTERN, ' url ', tweet)
    tweet = re.sub(QUOTE_PATTERN, ' userquote ', tweet)
    tweet = re.sub(re.compile('/[[:punct:]]/g'), ' ', tweet)

    #Score
    if line[0] == 4: score = 1
    else: score = 0

    i += 1
    write_csv.writerow([score, tweet])