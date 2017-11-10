#---------------------------------------------------------------------#
# Functions for automating the processing of lidar data.
# FJC (stolen and modified from a script that Stuart wrote)
# 04/10/17
#---------------------------------------------------------------------#
import math
from glob import glob
import os, os.path
import sys

def LAStoGRID(DataDirectory, Cores, UTMZone, Resolution, Hillshade=False):
    """
    Generate the bash files for filtering, gridding, and translating.
    This script generates a series of bash scripts that can be used to
    transform a series of .las files into DTMs.
    Firstly, I use PDAL to classify the las files and filter so we only
    have ground returns, based on a PDAL tutorial:
    https://www.pdal.io/tutorial/pcl_ground.html
    Then I use points2grid to grid the ground returns into a DTM:
    https://github.com/CRREL/points2grid
    Finally, some good old gdal to translate to ENVI bil and fill no data
    holes in the raster.

    Args:
        DataDirectory (str): the directory to look for the las files
        Cores (int): number of cores you want to run it on (=n bash scripts)
        UTMZone (str): the UTM zone that you want to convert the data to
        Resolution (str): the grid resolution you want
        Hillshade (bool): if true, hillshade the DEMs. default = false

    Returns: 3 bash scripts which can be run in sequence to filter, grid,
    and prepare your data.

    Author: FJC
    """

    # get total number of files
    n_files =  len([name for name in os.listdir(DataDirectory) if '.las' in name])
    print n_files

    for n in range(Cores):

        with open(DataDirectory+'pdal_Script' + str(n)+'.sh', 'w') as pdal, \
                open(DataDirectory+'p2g_Script' + str(n)+'.sh', 'w') as p2g, \
                    open(DataDirectory+'gdal_Script' + str(n)+'.sh', 'w') as gdal:
            print '\n Writing to pdal_Script' + str(n)+'.sh'
            print '\n Writing to p2g_Script' + str(n)+'.sh'
            print '\n Writing to gdal_Script' + str(n)+'.sh'

            # write the shebangs for the scripts\
            pdal.write('#!/bin/bash\n')
            p2g.write('#!/bin/bash\n')
            gdal.write('#!/bin/bash\n')

            # get each las file in the directory
            for FileName in glob(DataDirectory+"*.las")[n::Cores]:
                if not "ground" in FileName:
                    print "filename is: " + FileName

                    # get the name of the LAS file
                    split_fname = FileName.split('/')
                    split_fname = split_fname[-1]

                    # remove LAS extension from filename
                    fname_noext = split_fname.split('.')
                    fname_noext = fname_noext[0]

                    pdal_str = ('pdal pcl -i %s -o %s -p classify.json' % (split_fname, fname_noext+'_ground.las'))

                    SearchRadius = str(int(math.ceil(float(Resolution) * math.sqrt(2))))
                    Resolution = str(Resolution)

                    p2g_str = ('points2grid -i %s -o %s --idw --fill_window_size=7 '
                               '--output_format=arc --resolution=%s -r %s'
                               % (fname_noext+'_ground.las', fname_noext+"_"+Resolution+"m", Resolution, SearchRadius))

                    gdal_str = ("gdalwarp -t_srs \'+proj=utm +zone=%s "
                                "+datum=WGS84\' -r cubic -of ENVI -dstnodata -9999 -ot Float32 %s.idw.asc %s_DEM.bil"
                                % (UTMZone, fname_noext+"_"+Resolution+"m", fname_noext+"_"+Resolution+"m"))

                    fill_str = ("gdal_fillnodata.py -md 20 -si 1 %s_DEM.bil" % (fname_noext+"_"+Resolution+"m"))

                    del_str = ('rm %s.idw.asc\n' % (fname_noext+"_"+Resolution+"m"))

                    # write the commands to the 2 scripts
                    pdal.write('nice ' + pdal_str + '\n')
                    p2g.write('nice ' + p2g_str + '\n')
                    gdal.write('nice ' + gdal_str + '\n')
                    gdal.write('nice ' + fill_str + '\n')
                    gdal.write(del_str)
                    if Hillshade:
                        hs_str = ('gdaldem hillshade -of ENVI '
                                  '%s_DEM.bil %s_HS.bil\n'
                                  % (fname_noext, fname_noext))
                        gdal.write(hs_str)

    print '\tScripts successfully written.'

