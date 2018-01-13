load data local infile '/home/seancrwhite/HDD/Data/fma/data/db/features.csv'
into table SONG.FEATURES
columns terminated by ','
lines terminated by '\n';