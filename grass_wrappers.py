#!/usr/bin/env python

# import modules
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import vector as v
import os
import pandas as pd

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
    try:
        os.mkdir(this_dir)
    except:
        pass

    # set the region
    g.region(n=str(n[i]),s=str(s[i]),e=str(e[i]),w=str(w[i]), flags='p')

    # now output the ENVI bil file
    r.out_gdal(input="Upper_Miss_filled", format="ENVI", type="Float32", nodata=-9999, output=this_dir+'Upper_Miss_reach'+str(reach_no)+'.bil')

    # clip the baseline to this region
    v.in_region(output='region_tmp', overwrite=True)
    v.overlay(ainput='Mississippi_River', atype='line', binput='region_tmp', output='Mississippi_River_clip_tmp', operator='and', overwrite=True)
    v.out_ogr(input='Mississippi_River_clip_tmp', output=this_dir+'Upper_Miss_baseline_reach'+str(reach_no)+".shp", overwrite=True)
