from curses import flash
import os
import tensorflow as tf
import tensorflow_datasets as tfds

def download_ds(download):
    test_ds, train_ds = tfds.load('sentiment140', split=['test', 'train'], download=download, data_dir="./sentiment140")
    assert isinstance(test_ds, tf.data.Dataset)
    
    print(test_ds, train_ds)

if os.path.isdir('./sentiment140'):
    print('Downloading dataset: ')
    download_ds(False)
    print('Sucess: downloaded and loaded data set')

else: 
    download_ds(True)
    print('Sucess: loaded dataset')