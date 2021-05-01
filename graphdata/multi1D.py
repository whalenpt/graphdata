
import glob
import string
from pprint import pprint

from .helper import SortNumericStringList
from .helper import GetMovieCommand
from .helper import fmtcols
from .helper import GetPlotFile 
from .helper import ProcessAux 

from .shared1D import AuxPlotLabel1D 
from .shared1D import ProcessData1D 

def GetMultiPlotFileList(fileID,num = 0):
  fileList = glob.glob(fileID + '_*_' + str(num) + '.dat')
  if not fileList:
    fileList = glob.glob(fileID + '_*.dat')
    if not fileList:
      print('No files detected for fileID: ' + fileID)
      print('Files in directory are: ')
      dirFiles = os.listdir('.')
      dirFiles = SortNumericStringList(dirFiles)
      print(fmtcols(dirFiles,1))
      return False

  fileList = SortNumericStringList(fileList)
  print(fmtcols(fileList,1))
  return fileList

def MultiPlot(fileID,num = 0):
  plt.clf()
  configs.DefaultLS()
  fileList = GetMultiPlotFileList(fileID,num)
  auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList = AuxMultiPlot1D(fileList)
  AuxPlotLabel1D(auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList)
  plt.ion()
  plt.show()
  return True

def MultiPlotL(fileID,num = 0):
  plt.clf()
  configs.DefaultLS()
  fileList = GetMultiPlotFileList(fileID,num)
  auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList = AuxMultiLogPlot1D(fileList)
  AuxPlotLabel1D(auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList)
  plt.ion()
  plt.show()
  return True

def AuxMultiPlot1D(fileList):
  xmin = 0.0
  xmax = 0.0
  ymin = 0.0
  ymax = 0.0
  count = 0
  titleList = []
  xscaleVec = [] 
  yscaleVec = [] 
  yminVec = [] 
  ymaxVec = [] 
  xminVec = [] 
  xmaxVec = [] 
  xscale = 0.0 
  yscale = 0.0 
  
  for file in fileList:
    auxDict = ProcessAux(file) 
    if 'xscale' in auxDict:
      xscaleVec.append(float(auxDict['xscale']))
    if 'yscale' in auxDict:
      yscaleVec.append(float(auxDict['yscale']))

    with open(file) as f:
      data = np.genfromtxt(f,skip_header=len(auxDict))
      x,y,xmin,xmax,ymin,ymax = ProcessData1D(data[:,0],data[:,1],auxDict)
      yminVec.append(ymin)
      ymaxVec.append(ymax)
      xminVec.append(xmin)
      xmaxVec.append(xmax)
      if "xscale" in auxDict:
        if(configs._G["scale"] == 'nonDim'):
          x = x/float(auxDict["xscale"])
        elif(configs._G["scale"] == 'dimscale'):
          x = x/float(configs._G['xdimscale'])

      if "yscale" in auxDict:
        if(configs._G["scale"] == 'nonDim'):
          y = y/float(auxDict["yscale"])
        elif(configs._G["scale"] == 'dimscale'):
          y = y/float(configs._G['ydimscale'])
      
      plt.plot(x,y,configs.LS[count])
      plt.hold(True) 
      titleList.append(auxDict["legend"])
      count  = count + 1

  
  ymin = np.amin(yminVec)
  ymax = np.amax(ymaxVec)
  xmin = np.amin(xminVec)
  xmax = np.amax(xmaxVec)
  xscale = 1.0
  yscale = 1.0
  if xscaleVec:
    xscale = np.amin(xscaleVec)
  if yscaleVec:
    yscale = np.amax(yscaleVec)

  return (auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList)


def AuxMultiLogPlot1D(fileList):
  xmin = 0.0
  xmax = 0.0
  ymin = 0.0
  ymax = 0.0
  count = 0
  titleList = []
  xscaleVec = [] 
  yscaleVec = [] 
  yminVec = [] 
  ymaxVec = [] 
  xminVec = [] 
  xmaxVec = [] 
  xscale = 0.0 
  yscale = 0.0 
  
  for file in fileList:
    auxDict = ProcessAux(file) 
    if 'xscale' in auxDict:
      xscaleVec.append(float(auxDict['xscale']))
    if 'yscale' in auxDict:
      yscaleVec.append(float(auxDict['yscale']))

    with open(file) as f:
      data = np.genfromtxt(f,skip_header=len(auxDict))
      x,y,xmin,xmax,ymin,ymax = ProcessData1D(data[:,0],data[:,1],auxDict)
      yminVec.append(ymin)
      ymaxVec.append(ymax)
      xminVec.append(xmin)
      xmaxVec.append(xmax)
      if "xscale" in auxDict:
        if(configs._G["scale"] == 'nonDim'):
          x = x/float(auxDict["xscale"])
        elif(configs._G["scale"] == 'dimscale'):
          x = x/float(configs._G['xdimscale'])

      if "yscale" in auxDict:
        if(configs._G["scale"] == 'nonDim'):
          y = y/float(auxDict["yscale"])
        elif(configs._G["scale"] == 'dimscale'):
          y = y/float(configs._G['ydimscale'])
      
      plt.semilogy(x,y,configs.LS[count])
      plt.hold(True) 
      titleList.append(auxDict["legend"])
      count  = count + 1

  
  ymin = np.amin(yminVec)
  ymax = np.amax(ymaxVec)
  xmin = np.amin(xminVec)
  xmax = np.amax(xmaxVec)
  xscale = 1.0
  yscale = 1.0
  if xscaleVec:
    xscale = np.amin(xscaleVec)
  if yscaleVec:
    yscale = np.amax(yscaleVec)

  return (auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList)


