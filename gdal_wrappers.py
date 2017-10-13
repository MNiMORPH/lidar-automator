#--------------------------------------------------------------#
# Functions for merging rasters with gdal
# FJC 09/10/17
#--------------------------------------------------------------#
import os

def GetESRIFileNamesNextMap(DataDirectory):
    """
    This function takes in a data directory which has some ESRI rasters
    in it and gets a list of all the rasters - this can then be used with
    gdal_merge.py to merge the tiles into a seamless DEM.
    The command would be:
        gdal_merge.py -of ENVI -o Merged_DEM.bil --optfile DEM_list.txt

    Args:
        DataDirectory(str): the directory with the ESRI rasters in it.

    Author: FJC
    """

    file_list = []
    print "The data directory is: " + DataDirectory

    for dirs,subdirs,files in os.walk(DataDirectory):
        for fname in files:
            if '0' in fname:
                #print fname
                if not 'x' in fname:
                    print fname
                    file_list.append(fname+"\n")

    # write the new version of the file
    file_for_output = open(DataDirectory+"DEM_list.txt",'w')
    file_for_output.writelines(file_list)
    file_for_output.close()

if __name__ == "__main__":

    DataDirectory = '/media/fionaclubb/Seagate Backup Plus Drive/LIDAR0/Illinois/illinois_river/illinois_dem'
    GetESRIFileNamesNextMap(DataDirectory)
