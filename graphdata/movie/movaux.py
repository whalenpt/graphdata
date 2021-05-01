
import os
import subprocess
from graphdata import configs 

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
  cdc = 'vcodec=' + str(configs._G['movFormat'])
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
  cdc = 'vcodec=' + str(configs._G['movFormat'])
  command = ('mencoder',str2,'-mf',str4,
             '-ovc','lavc','-lavcopts',cdc,'-oac','copy',
             '-o',strAvi)
#  print(command)
  return command


def MovLength(**kwargs):
  movLength = float(configs._G['movLength'])
  if 'movLen' in kwargs:
    movLength = kwargs['movLen']
  return movLength


