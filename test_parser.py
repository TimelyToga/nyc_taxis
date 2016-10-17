import csv, sys
from geohash import encode
filename = 'data/yellow_tripdata_2016-01.csv'

lat = 40.67956543
long_coord = -73.98455048

my_geohash = encode(lat, long_coord)

print my_geohash

# with open(filename, 'rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#     	print row
