
import os 
from graphdata.movie.movaux import GenMovie
from graphdata.movie.movaux import MovLength
from graphdata.shared import GenFileList
import sys 
from graphdata import plt
from graphdata import configs 
from graphdata import np 
from graphdata.contour import ContourHF
from graphdata.contour import ContourHLF

def ContourfMovie(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessMovieF(fileList,**kwargs)
  fileID = args[0]
  movName = "ContourfMovie_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ContourLFM(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessMovieLF(fileList,**kwargs)
  fileID = args[0]
  movName = "ContourfLogMovie_" + str(fileID)
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
    plt.savefig(imgFile)
  plt.close()
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
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList



