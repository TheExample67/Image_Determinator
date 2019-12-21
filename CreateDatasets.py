# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
import random
import pickle
import json

DATADIR = "data"
SOURCEDIR = "source"
CATEGORIES = []
training_data = []
IMG_SIZE = 50
plotStuff = False


CATEGORIES = [dI for dI in os.listdir(SOURCEDIR) if os.path.isdir(os.path.join(SOURCEDIR,dI))]

print("Loading Categories..")
def create_training_data():
    for category in CATEGORIES:  # do dogs and cats

        path = os.path.join(SOURCEDIR,category)  # create path to dogs and cats
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat

        for img in tqdm(os.listdir(path)):  # iterate over each image per dogs and cats
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass

create_training_data()

#Switch around the data
random.shuffle(training_data)

X = []
y = []

for features,label in training_data:
    X.append(features)
    y.append(label)

print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 1))

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open("{0}\X.pickle".format(DATADIR),"wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("{0}\Y.pickle".format(DATADIR),"wb")
pickle.dump(y, pickle_out)
pickle_out.close()

