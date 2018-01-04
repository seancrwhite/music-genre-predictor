load data local infile '/home/seancrwhite/HDD/Data/fma/data/db/genres.csv'
into table SONG.GENRES
columns terminated by ','
lines terminated by '\n';