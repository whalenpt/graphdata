
import os 
import sys 
from ..helper import GenMovie
from ..helper import GetDataFileInfo
from ..helper import GenFileList
from ..helper import MovLength
from ..graphdata import plt
from ..graphdata import configs 
from ..graphdata import np 
from ..plot1D import PlotH 
from ..plot1D import PlotHL


def PlotM(*args,**kwargs):
  """
  Movie consisting of a sequence of 1D x-y graphs. 

  PlotM(fileID,fileRange,opts): 

  fileID: ID for data files where files look like fileID_fileNum.dat e.g. if
  data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the fileID is
  simply 'T'

  fileRange = [numFiles,minFileNum,maxFileNum] 
  fileRange: Specifies the files from which to accept data.  
  numFiles:     Number of 1D data files to plot 
  minFileNum:   Start file number.  
  maxFileNum:   End file number.
  If no fileRange is given, then all data files corresponding to the
  fileID are used.  fileRange does not need to specify minFileNum or
  maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
  spaced data files of fileID 'T' starting with the first available data
  file and ending with the last available data

  opts: Are optional arguments including

  limits (lim) = [minX,maxX,minY,maxY]
  minX:  Minimum x value limit 
  maxX:  Maximum x value limit 
  minY:  Minimum y value limit 
  maxY:  Maximum y value limit 

  xlim = [minX,maxX]  
  ylim = [minY,maxY]

  If no limits are given, then all data is used in the
  plots and then minimum and maximum graph limits will depend on the
  minimum and maximum data limits of the input and output variables.
  limits does not need to specify a minimum and maximum y value e.g.
  Evolve('T',10,[0 1]) will plot data with an input value between 0 and 1 

  movLen = val 
  Length of movie in seconds. This parameter determines time
  interval between succesive plot frames in the movie. If it is not
  specified then a default value will be used. This default value is set
  in 
     
  e.g. PlotM('T',[10,0,60],lim=[0,1,-10,10]) will produce a 1D Movie with 10
  (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
  then to ..., and lastly T_60.dat. The graph will truncate inputs to the
  range of 0 to 1 and plot output in the range of -10 to 10

  e.g. PlotM('ST',40) will produce a movie with 40 frames (if 40 data
  files are available of fileID 'ST')

  e.g. PlotM('ST',40,lim=[1.5,2.5,-5,5],movLen=10) will produce a 10 second movie
  with 40 frames of data (if 40 data files are available of fileID 'ST')
  and  with x and y plot limits given by 1.5 < x < 2.5 and -5 < y < 5.

  """

  fileList = GenFileList(*args)
  imageList = ProcessMovie(fileList,**kwargs)
  fileID = args[0]
  movLength = MovLength(**kwargs)
  GenMovie(imageList,fileID,movLength,**kwargs)

def PlotLM(*args,**kwargs): 
  """
  SemiLogy movie consisting of a sequence of 1D x-y graphs. 

  PlotLM(fileID,fileRange,opts): 

  fileID: ID for data files where files look like fileID_fileNum.dat e.g. if
  data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the fileID is
  simply 'T'

  fileRange = [numFiles,minFileNum,maxFileNum] 
  fileRange: Specifies the files from which to accept data.  
  numFiles:     Number of 1D data files to plot 
  minFileNum:   Start file number.  
  maxFileNum:   End file number.
  If no fileRange is given, then all data files corresponding to the
  fileID are used.  fileRange does not need to specify minFileNum or
  maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
  spaced data files of fileID 'T' starting with the first available data
  file and ending with the last available data

  opts: Are optional arguments including

  limits (lim) = [minX,maxX,minY,maxY]
  minX:  Minimum x value limit 
  maxX:  Maximum x value limit 
  minY:  Minimum y value limit 
  maxY:  Maximum y value limit 

  xlim = [minX,maxX]  
  ylim = [minY,maxY]

  If no limits are given, then all data is used in the
  plots and then minimum and maximum graph limits will depend on the
  minimum and maximum data limits of the input and output variables.
  limits does not need to specify a minimum and maximum y value e.g.
  Evolve('T',10,[0 1]) will plot data with an input value between 0 and 1 

  decades = val
  Number of decades of data to plot. Can be used instead of
  ylim = [ymin,ymax] for semilogy PlotLM movies
 
  movLen = val 
  Length of movie in seconds. This parameter determines time
  interval between succesive plot frames in the movie. If it is not
  specified then a default value will be used. This default value is set
  in 
     
  e.g. PlotLM('T',[10,0,60],lim=[0,1,-10,10]) will produce a 1D Movie with 10
  (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
  then to ..., and lastly T_60.dat. The graph will truncate inputs to the
  range of 0 to 1 and plot output in the range of -10 to 10

  e.g. PlotLM('SQ_ST',40,decs=) will produce a movie with 40 frames (if 40 data
  files are available of fileID 'SQ_ST')

  e.g. PlotM('SQ_ST',40,lim=[1.5,2.5,-5,5],movLen=10) will produce a 10 second movie
  with 40 frames of data (if 40 data files are available of fileID 'ST')
  and  with x and y plot limits given by 1.5 < x < 2.5 and -5 < y < 5.

  """

  fileList = GenFileList(*args)
  imageList = ProcessMovieL(fileList,**kwargs)
  fileID = args[0]
  movLength = MovLength(**kwargs)
  GenMovie(imageList,fileID,movLength,**kwargs)

def ProcessMovie(fileList,**kwargs):
  imageList = []
  plt.clf()
  configs.DefaultLS()
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    PlotH(fileID,repNum,**kwargs)
    imgFile = fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
    plt.clf()
    configs.DefaultLS()
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList

def ProcessMovieL(fileList,**kwargs):
  imageList = []
  plt.clf()
  configs.DefaultLS()
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    PlotHL(fileID,repNum,**kwargs)
    imgFile = fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
    plt.clf()
    configs.DefaultLS()
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList


