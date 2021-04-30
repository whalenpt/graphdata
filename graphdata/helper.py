#!/usr/bin/python
# Filename: aux.py

import shutil 
import glob
import os 
import string
import re
import sys 
import subprocess
import operator
from graphdata import plt
from graphdata import configs 
from graphdata import np 

# Load Data truncates off imaginary values if present
def LoadData1D(fileName):
  fileList = glob.glob(fileName)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()
  auxDict = ProcessAux(fileName) 
  with open(fileName,'rb') as f:
    data = np.genfromtxt(f,skip_header=len(auxDict))
    x = data[:,0]; y = data[:,1];
  return (x,y,auxDict)

def LoadData2D(file):
  fileList = glob.glob(file)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()

  auxDict = ProcessAux(file) 
  with open(file) as f:
    line = f.readline()
    while(line.startswith('#')):
      line = f.readline()
    nD1,nD2 = line.split()
    nD1 = int(nD1)
    nD2 = int(nD2)
    x = []
    y = []
    for i in range(nD1):
      x.append(float(f.readline()))
    for i in range(nD2):
      y.append(float(f.readline()))
    x = np.array(x)
    y = np.array(y)
    z = np.genfromtxt(f)
    shape = (nD1,nD2)
    z = z.reshape(shape)

  return (x,y,z,auxDict)

def LoadData3D(file):
  fileList = glob.glob(file)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()

  auxDict = ProcessAux(file) 
  with open(file) as f:
    line = f.readline()
    while(line.startswith('#')):
      line = f.readline()
    nD1,nD2,nD3 = line.split()
    nD1 = int(nD1)
    nD2 = int(nD2)
    nD3 = int(nD3)
    x1 = []
    x2 = []
    x3 = []
    for i in range(nD1):
      x1.append(float(f.readline()))
    for i in range(nD2):
      x2.append(float(f.readline()))
    for i in range(nD3):
      x3.append(float(f.readline()))
    x1 = np.array(x1)
    x2 = np.array(x2)
    x3 = np.array(x3)
    z = np.genfromtxt(f)
    shape = (nD1,nD2,nD3)
    z = z.reshape(shape)

  return (x1,x2,x3,z,auxDict)

def LoadParams(file):
  paramDict = dict()
  with open(file) as f:
    for line in f:
      if(line.find(':') != -1):
        key,val = line.split(':')
        key = key[0:]
        key = ' '.join(key.split())
        val = ' '.join(val.split())
        paramDict[key] = val
  return paramDict 

def LoadComplexData1D(fileName):
  fileList = glob.glob(fileName)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()
  auxDict = ProcessAux(fileName) 
  with open(fileName) as f:
    data = np.genfromtxt(f,skip_header=len(auxDict))
    x = data[:,0]; yr = data[:,1]; yi = data[:,2];
  return (x,yr,yi,auxDict)

def GenMovie(fileList,movName,movLength,**kwargs):
  loops = '3'
  if 'loops' in kwargs:
    loops = kwargs['loops']
  str2 = 'mf://' 
  for nm in fileList:
    str2 = str2 + nm + ','
  str2 = str2[0:-1]

  fps = len(fileList)/float(movLength)
  str4 = 'type=png:w=800:h=600:fps='+ str(fps)
  strAvi = movName + '.avi'
  cdc = 'vcodec=' + str(configs.G['movFormat'])
  command = ['mencoder',str2,'-mf',str4,
      '-ovc','lavc','-lavcopts',cdc,'-vf','scale=800:600','-oac','copy',
             '-o',strAvi]
  print(command)
  try:
    subprocess.call(command)
    cmd = 'mplayer -loop ' + str(loops) + ' ' + strAvi
    os.system(cmd)
    print(str(movName) + ".avi generated.") 
  except:
    print(str(movName) + ".avi NOT generated.") 

def GetMovieCommand(fileList,movName,movLength):
  str2 = 'mf://' 
  for nm in fileList:
    str2 = str2 + nm + ','
  str2 = str2[0:-1]
  fps = len(fileList)/movLength
  str4 = 'type=png:w=800:h=600:fps='+ str(fps)
  strAvi = movName + '.avi'
  cdc = 'vcodec=' + str(configs.G['movFormat'])
  command = ('mencoder',str2,'-mf',str4,
             '-ovc','lavc','-lavcopts',cdc,'-oac','copy',
             '-o',strAvi)
  print(command)
  return command


