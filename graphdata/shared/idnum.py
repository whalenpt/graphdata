"""--------------------------------------------------------------------------
   
    Author: "Patrick Whalen"
    Email: "whalenpt@gmail.com"
    Status: "Development"
    Date: "5/2/21"
    Description: Support functions for idnum modules

--------------------------------------------------------------------------"""
import glob

def GetDataFileName(fileID,fileNumber):
    search_string = fileID + '_' + str(fileNumber) + '.*'
    fileList = glob.glob(search_string)
    if not fileList:
        raise Exception('Failed to find a file matching the (fileID,fileNumber)=({},{}) with'\
                'search string of {}'.format(fileID,str(fileNumber),search_string))
    if len(fileList) > 1:
        files_string = '/n'.join(fileList)
        raise Exception('Found too many files matching the specified (fileID,fileNumber)=({},{})\
                Here are the files: {}'.format(fileID,fileNumber,files_string))
    return fileList[0]






