

import os 
from graphdata.movie.movaux import GenMovie
from graphdata.shared.shared import GetDataFileInfo
from graphdata.shared.shared import GenFileList
import sys 
from graphdata import plt
from graphdata import configs 
from graphdata import np 
from graphdata.surface import surface

def surfaceMovie(fileID,fileRange,limits=None,elev=None,azim=None,**kwargs):
  """
  Movie consisting of a sequence of 2D x-y-z graphs. 
  surfaceMovie(fileID,fileRange,plotLimits,viewingAngles,figSize,movieLength):
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
      e.g. surfaceMovie('RT',[10]) and surfaceMovie('RT',10) evolve 10 evenly spaced data
      files of fileID 'RT' starting with the first available data file and
      ending with the last available data

    limits = [minX,maxX,minY,maxY,minZ,maxZ]
    limits: Specifies the Surface plot limits 
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
        e.g. surfaceMovie('RT',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. surfaceMovie('RT',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. surfaceMovie('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits
          between 0 and 1, y-limits between -2 and 2, and z-limits from 0 to 10
        e.g. surfaceMovie('RT',10,[]) is the same as Surface('RT',10)

    figsize = [width,height]
    figsize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. surfaceMovie('RT',10,[],[],[14,5]) will plot a surface images
            with a width of 14 inches and a height of 5 inches

    movieLength: Length of movie in seconds. This parameter determines time 
    interval between succesive plot frames in the movie. If it is not  
    specified then a default value will be used. This default value is 
    set in 
     
    e.g. surfaceMovie('RT',[10,0,60],[0,1,-10,10,0,1]) will produce a 2D Surface Movie with 
    10 (input,output) data pairs starting with RT_0.dat, then going to RT_6.dat,
    then to ..., and lastly RT_60.dat. The graph will truncate the x-axis to the
    range of 0 to 1, y-axis to the range of -10 to 10 and z-axis from 0 to 1. 

    e.g. surfaceMovie('RT') will produces a movie consisting of all available RT data
    with no frame plotting limits

    e.g. surfaceMovie('RT',[],[],5) will produce a 2D Surface Movie with 
    of all data lasting 5 seconds.
  """

  fileList = GenFileList(*args)
  plotArgs = args[2:]
  imageList = ProcessSurfaceMovie(fileList,*plotArgs)
  fileID = args[0]
  movName = "Surface_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ProcessSurfaceMovie(fileList,*args):
  imageList = []
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    surface(fileID,repNum,*args,overwrite=True)
    imgFile = 'Surface_' + fileID + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList



