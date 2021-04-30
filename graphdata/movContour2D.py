
import os 
from .aux import GenMovie
from .aux import GetDataFileInfo
from .aux import GenFileList
from .aux import MovLength
import sys 
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 
from .contour2D import ContourHF
from .contour2D import ContourHLF

def ContourFM(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessMovieF(fileList,**kwargs)
  fileID = args[0]
  movName = "ContourF_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ContourLFM(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessMovieLF(fileList,**kwargs)
  fileID = args[0]
  movName = "ContourLF_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ProcessMovieF(fileList,*args,**kwargs):

  imageList = []
  confineLayout = True
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    ContourHF(fileID,repNum,*args,**kwargs)
    imgFile = 'ContourF_' + fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    pl.savefig(imgFile)
  pl.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList

def ProcessMovieLF(fileList,*args,**kwargs):
  imageList = []
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    ContourHLF(fileID,repNum,*args,**kwargs)
    imgFile = 'ContourLF_' + fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    pl.savefig(imgFile)
  pl.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList



