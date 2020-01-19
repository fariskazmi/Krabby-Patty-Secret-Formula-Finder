
#code to avoid path errors
import sys
sys.path.append(r"C:\Users\vince\AppData\Local\Programs\Python\Python37\Lib\site-packages")

print("yuh")

#importing dependencies
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("aiyaaaa")

from tensorflow.keras import layers

#prepping data for training
splits = tfds.Split.ALL.subsplit(weighted=(75,25))
splits, info = tfds.load('food101', with_info=True, split=splits)
(train_ex,test_ex) = splits
num_examples = info.splits['train'].num_examples

#defining the input resolution for the model and batch size
RES = 224
BATCH_SIZE = 100

def formatImage(image, label):
    #reformatting images so that the model can accept them in first layer
    image = tf.image.resize(image, (RES,RES))/255
    return image, label

train_batches = train_ex.cache().shuffle(num_examples//4).map(formatImage).batch(BATCH_SIZE).prefetch(1)
test_batches = test_ex.cache().map(formatImage).batch(BATCH_SIZE).prefetch(1)

#fetching the URL to use transfer learning 
modelURL = "https://tfhub.dev/google/imagenet/inception_resnet_v2/classification/4"

#setting up the base model (RESNET)
baseModel = hub.KerasLayer([modelURL, input_shape=(RES,RES,3)])
baseModel.trainable=False
#creating the model that will be used for image recognition
model = tf.keras.layers.Sequential([
    baseModel,
    tf.keras.layer.Dense(101, activation=tf.softmax)
])

SAMPLE_NUM = 101000

model.compile(optimizer='adam',loss='root_mean_squared',metrics=['accuracy'])
model.fit(train_batches,epochs=12,steps_per_epoch=match.ceil(SAMPLE_NUM/BATCH_SIZE))
model.evaluate(test_batches,steps.ceil(SAMPLE_NUM/BATCH_SIZE))    

#saving the model
str t = time.time()
model_name = "krabby_patty_vision"
model_name_sm = model_name + t 
model.save(model_name)
tf.saved_model.save(model_name,)
tf.saved_model.save(model_name, model_name_sm)



print("yes")