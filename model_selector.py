import csv

with open('data/db/features.csv', 'wb') as output:
    with open('data/db/features_full.csv', 'rb') as input:
        i = 0
        writer = csv.writer(output)

        for row in input:
            if i % 100 == 0:
                writer.writerow(row)

            i += 1
            