import sys
sys.path.append(r"C:\Users\vince\AppData\Local\Programs\Python\Python37\Lib\site-packages")

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("yuh")

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
tfds.disable_progress_bar()

print("aiyaaaa")

from tensorflow.keras import layers

splits = tfds.Split.ALL.subsplit(weighted=(75,25))
splits, info = tfds.load('food101', with_info=True, split=splits)

print("yes")