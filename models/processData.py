import tensorflow as tf
import pandas as pd
import re

VOCAB_SIZE = 1000

def cleanTweets(input_text):
        input_text = input_text.lower(input_text)
        input_text = re.replace(input_text, "(@.*?)", " USERAT ")
        return re.replace(input_text, "https?\S*", " URL ")

data = pd.read_csv(dtype=(('tweets', 'str'),('emotions', 'int'))

text_encode = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    standardize=cleanTweets,
    output_mode='int',
    output_sequence_length=100
)

text_encode.compile()
text_encode.adapt((lambda tweet, polarity: tweet))
