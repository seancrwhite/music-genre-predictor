# Sean White, December 2017
# Creates a CSV containing the MFCCs and song id of each song taken from
# the FMA dataset, methods used here outlined in feature_extraction.ipynb

from os import scandir, listdir

from audioread import NoBackendError
from librosa import feature, load
from numpy import savetxt, insert

with open('data/db/features.csv', 'wb') as output:
    # Extract MFCCs from each song in fma_large directory,
    # place them in a csv stored locally
    with scandir('data/fma_large') as directory:
        for folder in directory:
            for song in listdir(folder.path):
                s_id = song.lstrip('0').rstrip('.mp3')
                try:
                    X, sr = load('{}/{}'.format(folder.path, song))
                    mfcc = feature.mfcc(X, sr, n_mfcc=10).T

                    mfcc = insert(mfcc, 0, s_id, axis=1)

                    savetxt(output, mfcc, delimiter=',', fmt='%.18e')
                except (NoBackendError, ValueError) as e:
                    print('{}: {}'.format(type(e).__name__, s_id))
