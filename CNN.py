from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Dense, ELU, Flatten



class CNN:
    def build_model(self):
        model = Sequential()

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

        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])

        return model