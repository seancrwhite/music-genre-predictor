import os
import sys
import numpy as np
sys.path.append(os.path.abspath('./model'))
from load import init
from flask import Flask, request, jsonify

# init app
app = Flask(__name__)

# Get model
global model
model = init()


def format_data(data):
    m, n, length = 128, 1290, data.shape[0]

    assert length % m == 0

    num_clips = int((length / m) // n)

    data = np.reshape(data, (m, int(length / m)))
    data = np.reshape(data[:, :int(n * num_clips)], (num_clips, 1, m, n, 1))

    return data


def make_json(result):
    response = {}

    response['International'] = '%.5f' % result[0]
    response['Blues'] = '%.5f' % result[1]
    response['jazz'] = '%.5f' % result[2]
    response['Classical'] = '%.5f' % result[3]
    response['Historic'] = '%.5f' % result[4]
    response['Country'] = '%.5f' % result[5]
    response['Pop'] = '%.5f' % result[6]
    response['Rock'] = '%.5f' % result[7]
    response['Easy Listening'] = '%.5f' % result[8]
    response['Soul R&B'] = '%.5f' % result[9]
    response['Electronic'] = '%.5f' % result[10]
    response['Folk'] = '%.5f' % result[11]
    response['Spoken Word'] = '%.5f' % result[12]
    response['Hip Hop'] = '%.5f' % result[13]
    response['Experimental'] = '%.5f' % result[14]
    response['Instrumental'] = '%.5f' % result[15]

    return jsonify(response)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Get audio data from request
    audio = request.get_data()

    # Format data for model
    data = format_data(np.frombuffer(audio, dtype=np.float32))

    # Make prediction
    results = []

    for clip in data:
        result = model.predict(clip)
        results.append(result)

    result = np.sum(np.array(results), axis=0)
    result = result/result.sum(axis=1)

    response = make_json(result[0])

    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
