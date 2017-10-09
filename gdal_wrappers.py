#--------------------------------------------------------------#
# Functions for merging rasters with gdal
# FJC 09/10/17
#--------------------------------------------------------------#

def GetESRIFileNamesNextMap():

    file_list = []

    for DirName in glob("*/"):
        #print DirName

        directory_without_slash = DirName[:-1]

        this_filename = "./"+DirName+directory_without_slash+"dtme/hdr.adf\n"

        print this_filename
        file_list.append(this_filename)

    # write the new version of the file
    file_for_output = open("DEM_list.txt",'w')
    file_for_output.writelines(file_list)
    file_for_output.close()
