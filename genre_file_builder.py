# Sean White, January 2018
# Creates a CSV containing the song id and associated
# genres of each song taken from the FMA dataset

from csv import reader, writer

output = writer(open('data/db/genres.csv', 'w'))
genres = reader(open('data/fma_metadata/genres.csv', 'r'))
tracks = reader(open('data/fma_metadata/tracks.csv', 'r'))

key = []
parent_genre = {}

# Skip first line
next(genres)

for genre in genres:
    id = int(genre[0])
    parent = int(genre[4])

    parent_genre[id] = parent

    if int(genre[2]) == 0:
        key.append(id)

# Skip first 3 lines
next(tracks)
next(tracks)
next(tracks)

for track in tracks:
    s_id = int(track[0])
    g_ids = [int(x) for x in track[42].lstrip('[').rstrip(']').split(', ') if x.isdigit()]

    g_id_parents = []
    track_genres = [s_id]

    for g_id in g_ids:
        g_id_parent = parent_genre[g_id]
        if g_id_parent not in g_id_parents:
            g_id_parents.append(g_id_parent)

    for x in key:
        if x in g_id_parents:
            genre_present = 1
        else:
            genre_present = 0

        track_genres.append(genre_present)

    output.writerow(track_genres)