# Imports
import numpy as np
import mysql.connector as dbc
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.backend import clear_session
from keras.layers.normalization import BatchNormalization
from keras.layers.recurrent import GRU
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, ZeroPadding2D, Reshape, ELU, Flatten

clear_session()

# Get MFCC data
datapath = '/home/seancrwhite/HDD/Data/fma/data/db/melgrams.csv'

data = np.loadtxt(datapath, delimiter=',') # shape=(327270400, 1291)

print("Loaded Data ", data.shape)

ids = np.reshape(data[:, 0], (1, 327270400))
data = np.reshape(data[:, 1:], (2556800, 128, 1290, 1))

print("Reshaped Data")

# Clean ids
u_ids = []
i = 0

for s_id in ids[0]:
    if i % 128 == 0:
        u_ids.append(int(s_id))
    i = i + 1

del ids

print("Created set of unique ids")

# Get corresponding genres from DB
db = dbc.connect(port=3306,
                 user="root",
                 passwd="password",
                 db="SONG")
cursor = db.cursor()

labels = []
idxs = []

for s_id in u_ids:
    query = "select * from SONG.GENRES where s_id={}".format(s_id)
    cursor.execute(query)

    row = cursor.fetchone()

    if row is None:
        idxs.append(u_ids.index(s_id))
    else:
        labels.append(row)

labels = np.array(labels)
labels = labels[:, 1:]

db.close()

# print("Fetched Labels")
# with open('labels.csv', 'wb') as output:
#     np.savetxt(output, labels, delimiter=',', fmt='%.18e')
#
# with open('idxs.csv', 'wb') as output:
#     np.savetxt(output, idxs, delimiter=',', fmt='%.18e')

print("Data Shape  ", data.shape)
print("Labels Shape", labels.shape)

# Remove unlabeled data points
idxs = sorted(idxs, reverse=True)

for idx in idxs:
    data = np.delete(data, idx, 0)

del idxs

print("Removed unlabeled data")

# Split test and train data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.5, random_state=73)

del data, labels

# Build model
model = Sequential()

###### CNN  #######

model.add(BatchNormalization(axis=1, input_shape=(128, 1290, 1), name='input'))

model.add(Conv2D(32, (3, 3), name='conv1'))
model.add(BatchNormalization(axis=3))
model.add(ELU(alpha=1.0))
model.add(MaxPooling2D(pool_size=(2, 4), name='pool1'))

model.add(Conv2D(32, (3, 3), name='conv2'))
model.add(BatchNormalization(axis=3))
model.add(ELU(alpha=1.0))
model.add(MaxPooling2D(pool_size=(3, 4), name='pool2'))

model.add(Conv2D(32, (3, 3), name='conv3'))
model.add(BatchNormalization(axis=3))
model.add(ELU(alpha=1.0))
model.add(MaxPooling2D(pool_size=(2, 5), name='pool3'))

model.add(Conv2D(32, (3, 3), name='conv4'))
model.add(BatchNormalization(axis=3))
model.add(ELU(alpha=1.0))
model.add(MaxPooling2D(pool_size=(2, 4), name='pool4'))

model.add(Conv2D(32, (3, 3), activation='elu', name='conv5'))
model.add(BatchNormalization(axis=3))
model.add(ELU(alpha=1.0))
model.add(MaxPooling2D(pool_size=(1, 1), name='pool5'))

model.add(Flatten())
model.add(Dense(16, activation='sigmoid', name='output'))

###### CRNN #######

# model.add(ZeroPadding2D(padding=(0, 37), input_shape=(1000, 100, 1), name='input'))
# model.add(BatchNormalization(axis=1))
#
# model.add(Conv2D(64, (3, 3), activation='elu', padding='same', name='conv1'))
# model.add(BatchNormalization(axis=3))
# model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='pool1'))
# model.add(Dropout(0.1))
#
# model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv2'))
# model.add(BatchNormalization(axis=3))
# model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3), name='pool2'))
# model.add(Dropout(0.1))
#
# model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv3'))
# model.add(BatchNormalization(axis=3))
# model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), name='pool3'))
# model.add(Dropout(0.1))
#
# model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv4'))
# model.add(BatchNormalization(axis=3))
# model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), name='pool4'))
# model.add(Dropout(0.1))
#
# model.add(Reshape((10, 128)))
#
# model.add(GRU(32, return_sequences=True))
# model.add(GRU(32))
#
# model.add(Dense(16, activation='softmax', name='output'))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

# Train model, print accuracy
model.fit(X_train, y_train, epochs=3)

# score_train = model.evaluate(X_train, y_train)
score_test = model.evaluate(X_test, y_test)

# print("Training Data Accuracy: {}".format(score_train[1]))
print("Test Data Accuracy: {}".format(score_test[1]))

del model
del X_train, X_test, y_train, y_test
clear_session()