def MovLength(**kwargs):
  movLength = float(configs.G['movLength'])
  if 'movLen' in kwargs:
    movLength = kwargs['movLen']
  return movLength

def GenFileList(*args):

  fileList = []
  if len(args) == 0:
    print('Please enter at least one argument to GenFileList')
    return False

  fileID = ''
  if len(args) > 0:
    fileID = args[0]
    fileList = glob.glob(fileID + '_' + '*.dat')
    if len(fileList) == 0:
      print('No files detected for fileID: ' + fileID)
      print('Files in directory are: ')
      dirFiles = os.listdir('.')
      dirFiles = SortNumericStringList(dirFiles)
      print(fmtcols(dirFiles,1))
      return False
    else:
      fileList = SortNumericStringList(fileList)

  updateList = []
  if len(args) == 1:
    return fileList
  elif len(args) == 2:
    fileID = args[0] 
    fileSpec = args[1]
    if isinstance(fileSpec,int): 
      numFiles = fileSpec 
      repNums = set() 
      for file in fileList:
        idstr,repNum = GetDataFileInfo(file)
        repNums.add(int(repNum))
      indx1 = min(repNums)
      indx2 = max(repNums)
      tot = indx2 - indx1 + 1
      if tot <= numFiles:
        return fileList

      mult = int(np.floor(float(tot)/numFiles))
      if(mult == 0):
        mult = 1
      filenums = list(range(indx1,indx2,mult))
      if indx2 not in filenums:
        filenums.append(indx2)
      for i in filenums: 
        name = fileID + '_' + str(i) + '.dat'
        updateList.append(name)
      fileList = SortNumericStringList(updateList)
      return fileList
    elif len(fileSpec) == 0:
      fileID = args[0] 
      return fileList
    elif len(fileSpec) == 1:
      numFiles = int(fileSpec[0])
      repNums = set() 
      for file in fileList:
        idstr,repNum = GetDataFileInfo(file)
        repNums.add(int(repNum))
      indx1 = min(repNums)
      indx2 = max(repNums)
      tot = indx2 - indx1 + 1
      if tot <= numFiles:
        return fileList
      mult = int(np.floor(float(tot)/numFiles))
      if(mult == 0):
        mult = 1
      filenums = list(range(indx1,indx2,mult))
      if indx2 not in filenums:
        filenums.append(indx2)
      for i in filenums: 
        name = fileID + '_' + str(i) + '.dat'
        updateList.append(name)
      fileList = SortNumericStringList(updateList)
      return fileList
    elif len(fileSpec) > 1:
      repNums = set() 
      for file in fileList:
        idstr,repNum = GetDataFileInfo(file)
        repNums.add(int(repNum))
      numFiles = fileSpec[0] 
      minindx = min(repNums)
      maxindx = max(repNums)

      indx1 = max(fileSpec[1],minindx)
      indx2 = maxindx
      if len(fileSpec) > 2:
        indx2 = min(fileSpec[2],maxindx)

      tot = indx2 - indx1 + 1
      mult = int(np.floor(float(tot)/numFiles))
      if(mult == 0):
        mult = 1
      filenums = list(range(indx1,indx2,mult))
      if indx2 not in filenums:
        filenums.append(indx2)
      for i in filenums: 
        name = fileID + '_' + str(i) + '.dat'
        updateList.append(name)
      fileList = SortNumericStringList(updateList)
      return fileList
    else:
      print("Did not recognize number of arguments in GenFileList. ") 
      return False


def GetData1D(*arg):
  if len(arg) < 2:
    print("GetData1D requires at least two arguments: the fileID and file# ") 
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  print(fileName)
  x,y,auxDict = LoadData1D(fileName)
  return (x,y,auxDict)

def GetFileData1D(*arg):
  if len(arg) < 1:
    print("GetFileData1D requires at least one arguments: the file name ") 
    return False
  fileName = str(arg[0])
  print(fileName)
  x,y,auxDict = LoadData1D(fileName)
  return (x,y,auxDict)

def SetDecadeLimits(decades,y):
  ymax = 10.0*np.amax(y)
  ymin = pow(10,-decades-1)*ymax
  maxLevel = int(np.ceil(np.log10(ymax)))
  minLevel = int(maxLevel - decades - 1)
  indx = y < pow(10,minLevel)
  y[indx] = pow(10,minLevel)
  return y

