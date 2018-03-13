from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.recurrent import GRU
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, ZeroPadding2D, Reshape


class CRNN:
    def build_model(self):
        model = Sequential()

        model.add(ZeroPadding2D(padding=(0, 37), input_shape=(1000, 100, 1), name='input'))
        model.add(BatchNormalization(axis=1))

        model.add(Conv2D(64, (3, 3), activation='elu', padding='same', name='conv1'))
        model.add(BatchNormalization(axis=3))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='pool1'))
        model.add(Dropout(0.1))

        model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv2'))
        model.add(BatchNormalization(axis=3))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3), name='pool2'))
        model.add(Dropout(0.1))

        model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv3'))
        model.add(BatchNormalization(axis=3))
        model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), name='pool3'))
        model.add(Dropout(0.1))

        model.add(Conv2D(128, (3, 3), activation='elu', padding='same', name='conv4'))
        model.add(BatchNormalization(axis=3))
        model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4), name='pool4'))
        model.add(Dropout(0.1))

        model.add(Reshape((10, 128)))

        model.add(GRU(32, return_sequences=True))
        model.add(GRU(32))

        model.add(Dense(16, activation='softmax', name='output'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])

        return model