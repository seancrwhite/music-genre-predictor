import numpy as np
from CNN import CNN
from CRNN import CRNN
import mysql.connector as dbc

cnn = CNN()
crnn = CRNN()

num_files = 20

db = dbc.connect(port=3306,
                 user="root",
                 passwd="password",
                 db="SONG")
cursor = db.cursor()

# Change this to switch model
model = cnn.build_model()

for idx in range(num_files):
    datapath = '/home/seancrwhite/HDD/Data/fma/data/db/melgrams%d.csv'%idx

    # Load and reshape data
    data = np.loadtxt(datapath, delimiter=',')

    m, n = data.shape

    ids = np.reshape(data[:, 0], (1, m))
    data = np.reshape(data[:, 1:], (int(m/128), 128, 1290, 1))

    print("Loaded Data %d"%idx)

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

    print("Fetched labels")

    # Remove unlabeled data points
    idxs = sorted(idxs, reverse=True)

    for idx in idxs:
        data = np.delete(data, idx, 0)

    del idxs
    # Train model, print accuracy
    model.fit(data, labels, epochs=12)

# Save weight file and architecture to JSON for deployment
model_json = model.to_json()
with open('model/model.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights("model/model.h5")

db.close()
del model