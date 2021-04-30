#!/usr/bin/python
import subprocess
import os 

def GenMovie(fileList,movName,movLength):
str2 = 'mf://' 
for nm in fileList:
  str2 = str2 + nm + ','
str2 = str2[0:-1]
fps = len(fileList)/movLength
str4 = 'type=png:w=800:h=600:fps='+ str(fps)
strAvi = movName + '.avi'
cdc = 'vcodec=' + str(configs.G['movFormat'])
command = ['mencoder',str2,'-mf',str4,
           '-ovc','lavc','-lavcopts',cdc,'-oac','copy',
           '-o',strAvi]
print command
try:
  subprocess.call(command)
  cmd = 'mplayer -loop 3 ' + strAvi
  os.system(cmd)
  print str(movName) + ".avi generated." 
except:
  print str(movName) + ".avi NOT generated." 


