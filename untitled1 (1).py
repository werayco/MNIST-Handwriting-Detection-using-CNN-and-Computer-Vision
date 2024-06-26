# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DMeyT6XS40HDJqNICYlu4o-WPpxkyQ_3
"""

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json


!kaggle competitions download -c digit-recognizer

from zipfile import ZipFile

with ZipFile('/content/digit-recognizer.zip', 'r') as zip:
    zip.extractall()

!pip install tensorflow

import pandas as pd
import gensim
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential

# reading the dataframe
data = pd.read_csv("/content/train.csv")

train_dat,test_dat=train_test_split(data,random_state=59,train_size=0.6)

x_train,y_train = train_dat.iloc[:,1:],train_dat.iloc[:,0]

x_test,y_test = test_dat.iloc[:,1:],test_dat.iloc[:,0]



column_to_drop = x_test.columns[63]
print(f"x_test: {x_test.shape}, y_test:{y_test.shape}")
print(f"x_train: {x_train.shape},y_train:{y_train.shape}")

# normalizing our data
x_train_scaled = x_train/255
x_test_scaled = x_test/255

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.regularizers import l2

# Define the model
# model = Sequential()
# model.add(Dense(256, activation='relu', input_shape=(784,)))
# model.add(Dropout(0.5))
# model.add(Dense(128, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(10, activation='softmax'))

model = Sequential()
model.add(Dense(256, activation='relu', input_shape=(784,), kernel_regularizer=l2(0.001)))
model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.001)))
model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.001)))
model.add(Dense(10, activation='softmax', kernel_regularizer=l2(0.001)))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# One-hot encode the labels
y_train_encoded = to_categorical(y_train, num_classes=10)
y_val_encoded = to_categorical(y_test, num_classes=10)

early_stopping = EarlyStopping(patience=5, restore_best_weights=True)

# Fit the model
history = model.fit(x_train_scaled, y_train_encoded, epochs=5, batch_size=32,validation_split=0.2)

history.history

y_test_encoded = to_categorical(y_test,num_classes=10)

loss, accuracy = model.evaluate(x_test_scaled, y_test_encoded)

print(f"Loss: {loss}, Accuracy: {accuracy}")

# print(f"x_test: {x_test_scaled.shape}, y_test:{y_test.shape}")

import matplotlib.pyplot as plt

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.legend(["accuracy","val_accuracy"])
plt.show()
plt.savefig("ROC.png")

import json

metrics = {"CNN_Accuracy":  0.945684552192688 }

with open("metrics.json","w") as JsonMetric:

  json.dump(metrics, JsonMetric)

model.save("MNIST_Model.h5")