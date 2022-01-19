
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow
import numpy as np
import csv

BUFFER_SIZE = 10000
BATCH_SIZE = 1024
VOCAB_SIZE = 100000

URL_REGEX = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"


#Data preprocessing
def cleanTweets(input_text):
    input_text = tf.strings.lower(input_text)
    return tf.strings.regex_replace(input_text, URL_REGEX, "URL", replace_global=True)

train_db, test_db = tfds.load('sentiment140', split=['train', 'test'], data_dir='./sentiment140', as_supervised=True)

train_db = train_db.map(lambda x, y: (x, tf.math.round(y/4)))
test_db = test_db.map(lambda x, y: (x, tf.math.round(y/4)))

train_db = train_db.shuffle(BUFFER_SIZE)
train_db = train_db.batch(BATCH_SIZE)
test_db = test_db.batch(BATCH_SIZE)

text_encode = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    standardize=cleanTweets,
    output_mode='int',
)

text_encode.adapt(train_db.map(lambda tweet, polarity: tweet))

#Model
print(text_encode.get_vocabulary())
model = tf.keras.Sequential([
    text_encode,
    tf.keras.layers.Embedding(
        input_dim=len(text_encode.get_vocabulary()),
        output_dim=64,
        mask_zero=True),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.GlobalAveragePooling1D(),
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