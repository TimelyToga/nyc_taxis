import csv, sys
filename = 'data/yellow_tripdata_2016-01.csv'
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	print row
