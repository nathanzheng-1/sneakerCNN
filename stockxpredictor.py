import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing.image import load_img
from keras.applications.imagenet_utils import preprocess_input
import csv
import cv2
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras import metrics
from keras.layers import Input

def premade_Model():
    input_tensor = Input(shape = (299,299,3))
    base_model = InceptionResNetV2(input_tensor = input_tensor, weights = None, include_top = False)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(1)(x) #linear activation
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics= [metrics.RootMeanSquaredError()])
    return model

final_model = premade_Model()
final_model.load_weights("stockx_model")

#load in picture
img = load_img("1") #replace with name
array = keras.preprocessing.image.img_to_array(img)
array = cv2.resize(array, dsize=(299,299))
array = np.expand_dims(array, axis = 0)
array = array/255 #or preprocess(array)
#array = K.variable(array)

print(final_model.predict(array))
