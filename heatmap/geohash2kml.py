#!/usr/bin/env pythonG
# -*- coding: utf-8 -*-
import sys
import math

reload(sys)
sys.setdefaultencoding("utf-8")
import geohash
from kml_template import header, footer, box_template, red_template, orange_template, yellow_template, green_template

OUTPUT_TYPES = ['num_rides', 'ride_distance']

NR_COLORS = [4,7,13]
NR_PHEIGHT = 600

RD_COLORS = [2, 2.5, 3.3]
RD_PHEIGHT = 1300

class KmlMaker(object):
    def __init__(self,filename):
        self.filename = filename
        print "walking",filename
        self.locations = {}

    def makeGoogleEarthBox(self,geo):
        bbox = geohash.bbox(geo)
        lowerleft = "%s,%s,elevation"%(bbox['w'],bbox['s'])
        upperleft = "%s,%s,elevation"%(bbox['w'],bbox['n'])
        lowerright = "%s,%s,elevation"%(bbox['e'],bbox['s'])
        upperright = "%s,%s,elevation"%(bbox['e'],bbox['n'])
        polygon = "%s %s %s %s %s"%(lowerleft,upperleft,upperright,lowerright,lowerleft)
        return polygon

    def loadLocations(self):
        counts = {}
        for line in open(self.filename,"rU"):
            (geohashcode, count) = line.strip().split(",")
            self.locations[geohashcode] = math.log(float(count)) / math.log(2)
        print 'Done loading geohashcode counts.'

    def get_template(self,input_value,color_ramp=[2,3,5]):
        low = color_ramp[0]
        medium = color_ramp[1]
        high = color_ramp[2]
        template = box_template
        if input_value < low:
            template = green_template
        elif input_value < medium:
            template = yellow_template
        elif input_value < high:
            template = orange_template
        else:
            template = red_template
        return template


    def simple_kml_output(self,title='Location Indicators',output_filename ='output_simple.kml' ):
        f = open(output_filename,"w")
        header2 = header.replace('__title__',title)
        f.write(header2)
        for key,value in self.locations.items():
            value = int(value)
            if value < 1: continue
            print key,value
            t = box_template
            poly = self.makeGoogleEarthBox(key)
            #TODO: remove this constraint for visualization
            if value > 40:
                value = 40
            height = value * 600
            height = str(height)
            poly = poly.replace("elevation",height)
            t = t.replace("__name__",key)
            t = t.replace("__coordinates__",poly)
            f.write(t+"\n")
        f.write(footer)

    def advanced_kml_output(self,title='Location Indicators',output_filename ='output_advanced.kml',color_ramp=[1,500,1000],polygon_height=1000):
        f = open(output_filename,"w")
        header2 = header.replace('__title__',title)
        f.write(header2)
        for key,value in self.locations.items():
            value = int(value)
            if value < 1: continue
            print key,value
            t = self.get_template(value,color_ramp=color_ramp)
            poly = self.makeGoogleEarthBox(key)
            #TODO: remove this constraint for visualization
            if value > 50000:
                value = 50000
            height = value * polygon_height
            height = str(height)
            poly = poly.replace("elevation",height)
            t = t.replace("__name__",key)
            t = t.replace("__coordinates__",poly)
            t = t.replace('__title__',title)
            f.write(t+"\n")
        f.write(footer)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: python geohash2kml.py <mode> <input file> <output file>"
        sys.exit(-1)
    
    output_type = sys.argv[1]
    if output_type not in OUTPUT_TYPES:
        print "Please select one of the following modes: {}".format(OUTPUT_TYPES)
        sys.exit(1)

    # Collect file arguments
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # Create helper object
    kml = KmlMaker(input_file)
    kml.loadLocations()
    
    # Retrieve correct settings for current mode
    cur_color_ramp = []
    pheight = 1
    if output_type == OUTPUT_TYPES[0]:
        cur_color_ramp = NR_COLORS
        pheight = NR_PHEIGHT
    elif output_type == OUTPUT_TYPES[1]:
        cur_color_ramp = RD_COLORS
        pheight = RD_PHEIGHT
    else:
        print "Something went very very wrong"
        sys.exit(1)
    
    # Generate the KML
    kml.advanced_kml_output(output_filename=output_file, color_ramp=cur_color_ramp, polygon_height=pheight)
