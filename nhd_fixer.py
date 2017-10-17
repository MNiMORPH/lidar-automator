"""
Function to read in a shapefile of channels from the National Hydrography dataset
and filter it down to a specific river that you want (e.g. the Mississippi)

Info on NHD:
https://nhd.usgs.gov/NHD_High_Resolution.html

FJC
13/10/17
"""

import fiona

def filter_shapefile(DataDirectory, shapefile, string):
    """
    This function reads through the shapefile and selects only the rivers
    with the specific name defined by the string
    """

    print("Loading the shapefile...")
    split_fname = string.split(" ")
    output_shp = 'NHD_'+split_fname[0]+'.shp'
    with fiona.open(DataDirectory+shapefile) as input:
        schema = input.schema
        with fiona.open(DataDirectory+output_shp, 'w',driver=input.driver, crs=input.crs,schema=schema) as output:
            for multi in input:
                #print multi
                chan_name = multi['properties']['GNIS_NAME']
                if chan_name == string:
                    output.write(multi)

    print("Done!")


if __name__ == '__main__':

    DataDirectory = '/home/s0923330/MN_postdoc/Mississippi_terraces/National_Hydrography_Dataset/Minnesota/Shape/'
    shapefile = 'NHDFlowline.shp'
    river_name = 'Mississippi River'
    filter_shapefile(DataDirectory,shapefile,river_name)
