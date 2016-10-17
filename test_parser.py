import csv, sys
from geohash import encode
big_file = 'data/yellow_tripdata_2016-01.csv'
example_file = 'yellow_tripdata_example.csv'

# lat = 40.67956543
# long_coord = -73.98455048
#
# my_geohash = encode(lat, long_coord)
#
# print my_geohash

with open(big_file, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            pickup_gh = encode(float(row[6]), float(row[5]))
            if not pickup_gh.startswith("dr"):
                continue

            dropoff_gh = encode(float(row[10]), float(row[9]))
            if not dropoff_gh.startswith("dr"):
                continue

            print("START: {}, END: {}".format(pickup_gh, dropoff_gh))
        except Exception:
            # Make sure that the data in the lat / long columns are floats
            continue
