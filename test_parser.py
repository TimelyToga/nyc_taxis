import csv, sys
import calendar
from geohash import encode
from datetime import datetime

big_file = 'data/yellow_tripdata_2016-01.csv'
example_file = 'yellow_tripdata_example.csv'

output_file = 'geography.csv' # Come up with another name

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
PRECISION = 6
FULL_PRECISION = 12

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
        writer.writerow(["PICKUP_TIME", "ELAPSED_RIDE_TIME", "PICKUP_GEOHASH12", "PICKUP_GEOHASH6" "DROPOFF_GEOHASH12", "DROPOFF_GEOHASH6", "RIDE_DISTANCE"])
        for row in reader:
            try:
                start_time = datetime.strptime(row[1], DATE_FORMAT)
                end_time = datetime.strptime(row[2], DATE_FORMAT)

                elapsed_time = end_time - start_time
                start_time_utc = calendar.timegm(start_time.utctimetuple())
                drive_dis = float(row[4])

                pickup_gh6 = encode(float(row[6]), float(row[5]), precision=PRECISION)
                pickup_gh = encode(float(row[6]), float(row[5]), precision=FULL_PRECISION)
                if not pickup_gh.startswith("dr"):
                    continue

                dropoff_gh6 = encode(float(row[10]), float(row[9]), precision=PRECISION)
                dropoff_gh = encode(float(row[10]), float(row[9]), precision=FULL_PRECISION)

                if not dropoff_gh.startswith("dr"):
                    continue

                output_row = [start_time_utc, elapsed_time.seconds, pickup_gh, pickup_gh6, dropoff_gh, dropoff_gh6, drive_dis]
                writer.writerow(output_row)

                print(output_row)

            except Exception as exc:
                # Make sure that the data in the lat / long columns are floats
                print exc
                continue
