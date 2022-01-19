import tensorflow_datasets as tfds

test_ds, train_ds = tfds.load('sentiment140', split=['test', 'train'], download=download, data_dir="./sentiment140")