def gdalScripter(DataDirectory, Cores, UTMZone, Resolution, InputType='tif', Hillshade=False):
    """
    Similar to p2gScripter above but only generates the bash script for using
    gdal to translate the files to ENVI and projecting to UTM WGS84

    Args:
        DataDirectory (str): the directory to look for the las files
        Cores (int): number of cores you want to run it on (=n bash scripts)
        UTMZone (str): the UTM zone that you want to convert the data to
        Resolution (str): the grid resolution you want
        InputType (str): the input format of the data, default = 'tif'
        Hillshade (bool): if true, hillshade the DEMs. default = false

    Returns: Bash script to translate the data to an lsdtopotools friendly format

    Author: FJC
    """
    # get total number of files
    n_files =  len([name for name in os.listdir(DataDirectory) if name.endswith(InputType)])
    print n_files

    for n in range(Cores):

        with open(DataDirectory+'gdal_Script' + str(n)+'.sh', 'w') as gdal:
            print '\n Writing to gdal_Script' + str(n)+'.sh'

            # write the shebangs for the scripts\
            gdal.write('#!/bin/bash\n')

            # get each las file in the directory
            for FileName in glob(DataDirectory+"*."+InputType)[n::Cores]:
                print "filename is: " + FileName

                # get the name of the file
                split_fname = FileName.split('/')
                split_fname = split_fname[-1]

                # remove extension from filename
                fname_noext = split_fname.split('.')
                fname_noext = fname_noext[0]

                gdal_str = ("gdalwarp -t_srs \'+proj=utm +zone=%s "
                            "+datum=WGS84\' -r cubic -of ENVI -tr %s %s -dstnodata -9999 -ot Float32 %s %s"
                            % (UTMZone, str(Resolution), str(Resolution), split_fname, fname_noext+'.bil'))

                # write the commands to the 2 scripts
                gdal.write('nice ' + gdal_str + '\n')
                if Hillshade:
                    hs_str = ('gdaldem hillshade -of ENVI '
                              '%s_DEM.bil %s_HS.bil\n'
                              % (fname_noext, fname_noext))
                    gdal.write(hs_str)

    print '\tScripts successfully written.'

#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello! I'm going to do some gridding and filtering for you.")
    print("You will need to tell me which directory to look in.")
    print("Use the -dir flag to define the working directory.")
    print("If you don't do this I will assume the data is in the same directory as this script.")
    print("For help type:")
    print("   python lidar_automator.py -h\n")
    print("=======================================================================\n\n ")

def main(argv):

    import argparse

    # If there are no arguments, send to the welcome screen
    if not len(sys.argv) > 1:
        full_paramfile = print_welcome()
        sys.exit()

    # parse in the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--base_directory", type=str, help="The base directory with the files. If this isn't defined I'll assume it's the same as the current directory.")
    parser.add_argument("-n_cores", "--n_cores", type=int, default=1, help="The number of cores you want to run the scripts on.")
    parser.add_argument("-zone", "--UTM_zone", type=int, help="The UTM zone that you want to project your data into")
    parser.add_argument("-res", "--grid_resolution", type=int, default=1, help="The grid resolution you want for your data.")
    parser.add_argument('-hs', '--hillshade', type=bool, default=False, help="If true, will create hillshades of the DEMs")
    parser.add_argument('-fmt', '--input_format', type=str, default='tif', help="The input format of your DEMs (default = tif)")

    parser.add_argument('-las', '--las2dem', type=bool, default=False, help="If true, I'll search for all the LAS files in the data directory and generate scripts for filtering and gridding them.")
    parser.add_argument('-gdal', '--gdal', type=bool, default=False, help="If true, I'll generate a bash script for translating your DEMs into an LSDTopoTools-friendly format.")

    args = parser.parse_args()

    if not args.UTM_zone:
        print("WARNING! You haven't supplied a UTM Zone. Please specify this with the flag '-zone'")
        sys.exit()

    # get the data directory
    if not args.base_directory:
        print("WARNING! You haven't supplied the data directory. Using current directory...")
        this_dir = os.getcwd()
    else:
        this_dir = args.base_directory

    # now run the functions depending on your choices
    if args.las2dem:
        LAStoGRID(this_dir, args.n_cores, args.UTM_zone, args.grid_resolution, args.hillshade)
    if args.gdal:
        gdalScripter(this_dir, args.n_cores, args.UTM_zone, args.grid_resolution, args.input_format, args.hillshade)

#=============================================================================
if __name__ == "__main__":
    main(sys.argv[1:])
