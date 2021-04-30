#!/usr/bin/python
# Filename: optic.py

import shutil 
import glob
import os 
import string
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 
from .aux import SortNumericStringList 
from .aux import ProcessAux
from .aux import LoadData1D
from .aux import LoadData2D
from .aux import GetDataFileInfo 
from .aux import GetDataFileInfoS
from .aux import GenFileList

def ConvertData1D(x,y,auxDict,direction):
  if direction == 'ftow':
    if 'xlabel' in auxDict:
      auxDict['xlabel'] = '$\lambda$'
    if 'xscale' in auxDict:
      auxDict['xscale'] = 2.0*np.pi*3.0e8/float(auxDict['xscale']) 
    if 'xscale_str' in auxDict:
      auxDict['xscale_str'] = '$\lambda_{0}$'
    if 'xunit_str' in auxDict:
      auxDict['xunit_str'] = 'm'
    if 'xcordID' in auxDict:
      if auxDict['xcordID'] != 'ST':
        print('xcordID muconfigs be ST to proceed. ') 
        return False
  elif direction == 'wtof':
    if 'xlabel' in auxDict:
      auxDict['xlabel'] = '$\omega$'
    if 'xscale' in auxDict:
      auxDict['xscale'] = 2.0*np.pi*3.0e8/float(auxDict['xscale']) 
    if 'xscale_str' in auxDict:
      auxDict['xscale_str'] = '$\omega_{0}$'
    if 'xunit_str' in auxDict:
      auxDict['xunit_str'] = 's$^{-1}$'
    if 'xcordID' in auxDict:
      if auxDict['xcordID'] != 'ST':
        print('xcordID muconfigs be ST to proceed. ') 
        return False

  x = 2.0*np.pi*3.0e8/x
  x = np.flipud(x)
  y = np.flipud(y)
  return(x,y,auxDict)

def Write1D(fileName,x,y,auxDict,option):
  if option != 'wo':
    fileID,repNum = GetDataFileInfo(fileName)
    fileName = fileID + 'w' + '_' + str(repNum) + '.dat'
  data = np.vstack((x,y)) 
  data = data.transpose()
  print(fileName)
  with open(fileName,'w') as f:
    for item in auxDict:
      f.write('#' + item + ':\t\t\t' + str(auxDict[item]) + '\n')
    np.savetxt(f,data,fmt = '%18.12e')

def FreqToWaveF1D(*args):
  fileName = args[0]
  plotArgs = args[1:]
  if len(plotArgs) > 0:
    option = plotArgs[0] 
  else:
    option = ''
  x,y,auxDict = LoadData1D(fileName)
  x,y,auxDict = ConvertData1D(x,y,auxDict,'ftow')
  Write1D(fileName,x,y,auxDict,option)
  return True

def FreqToWave1D(*args):
  fileList = GenFileList(*args)
  optArgs = args[2:]
  if len(optArgs) > 0:
    option = optArgs[0] 
  else:
    option = ''
  for file in fileList:
    FreqToWaveF1D(file,option)

def WaveToFreqF1D(*args):
  fileName = args[0]
  plotArgs = args[1:]
  if len(plotArgs) > 0:
    option = plotArgs[0] 
  else:
    option = ''
  x,y,auxDict = LoadData1D(fileName)
  x,y,auxDict = ConvertData1D(x,y,auxDict,'wtof')
  Write1D(fileName,x,y,auxDict,option)
  return True

def WaveToFreq1D(*args):
  fileList = GenFileList(*args)
  optArgs = args[2:]
  if len(optArgs) > 0:
    option = optArgs[0] 
  else:
    option = ''
  for file in fileList:
    WaveToFreqF1D(file,option)

def FreqToWaveF2D(*args):
  fileName = args[0]
  plotArgs = args[1:]
  if len(plotArgs) > 0:
    option = plotArgs[0] 
  else:
    option = ''
  x,y,z,auxDict = LoadData2D(fileName)
  x,y,z,auxDict = ConvertData2D(x,y,z,auxDict,'ftow')
  Write2D(fileName,x,y,z,auxDict,option)
  return True

def FreqToWave2D(*args):
  fileList = GenFileList(*args)
  optArgs = args[2:]
  if len(optArgs) > 0:
    option = optArgs[0] 
  else:
    option = ''
  for file in fileList:
    FreqToWaveF2D(file,option)

def Write2D(fileName,x,y,z,auxDict,option):
  if option != 'wo':
    fileID,repNum = GetDataFileInfo(fileName)
    fileName = fileID + 'w' + '_' + str(repNum) + '.dat'
  xy_data = np.hstack((x,y)) 
  with open(fileName,'w') as f:
    for item in auxDict:
      f.write('#' + item + ':\t\t\t' + str(auxDict[item]) + '\n')
    dimstr = str(len(x)) + '  ' + str(len(y)) + '\n'
    f.write(dimstr)
    np.savetxt(f,xy_data,fmt = '%18.12e')
    np.savetxt(f,z,fmt = '%18.12e')
  print(fileName)

def ConvertData2D(x,y,z,auxDict,direction):
  if direction == 'ftow':
    if 'xlabel' in auxDict:
      auxDict['xlabel'] = '$\lambda$'
    if 'xscale' in auxDict:
      auxDict['xscale'] = 2.0*np.pi*3.0e8/float(auxDict['xscale']) 
    if 'xscale_str' in auxDict:
      auxDict['xscale_str'] = '$\lambda_{0}$'
    if 'xunit_str' in auxDict:
      auxDict['xunit_str'] = 'm'
    if 'xcordID' in auxDict:
      if auxDict['xcordID'] != 'ST':
        print('xcordID muconfigs be ST to proceed. ') 
        return False
    y = 2.0*np.pi*3.0e8/y[1:]
    y = np.flipud(y)
  elif direction == 'wtof':
    if 'xlabel' in auxDict:
      auxDict['xlabel'] = '$\omega$'
    if 'xscale' in auxDict:
      auxDict['xscale'] = 2.0*np.pi*3.0e8/float(auxDict['xscale']) 
    if 'xscale_str' in auxDict:
      auxDict['xscale_str'] = '$\omega_{0}$'
    if 'xunit_str' in auxDict:
      auxDict['xunit_str'] = 's$^{-1}$'
    if 'xcordID' in auxDict:
      if auxDict['xcordID'] != 'ST':
        print('xcordID muconfigs be ST to proceed. ') 
        return False
    y = 2.0*np.pi*3.0e8/y
    y = np.flipud(y)

  z = np.fliplr(z)
  return(x,y,z,auxDict)

def SwapIndx1D(fileID):
  fileList = GenFileList(fileID)
  for file in fileList: 
    newID,repNum,simNum = GetDataFileInfoS(file)
    newName = fileID + 'temp_' + str(simNum) + '_' + str(repNum) + '.dat'
    shutil.move(file,newName)
  tempID = fileID + 'temp'
  fileList = GenFileList(tempID)
  for file in fileList: 
    newID,repNum,simNum = GetDataFileInfoS(file)
    newName = fileID + '_' + str(repNum) + '_' + str(simNum) + '.dat'
    shutil.move(file,newName)

