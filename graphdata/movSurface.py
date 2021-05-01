
import os 
from .helper import GenMovie
from .helper import GetDataFileInfo
from .helper import GenFileList
import sys 
from graphdata import plt
from graphdata import configs 
from graphdata import np 
from .surface import SurfaceH
from .surface import WireH


def SurfaceM(*args):
  """
  Movie consisting of a sequence of 2D x-y-z graphs. 
  SurfaceM(fileID,fileRange,plotLimits,viewingAngles,figSize,movieLength):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat
      e.g. if data files for RT data are RT_0.dat,RT_1.dat,RT_2.dat,...
      then the fileID is simply 'RT'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the fileID
      are used.  fileRange does not need to specify minFileNum or maxFileNum
      e.g. SurfaceM('RT',[10]) and SurfaceM('RT',10) evolve 10 evenly spaced data
      files of fileID 'RT' starting with the first available data file and
      ending with the last available data

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the Surface plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. SurfaceM('RT',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. SurfaceM('RT',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. SurfaceM('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits
          between 0 and 1, y-limits between -2 and 2, and z-limits from 0 to 10
        e.g. SurfaceM('RT',10,[]) is the same as Surface('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. 

    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. SurfaceM('RT',10,[],[],[14,5]) will plot a surface images
            with a width of 14 inches and a height of 5 inches

    movieLength: Length of movie in seconds. This parameter determines time 
    interval between succesive plot frames in the movie. If it is not  
    specified then a default value will be used. This default value is 
    set in 
     
    e.g. SurfaceM('RT',[10,0,60],[0,1,-10,10,0,1]) will produce a 2D Surface Movie with 
    10 (input,output) data pairs starting with RT_0.dat, then going to RT_6.dat,
    then to ..., and lastly RT_60.dat. The graph will truncate the x-axis to the
    range of 0 to 1, y-axis to the range of -10 to 10 and z-axis from 0 to 1. 

    e.g. SurfaceM('RT') will produces a movie consisting of all available RT data
    with no frame plotting limits

    e.g. SurfaceM('RT',[],[],5) will produce a 2D Surface Movie with 
    of all data lasting 5 seconds.
  """

  fileList = GenFileList(*args)
  plotArgs = args[2:]
  imageList = ProcessMovie(fileList,*plotArgs)
  fileID = args[0]
  movName = "Surface_" + str(fileID)
  movLength = MovLength(*args)
  GenMovie(imageList,movName,movLength)

def ProcessMovie(fileList,*args):
  imageList = []
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    SurfaceH(fileID,repNum,*args)
    imgFile = 'Surface_' + fileID + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList

def WireM(*args):
  """
  Movie consisting of a sequence of 2D x-y-z graphs. 
  WireM(fileID,fileRange,plotLimits,viewingAngles,figSize,movieLength):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat
      e.g. if data files for RT data are RT_0.dat,RT_1.dat,RT_2.dat,...
      then the fileID is simply 'RT'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the fileID
      are used.  fileRange does not need to specify minFileNum or maxFileNum
      e.g. WireM('RT',[10]) and WireM('RT',10) evolve 10 evenly spaced data
      files of fileID 'RT' starting with the first available data file and
      ending with the last available data

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the Wire plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. Wire('RT',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. Wire('RT',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. Wire('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits
          between 0 and 1, y-limits between -2 and 2, and z-limits from 0 to 10
        e.g. Wire('RT',10,[]) is the same as Wire('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. 

    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. WireM('RT',10,[],[],[14,5]) will plot wire images
            with a width of 14 inches and a height of 5 inches
 
    movieLength: Length of movie in seconds. This parameter determines time 
    interval between succesive plot frames in the movie. If it is not  
    specified then a default value will be used. This default value is 
    set in 

    e.g. WireM('RT',[10,0,60],[0,1,-10,10,0,1]) will produce a 2D Wire Movie with 
    10 (input,output) data pairs starting with RT_0.dat, then going to RT_6.dat,
    then to ..., and lastly RT_60.dat. The graph will truncate the x-axis to the
    range of 0 to 1, y-axis to the range of -10 to 10 and z-axis from 0 to 1. 

    e.g. WireM('RT') will produces a movie consisting of all available RT data
    with no frame plotting limits

    e.g. WireM('RT',[],[],5) will produce a 2D Wire Movie with 
    of all data lasting 5 seconds.
  """

  fileList = GenFileList(*args)
  plotArgs = args[2:]
  imageList = ProcessMovieW(fileList,*plotArgs)
  fileID = args[0]
  movName = "Wire_" + str(fileID)
  movLength = MovLength(*args)
  GenMovie(imageList,movName,movLength)

def MovLength(*args):
  if len(args) > 5:
    movLength = float(args[5])
  else:
    movLength = float(configs._G['movLength'])
  return movLength


def ProcessMovieW(fileList,*args):
  imageList = []
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    WireH(fileID,repNum,*args)
    imgFile = 'Wire_' + fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList


#def ProcessMovieL(fileList,*args):
#  imageList = []
#  plt.clf()
#  configs.DefaultLS()
#  for file in fileList: 
#    fileID,repNum = GetDataFileInfo(file) 
#    SurfaceL(fileID,repNum,*args)
#    imgFile = fileID + '_' + str(repNum) + '.png'
#    imageList.append(imgFile)
#    plt.savefig(imgFile)
#    plt.clf()
#    configs.DefaultLS()
#  plt.close()
#  if not imageList:
#    print "No images generated in ProcessMovie. "  
#    sys.exit()
#  return imageList



