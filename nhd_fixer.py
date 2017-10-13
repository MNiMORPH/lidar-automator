"""
Function to read in a shapefile of channels from the National Hydrography dataset
and filter it down to a specific river that you want (e.g. the Mississippi)

Info on NHD:
https://nhd.usgs.gov/NHD_High_Resolution.html

FJC
13/10/17
"""

import fiona
from shapely.geometry import shape, mapping

def filter_shapefile(DataDirectory, shapefile, string):
    """
    This function reads through the shapefile and selects only the rivers
    with the specific name defined by the string
    """

    lines = []
    with fiona.open(DataDirectory+shapefile) as input:
        for multi in input:
            #print multi
            chan_name = multi['properties']['GNIS_NAME']
            print chan_name
            if chan_name == string:
                lines.append(multi.geometries)
            # this_output_name = 'catchment_'+str(catchment_id)+'.shp'
            # with fiona.open(DataDirectory+this_output_name, 'w', driver=input.driver, crs=input.crs,schema=input.schema) as output:
            #     output.write({'properties': multi['properties'], 'geometry': mapping(shape(multi['geometry']))})


if __name__ == '__main__':

    DataDirectory = '/media/fionaclubb/Seagate Backup Plus Drive/Shapefiles/National_Hydrography_Dataset/Minnesota/Shape/'
    shapefile = 'NHDFlowline.shp'
    river_name = 'Mississippi River'
    filter_shapefile(DataDirectory,shapefile,river_name)