def GetDataFileInfo(fileName):
  splitList = re.split('[.]',fileName)
  fName = splitList[0]
  splitList = re.split('[_]',fName)
  repNum = splitList[-1] 
  fileID = splitList[0] 
  for i in range(1,len(splitList)-1):
    fileID = fileID + '_' + str(splitList[i])
  return (fileID,repNum)

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

def GetData2D(*arg):
  if len(arg) < 2:
    print("GetData2D requires at least two arguments: the fileID and file# ") 
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  print(fileName)
  x,y,z,auxDict = LoadData2D(fileName)
  if len(arg) > 2:
    auxDict = SetLimits2D(arg[2],auxDict)
  return (x,y,z,auxDict)

def SetLimits2D(glist,auxDict):
  if len(glist) > 0:
    xmin = glist[0] 
    auxDict['xmin'] = xmin
  if len(glist) > 1:
    xmax = glist[1] 
    auxDict['xmax'] = xmax
  if len(glist) > 2:
    ymin = glist[2] 
    auxDict['ymin'] = ymin
  if len(glist) > 3:
    ymax = glist[3] 
    auxDict['ymax'] = ymax
  if len(glist) > 4:
    zmin = glist[4] 
    auxDict['zmin'] = zmin
  if len(glist) > 5:
    zmax = glist[5] 
    auxDict['zmax'] = zmax
  return auxDict

def GetDataL_2D(*arg):
  if len(arg) < 2:
    print("GetData2D requires at least two arguments: the fileID and file# ") 
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  print(fileName)
  x,y,z,auxDict = LoadData2D(fileName)
  if len(arg) > 2:
    auxDict = SetLimits2D(arg[2],auxDict)

  return (x,y,z,auxDict)

def GetRepNums(fileList):
  repNums = set()
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file)
    repNums.add(int(repNum))
  repList = list(repNums)
  repList.sort()
  return repList

def GetSimNums(fileID):
  simNums = set()
  fileList = glob.glob(fileID + '*')
  for file in fileList:
    fileID,repNum,simNum = GetDataFileInfoS(file)
    simNums.add(int(simNum))
  simList = list(simNums)
  simList.sort()
  return simList

def GetRepFileList(fileID):
  fileList = glob.glob(fileID + '_' + '*')
  fileList = SortNumericStringList(fileList)
  return fileList

def ProcessAux(file):
  auxDict = dict()
  with open(file) as f:
    line = f.readline()
    while(line.startswith('#')):
      key,val = line.split(':')
      key = key[1:]
      key = ' '.join(key.split())
      val = ' '.join(val.split())
      auxDict[key] = val
      line = f.readline()
  return auxDict

class NumericString:
  def __init__(self,rawValue):
    self.rawValue = rawValue

  def __lt__(self,other):
    if self.rawValue == other.rawValue: return 0
    if self.rawValue == None: return -1
    if other.rawValue == None: return 1
    if self.rawValue == "": return -1
    if other.rawValue == "": return 1

    xList = self.getValueList(self.rawValue)
    yList = self.getValueList(other.rawValue)

    for i in range(min(len(xList),len(yList))):
      compareResult = self.compareTwoVals(xList[i],yList[i])
      if compareResult != 0:
        return compareResult

    return operator.lt(len(xList),len(yList))


  def compareTwoVals(self,xVal,yVal):
    if xVal.isdigit() and yVal.isdigit():
      return operator.lt(int(xVal),int(yVal))
    if not xVal.isdigit() and not yVal.isdigit():
      return operator.lt(xVal,yVal)
    if xVal.isdigit():
      return -1
    return 1


  def getValueList(self,rawValue):
    values = []
    tempVal = ""

    for i in range(len(rawValue)):
      val = rawValue[i]
      if val.isdigit():
        tempVal += str(val)
      else:
        if tempVal != "":
          values.append(tempVal)
          tempVal = ""

        values.append(val)

    if tempVal != "":
      values.append(tempVal)

    return values

def SortNumericStringList(original):
  newList = [NumericString(x) for x in original]
  newList.sort()
  return [x.rawValue for x in newList]

def isaux(s):
  return s.startswith('#')


def fmtcols(mylist,cols):
  lines = ("\t".join(mylist[i:i+cols]) for i in range(0,len(mylist),cols))
  return '\n'.join(lines)



