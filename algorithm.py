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

training_set = []
y_train = []

# load the images 
for i in range(3): #change to number of images
    img = load_img(str(i+1))
    array = keras.preprocessing.image.img_to_array(img)
    array = cv2.resize(array, dsize=(299,299))
    array = np.expand_dims(array, axis = 0)
    array = array/255 #or preprocess(array)
    if i == 0:
        training_set = array
    else:
        training_set = np.concatenate((training_set, array), axis = 0)

#training_set = K.variable(training_set)

#load y values
with open('percentages.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = '\n')
    for row in csv_reader:
        y_train.append(float(row[0]))

y_train = np.array(y_train).reshape(3,1)

#define network with custom inputs
input_tensor = Input(shape = (299,299,3))
base_model = InceptionResNetV2(input_tensor = input_tensor, weights = None, include_top = False)

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1)(x) #linear activation

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics= [metrics.RootMeanSquaredError()])
model.fit(x = training_set, y = y_train, epochs = 5)

#save network
model.save_weights("stockx_model")


