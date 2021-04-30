
#!/usr/bin/python
# Filename: auxs.py

import shutil 
import glob
import os 
import string
import re
import sys 
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 
from .aux import GenFileList
from .aux import SortNumericStringList
from .aux import fmtcols

def GenFileListS(*args):
  fileID = '' 
  fileList = []
  if len(args) == 0:
    return False
  elif len(args) == 1:
    fileID = args[0] 
    simList = GetSimNums(fileID)
    for i in simList:
      fileIDs = fileID + '_' + str(i) 
      fileList.append(GenFileList(fileIDs))
  elif len(args) > 1:
    fileID = args[0] 
    fileSpec = args[1]
    simList = GetSimNums(fileID)
    for i in simList:
      fileIDs = fileID + '_' + str(i) 
      fileList.append(GenFileList(fileIDs,fileSpec)) 
  if not fileList:
    print("PlotM fileList not generated. ")  
    sys.exit()
  return fileList

def GetDataFileInfoS(fileName):
  splitList = re.split('[.]',fileName)
  fName = splitList[0]
  splitList = re.split('[_]',fName)
  repNum = splitList[-1] 
  simNum = splitList[-2] 
  fileID = splitList[0] 
  for i in range(1,len(splitList)-2):
    fileID = fileID + '_' + str(splitList[i])
  return (fileID,repNum,simNum)


def GetSimNums(fileID):
  simNums = set()
  fileList = glob.glob(fileID + '*.dat')
  for file in fileList:
    fileID,repNum,simNum = GetDataFileInfoS(file)
    simNums.add(int(simNum))
  simList = list(simNums)
  simList.sort()
  return simList

def GenFileListS(*arg):
  fileList = []
  fileID = ''
  num = 0
  if len(arg) == 1:
    fileID = arg[0]
    fileList = glob.glob(fileID + '_' + '*')
  elif len(arg) == 2:
    fileID,num = arg
    fileList = glob.glob(fileID + '_*_' + str(num) + '.dat')
  elif len(arg) == 0:
    print('Enter at least one argument to GetPlotFile ')
    return False
  else:
    print('Please only enter up to 2 arguments to GenFileListS(*args) ')
    return False

  if len(fileList) == 0:
    print('No files detected for fileID: ' + fileID)
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    return False
  else:
    fileList = SortNumericStringList(fileList)
    print(fileList)
    return fileList



