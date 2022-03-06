#!/bin/bash
cd /home/lttk-data/hornbill
echo $(date) >> ./scripts/run_tweets.log
python3 ./emote_shearch.py
