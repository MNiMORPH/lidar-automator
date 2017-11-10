#!/usr/bin/env python

# import modules
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import general as g
import pandas as pd
import os

# read in the csv with the reaches
DataDirectory = '/media/fionaclubb/terrace_lidar/DEMs_for_analysis/'
input_csv = 'Miss_reaches.csv'
reaches_df = pd.read_csv(DataDirectory+input_csv)

# now get the data
reaches = reaches_df['Reach_no']
n = reaches_df['N']
s = reaches_df['S']
e = reaches_df['E']
w = reaches_df['W']

for i, reach_no in enumerate(reaches):
    # make the directory for this reach
    this_dir = DataDirectory+'Upper_Miss_reach'+str(reach_no)+'/'
    os.mkdir(this_dir)

    # set the region
    g.region(n=n[i],s=s[i],e=e[i],w=w[i])

    # now output the ENVI bil file
    r.out.gdal(input=Upper_Miss_filled, format=ENVI, type=Float32, nodata=-9999, output=this_dir+'Upper_Miss_reach'+str(reach_no)+'.bil')
