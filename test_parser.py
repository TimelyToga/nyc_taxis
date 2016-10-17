import csv, sys
import calendar
from geohash import encode
from datetime import datetime

big_file = 'data/yellow_tripdata_2016-01.csv'
example_file = 'yellow_tripdata_example.csv'

output_file = 'geography.csv' # Come up with another name

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# lat = 40.67956543
# long_coord = -73.98455048
#
# my_geohash = encode(lat, long_coord)
#
# print my_geohash

with open(example_file, 'rb') as f:
    with open(output_file, 'w') as of:
        reader = csv.reader(f)
        writer = csv.writer(of, delimiter=',')
        for row in reader:
            try:
                start_time = datetime.strptime(row[1], DATE_FORMAT)
                start_time_utc = calendar.timegm(start_time.utctimetuple())

                pickup_gh = encode(float(row[6]), float(row[5]))
                if not pickup_gh.startswith("dr"):
                    continue

                dropoff_gh = encode(float(row[10]), float(row[9]))
                if not dropoff_gh.startswith("dr"):
                    continue


                writer.writerow([start_time_utc, pickup_gh, dropoff_gh])

                print("START: {}, END: {}".format(pickup_gh, dropoff_gh))
            except Exception as exc:
                # Make sure that the data in the lat / long columns are floats
                print exc
                continue
