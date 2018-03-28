from keras.models import model_from_json


def init():
    with open('model.json', 'r') as model_json:
        loaded_model = model_json.read()

    model = model_from_json(loaded_model)
    model.load_weights('model.h5')

    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])

    return model
