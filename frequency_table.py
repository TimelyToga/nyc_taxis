import csv, sys, os
import calendar
import pandas as pd
import numpy as np


input_file = 'geography.csv'
output_file = 'frequency_table_locations.csv'
string_length = 6; #original length 12
domain = "PICKUP_GEOHASH"
# domain1 = "DROPOFF_GEOHASH"

fre_table = pd.read_csv(input_file)

# trim the domain to be of the length as user setting
if string_length <> 12:
    string_list = fre_table[domain]
    new_list = np.array([item[0:string_length] for item in string_list])
    fre_table[domain] = pd.Categorical(new_list)

# create frequency table and sort by frequency
my_tab = pd.crosstab(index = fre_table[domain],columns = "count")
my_tab = my_tab.sort(["count"], ascending = False)
my_tab.to_csv(output_file)
print(my_tab)
