
import os 
from graphdata.movie.movaux import GenMovie
from graphdata.movie.movaux import MovLength
from graphdata.shared.shared import GenFileList
import sys 
from graphdata import plt
from graphdata import configs 
from graphdata import np 
from graphdata.contour import contourf

def contourfMovie(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessContourfMovie(fileList,**kwargs)
  fileID = args[0]
  movName = "contourfMovie_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ProcessContourfMovie(fileList,*args,**kwargs):
  imageList = []
  confineLayout = True
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    contourf(fileID,repNum,*args,overwrite=True,**kwargs)
    imgFile = 'ContourF_' + fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList

def contourfLogMovie(*args,**kwargs):
  fileList = GenFileList(*args)
  imageList = ProcessContourfLogMovie(fileList,**kwargs)
  fileID = args[0]
  movName = "contourfLogMovie_" + str(fileID)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,movName,movLength)

def ProcessContourfLogMovie(fileList,*args,**kwargs):
  imageList = []
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    ContourHLF(fileID,repNum,*args,overwrite=True,**kwargs)
    imgFile = 'ContourLF_' + fileID + '_' + str(repNum) + '.png'
    imageList.append(imgFile)
    plt.savefig(imgFile)
  plt.close()
  if not imageList:
    print("No images generated in ProcessMovie. ")  
    sys.exit()
  return imageList



