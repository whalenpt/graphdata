#!/usr/bin/env python

"""--------------------------------------------------------------------------
   
    Author: "Patrick Whalen"
    Email: "whalenpt@gmail.com"
    Status: "Development"
    Date: "01/17/2022"
    Description: Python functions for making movies with mplayer

--------------------------------------------------------------------------"""

# IMPORTS

from graphdata import plt
from graphdata import configs 
from graphdata import np 
from graphdata.shared.idnum import GetDataFileList
import subprocess
import tempfile
import os
from shutil import which

def movie(fileID : str, fileNumbers : list, func, duration : int = 10, \
        vcodec : str = 'mpeg4', movie_name=None, **kwargs):
    """
    Movie of a list of data files plotted using a specified function [func]

    INPUTS:
        fileID: str
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (extension is a catchall, doesnt have to be dat)

        fileNumbers: list[int]
            Specifies which data file numbers to plot 
            e.g.  waterfall('T',[0:2:100]) will plot files T_0.dat,T_2.dat,...,T_100.dat

        func: function[fileID,fileNumbers,overwrite=True,**kwargs]
            Specifies the function to use for graphing data in the movie

        duration: int
            Amount of time in seconds to cycle through all graph frames

        vcodec : str
            The codec used by mplayer: one of the following (asv1,asv2,dvvideo,\
                    ffv1,ffvhuff,flv,h261,h263,h263p,huffyuv,libtheora,libx264,\
                    libxvid,ljpeg,mjpeg,mpeg1video,mpeg2video,mpeg4,msmpeg4,\
                    msmpeg4v2,roqvideo,rv10,snow,svq1,wmv1,wmv2

        **kwargs: dict
            Optional arguments to be passed on to the function used for plotting data

    OUTPUTS:
        None - creates movie file using system subprocess

    """

    if which('mplayer') is None:
        raise ImportError('MPlayer is not installed: the movie function will not work')

    if movie_name is None:
        movie_name = fileID + '.' + vcodec

    file_list = GetDataFileList(fileID,fileNumbers)
    image_list = []
    image_dir = tempfile.mkdtemp() # create temporary image directory

    dpi = 100
    w = 800; h = 600
    figsize = (w/dpi,h/dpi)
    if 'figsize' in kwargs:
        (w,h) = kwargs['figsize']
        w = dpi*int(w)
        h = dpi*int(h)
    else:
        kwargs['figsize'] = figsize

    for i,file in enumerate(file_list): 
        func(file,overwrite=True,**kwargs)
        image_file = os.path.join(image_dir,fileID + '_' + str(i) + '.png')
        plt.savefig(image_file,format='png')
        plt.clf()
        image_list.append(image_file)
    plt.close()
    if not image_list:
        raise RuntimeError("Failed to make a movie: images would not save")

    fps = len(image_list)/float(duration)
    str2 = 'mf://' 
    for file in image_list:
        str2 = str2 + file + ','
    str2 = str2[0:-1] # remove last comma

    str4 = 'type=png:w=' + str(w) + ':h='+str(h)+':fps='+ str(fps)
    cdc = 'vcodec=' + vcodec
    command = ['mencoder',str2,'-mf',str4,
      '-ovc','lavc','-lavcopts',cdc,'-vf','scale='+str(w)+':'+str(h),'-oac','copy',
             '-o',movie_name]
    print(command)
    try:
        subprocess.call(command)
        print(movie_name + " generated.") 
    except:
        print('Failed to generate ' + movie_name)
    
    for file in image_list: 
        if os.path.isfile(file):
            os.remove(file)
    os.removedirs(image_dir) # delete image directory


#def ProcessMovie(fileList,**kwargs):
#  imageList = []
#  pl.clf()
#  configs.DefaultLS()
#  for file in fileList: 
#    fileID,repNum = GetDataFileInfo(file) 
#    PlotH(fileID,repNum,**kwargs)
#    imgFile = fileID + '_' + str(repNum) + '.png'
#    imageList.append(imgFile)
#    pl.savefig(imgFile)
#    pl.clf()
#    configs.DefaultLS()
#  pl.close()
#  if not imageList:
#    print("No images generated in ProcessMovie. ")  
#    sys.exit()
#  return imageList
#
#
#def genMovie(fileList,movName,movLength,**kwargs):
#  loops = '3'
#  if 'loops' in kwargs:
#    loops = kwargs['loops']
#  str2 = 'mf://' 
#  for nm in fileList:
#    str2 = str2 + nm + ','
#  str2 = str2[0:-1]
#
#  fps = len(fileList)/float(movLength)
#  str4 = 'type=png:w=800:h=600:fps='+ str(fps)
#  strAvi = movName + '.avi'
#  cdc = 'vcodec=' + str(configs.G['movFormat'])
#  command = ['mencoder',str2,'-mf',str4,
#      '-ovc','lavc','-lavcopts',cdc,'-vf','scale=800:600','-oac','copy',
#             '-o',strAvi]
#  print(command)
#  try:
#    subprocess.call(command)
#    cmd = 'mplayer -loop ' + str(loops) + ' ' + strAvi
#    os.system(cmd)
#    print(str(movName) + ".avi generated.") 
#  except:
#    print(str(movName) + ".avi NOT generated.") 
#
#def GetMovieCommand(fileList,movName,movLength):
#  str2 = 'mf://' 
#  for nm in fileList:
#    str2 = str2 + nm + ','
#  str2 = str2[0:-1]
#  fps = len(fileList)/movLength
#  str4 = 'type=png:w=800:h=600:fps='+ str(fps)
#  strAvi = movName + '.avi'
#  cdc = 'vcodec=' + str(configs.G['movFormat'])
#  command = ('mencoder',str2,'-mf',str4,
#             '-ovc','lavc','-lavcopts',cdc,'-oac','copy',
#             '-o',strAvi)
#  print(command)
#  return command










