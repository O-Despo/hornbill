import tensorflow as tf
import tensorflow
from tensorflow import tfdf
import numpy as np
import pandas as pd
import csv

BUFFER_SIZE = 10000
BATCH_SIZE = 1024
VOCAB_SIZE = 1000

train_db = pd.read_csv('./Data/sent140-train.csv', names=['score', 'tweet'])
test_db = pd.read_csv('./Data/sent140-test.csv', names=['score', 'tweet'])

train_db = train_db.shuffle(BUFFER_SIZE)
train_db = train_db.batch(BATCH_SIZE)

text_encode = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode='int',
    output_sequence_length=100
)


#Model
print(text_encode.get_vocabulary())
model = tf.keras.Sequential([
    text_encode,
    tf.keras.layers.Embedding(
        input_dim=len(text_encode.get_vocabulary()),
        output_dim=32,
        mask_zero=True),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='relu')
    ])
model.summary()
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])

model.predict(np.array(['Confession time: I tweeted last week that LA would lose game 1 by 15. Sorry, I meant to say Game 2.']))
history = model.fit(train_db, epochs=5, validation_data=test_db, validation_steps=30)

t_loss, t_acc = model.evaluate(test_db)
print(f"Loss: {t_loss}, Acc {t_acc}")