#!/usr/bin/python
# Filename: configurations.py

import os 
import sys
import copy
from matplotlib import rc,rcParams 
from pprint import pprint

class PlotSettings(object):

  def __init__(self):
    self.LoadSettings()
    self.LSoptions = {'basic':['k-o','k--d','k-.s','r-o','r--d','r-.s'],\
            'color':['k','r','b','g','c'],\
            'longcolor': ['k','r','b','g','c','k--','r--','b--','g--','c--'],\
            'color2':['r','b','g','k'],\
            'grey': ['k-o','k--d','k.-s','k--*'],\
            'cpaper':['k.','b--','r','gs'],\
            'cpaper2':['k--','r'],\
            'cpaper3':['k','b--','r','gs'],\
            'converge':['r-<','k-d','b-o','g-*','t-p','f-v'],\
            'converge2':['t-p','k-d','f-v','g-*'],\
            'converge3':['r-<','t-p','b-o','c-v'],\
            'converge4':['t-p','k-d','c-v','g-*']}
    self.LSvec = copy.deepcopy(self.LSoptions[self.G['LSvec']])
    self.LS = self.LSvec[0] 
    self.cmapvec = ['hot','jet','bone','gray','binary','gist_yarg']
    self.LegendList = []
    self.ModeVec = ['basic','paper']
    self.SetMode(self.G["Mode"])

  def LoadSettings(self):
    self.G = dict()
    defaultDict = {'Points1D': 100,'PointsX_2D':100,'PointsY_2D':100,\
      'scale':'nonDim','xdimscale':1.0,'ydimscale':1.0,'zdimscale':1.0,\
      'pdimscale':1.0,'xdimscale_str':'','ydimscale_str':'','zdimscale_str':'',\
      'pdimscale_str':'', 'process data':'on',\
      'LSvec':'color','cmap':'hot','title':'on','legend':'on',\
      'movFormat':'wmv2','movLength':10.0,\
      'FigWidth':14,'FigHeight':8,'FigWidthL':15,'FigHeightL':5,\
      'PlotWidth':14,'PlotHeight':8,'PlotWidthL':15,'PlotHeightL':5,\
      'SurfaceTickFormat':'%0.02e','NumberSurfaceTicks':6,'SurfaceTickFormat':'%0.02e',\
      'SurfaceWidth':8,'SurfaceHeight':8,'WireHeight':8,'WireWidth':8,\
      'ContourHeight':6,'ContourWidth':15,'contours':50,\
      'ConvergeHeight':6,'ConvergeWidth':6,\
      'EvolveHeight':8,'EvolveWidth':12,'EvolveHeightL':5,'EvolveWidthL':16,\
      'decades':12,\
      'Mode':'basic'}

    try:
      hm = os.environ.get("HOME")
      prFile = hm + "/Code/GraphData3/Settings/graphParams.txt"
      f = open(prFile)
      params = f.read() 
      f.close()
      for row in params.splitlines():
        nm,val = row.split(':')
        val = val.strip() 
        self.G[nm] = val
    except:
      print("graphParams.txt file not found.")

    for key in defaultDict:
      if key not in self.G:
        self.G[key] = defaultDict[key]


  def GraphParamStdOut(self):
    for key in sorted(self.G.keys()):
      print((key + "\t\t\t\t" + str(self.G[key])))

  def GraphParamFileOut(self):
    hm = os.environ.get("HOME")
    prFile = hm + "/CompletedProjects/Python/GraphData3/Settings/graphParams.txt"
    f = open(prFile,'w')
    for key in sorted(self.G.keys()):
      line = key + ":\t\t\t\t\t\t\t\t" + str(self.G[key]) + "\n"
      f.write(line)
    f.close()

  def ProcessScale(self,scale):
    if scale == 'femto' or scale == 'f':
      return ('f',1.0e-15)
    elif scale == 'nano' or scale == 'n':
      return ('n',1.0e-9)
    elif scale == 'micro' or scale == 'mu':
      return ('$\mu$',1.0e-6)
    elif scale == 'milli' or scale == 'm':
      return ('m',1.0e-3)
    elif scale == 'centi' or scale == 'c':
      return ('c',1.0e-2)
    elif scale == 'mega' or scale == 'M':
      return ('M',1.0e6)
    elif scale == 'giga' or scale == 'G':
      return ('G',1.0e9)
    elif scale == '':
      return ('',1.0)
    else:
      return False

  def ScaleX(self,scale):
    scale_str, scale_val = self.ProcessScale(scale)
    self.G['xdimscale'] = scale_val
    self.G['xdimscale_str'] = scale_str
    self.GraphParamFileOut()
  def ScaleY(self,scale):
    scale_str, scale_val = self.ProcessScale(scale)
    self.G['ydimscale'] = scale_val
    self.G['ydimscale_str'] = scale_str
    self.GraphParamFileOut()
  def ScaleZ(self,scale):
    scale_str, scale_val = self.ProcessScale(scale)
    self.G['zdimscale'] = scale_val
    self.G['zdimscale_str'] = scale_str
    self.GraphParamFileOut()
  def ScaleP(self,scale):
    scale_str, scale_val = self.ProcessScale(scale)
    self.G['pdimscale'] = scale_val
    self.G['pdimscale_str'] = scale_str
    self.GraphParamFileOut()

  def AddLegend(self,name):
    self.LegendList.append(name)

  def SetLegend(self,name):
    self.LegendList = []
    self.LegendList.append(name)

  def ContourSize(self,w,h):
    self.G["ContourWidth"] = w
    self.G["ContourHeight"] = h
    self.GraphParamFileOut()

  def EvolveSize(self,w,h):
    self.G["EvolveWidth"] = w
    self.G["EvolveHeight"] = h
    self.GraphParamFileOut()

  def EvolveSizeL(self,w,h):
    self.G["EvolveWidthL"] = w
    self.G["EvolveHeightL"] = h
    self.GraphParamFileOut()

  def SurfaceSize(self,w,h):
    self.G["SurfaceWidth"] = w
    self.G["SurfaceHeight"] = h
    self.GraphParamFileOut()

  def PlotSize(self,w,h):
    self.G["PlotWidth"] = w
    self.G["PlotHeight"] = h
    self.GraphParamFileOut()

  def PlotSizeL(self,w,h):
    self.G["PlotWidthL"] = w
    self.G["PlotHeightL"] = h
    self.GraphParamFileOut()

  def WireSize(self,w,h):
    self.G["WireWidth"] = w
    self.G["WireHeight"] = h
    self.GraphParamFileOut()

  def LogLogSize(self,w,h):
    self.G["LogLogWidth"] = w
    self.G["LogLogHeight"] = h
    self.GraphParamFileOut()

  def ConvergeSize(self,w,h):
    self.G["ConvergeWidth"] = w
    self.G["ConvergeHeight"] = h
    self.GraphParamFileOut()

  def ToggleLS(self):
    print((self.LSvec))
    item = self.LSvec.pop(0)
    self.LSvec.append(item)
    print((self.LSvec))
    self.LS = self.LSvec[0]

  def ToggleCmap(self):
    item = self.cmapvec.pop(0)
    self.cmapvec.append(item)
    self.G["cmap"] = str(self.cmapvec[0])
    print(("Colormap toggled to " + str(self.G["cmap"])))
    self.GraphParamFileOut()

  def SetCmap(self,val):
    """
    Cmap styles:  hot,jet,bone,gray,binary,gist_yarg,etc.
    """
    self.G["cmap"] = val 
    print(("Colormap set to " + str(self.G["cmap"])))
    self.GraphParamFileOut()

  def SetLS(self,key):
    """
    Linestyle options:
       basic:       ['k-o','k--d','k-.s','r-o','r--d','r-.s']
       color:       ['k','r','b','g','c']
       color2:      ['r','b','g','k']
       longcolor:   ['k','r','b','g','c','k--','r--','b--','g--','c--']
       grey:        ['k-o','k--d','k.-s','k--*']
       cpaper:      ['k.','b--','r','gs']
       cpaper2:      ['k--','r']
       converge:     ['r-<','k-d','b-o','g-*','t-p','f-v']
       converge2:     ['t-p','k-d','f-v','g-*']
    """
    
    if key in self.LSoptions:
      self.G['LSvec'] = key
      self.GraphParamFileOut()
      self.DefaultLS()
    else:
      print("Did not recognize linestyles. Here is a list of the options: ")
      print(('\n'.join("%s:\t\t %s" % (kkey, ','.join(map(str, values))) for kkey, values in list(self.LSoptions.items()))))

  def DefaultLS(self):
    self.LSvec = copy.deepcopy(self.LSoptions[self.G['LSvec']])
    self.LS = self.LSvec[0] 

  def SetMovieLength(self,num):
    self.G["movLength"] = num
    self.GraphParamFileOut()

  def Decades(self,num):
    self.G["decades"] = num
    self.GraphParamFileOut()

  def NumContours(self,num):
    self.G["contours"] = num
    self.GraphParamFileOut()

  def SurfaceView(self,num1,num2):
    self.G["surfaceElevation"] = num1
    self.G["surfaceAzimuth"] = num2
    self.GraphParamFileOut()

  def Points1D(self,num):
    self.G["Points1D"] = num
    self.GraphParamFileOut()

  def Points2D(self,num1,num2):
    self.G["PointsX_2D"] = num1
    self.G["PointsY_2D"] = num2
    self.GraphParamFileOut()

  def PointsX_2D(self,num):
    self.G["PointsX_2D"] = num
    self.GraphParamFileOut()

  def PointsY_2D(self,num):
    self.G["PointsY_2D"] = num
    self.GraphParamFileOut()

  def ScaleSet(self,val):
    self.G["scale"] = val 
    self.GraphParamFileOut()

  def SetNumSurfTicks(self,val):
    self.G['NumberSurfaceTicks'] = val 
    self.GraphParamFileOut()

  def ToggleSurfFormat(self):
    if(self.G['SurfaceTickFormat'] == '%0.02e'):
      self.G['SurfaceTickFormat'] = '%0.02f'
    else:
      self.G['SurfaceTickFormat'] = '%0.02e'
    self.GraphParamFileOut()


  def ToggleTitle(self):
    if(str(self.G['title']) == 'on'):
      self.G['title'] = 'off'
    else:
      self.G['title'] = 'on'
    self.GraphParamFileOut()
    print("Title Toggled: ") 

  def ToggleLegend(self):
    if(self.G['legend'] == 'on'):
      self.G['legend'] = 'off'
    else:
      self.G['legend'] = 'on'
    self.GraphParamFileOut()
    print("Legend Toggled: ") 

  def ToggleMovFormat(self):
    if(self.G['movFormat'] == 'mpeg4'):
      self.G['movFormat'] = 'wmv2'
    else:
      self.G['movFormat'] = 'mpeg4'
    self.GraphParamFileOut()

  def ToggleScale(self):
    if(str(self.G['scale']) == 'nonDim'):
      self.G['scale'] = 'noscale'
      print("Scale toggled to noscale")
    elif(str(self.G['scale']) == 'noscale'):
      self.G['scale'] = 'dimscale'
      print("Scale toggled to dimscale")
    else:
      self.G['scale'] = 'nonDim'
      print("Scale toggled to non-dimensional scale")
    self.GraphParamFileOut()

  def ToggleProcessData(self):
    if(str(self.G['process data']) == 'on'):
      self.G['process data'] = 'off'
      print("Data will not be processed")
    elif(str(self.G['process data']) == 'off'):
      self.G['process data'] = 'on'
      print("Data will be processed")
    else:
      self.G['process data'] = 'on'
      print("Data will be processed")
    self.GraphParamFileOut()

  def SetMode(self,val):
    """
    Mode settings available are
       paper:       high res figures (sizes show up as they will in a paper)  
       basic:    bigger plots for use with presentations/data visualization. 
    """

    if val ==  'paper':
      self.G["Mode"] = 'paper'
#      font = {'family' : 'sans-serif', 
#              'sans-serif' : 'Helvetica',
#              'weight' : 'bold',
#              'size' : 6}
      font = {'family' : 'sans-serif', 
              'sans-serif' : 'Helvetica',
              'weight' : 'bold',
              'size' : 8}

      rc('font',**font)
      rcParams['figure.dpi'] = 240 
#      width = 1.1*3.35; height = 1.1*1.6
      #width = 3.35; height = 1.5
      width = 3.35; height = 1.5
      rcParams['figure.figsize'] = width,height    # figure size in inches
      rcParams['lines.markersize'] = 1.2 
      #rcParams['lines.linewidth'] = 1.0
      rcParams['lines.linewidth'] = 0.75
      rcParams['xtick.major.width'] = 0.25
      rcParams['xtick.major.size'] = 4 
      #rcParams['xtick.major.size'] = 2 
      rcParams['xtick.labelsize'] = 7 
      #rcParams['xtick.labelsize'] = 6 
      rcParams['ytick.major.width'] = 0.25
      rcParams['ytick.major.size'] = 4 
      #rcParams['ytick.major.size'] = 2 
      rcParams['ytick.labelsize'] = 7 
#      rcParams['ytick.labelsize'] = 6 
      rcParams['figure.subplot.left'] =  0.2 #the left side of the subplots of the figure
      rcParams['figure.subplot.right'] = 0.8    # the right side of the subplots of the figure
      rcParams['figure.subplot.bottom'] = 0.2    # the bottom of the subplots of the figure
      rcParams['figure.subplot.top'] = 0.8 
      rcParams['figure.subplot.wspace'] = 0.2 
      rcParams['figure.subplot.hspace'] = 0.2 
      rcParams['axes.labelsize'] = 8 
#      rcParams['axes.labelsize'] = 7 
      rcParams['savefig.dpi'] = 600      # figure dots per inch
#      rcParams['legend.handlelength'] =  2.2     # the length of the legend lines in fraction of fontsize
#      rcParams['legend.handlelength'] =  2.2     # the length of the legend lines in fraction of fontsize
      rcParams['legend.handleheight'] = 0.2     # the height of the legend handle in fraction of fontsize
      rcParams['legend.handletextpad'] = 0.4    # the space between the legend line and legend text in fraction of fontsize
      rcParams['legend.handlelength'] =  1.6     # the length of the legend lines in fraction of fontsize
#      rcParams['legend.fontsize'] = 'small' 
      #rcParams['legend.numpoints'] = 3  
      rcParams['legend.numpoints'] = 1  
      rcParams['legend.fontsize'] = 'medium' 
      rcParams['legend.frameon'] = True 
      self.EvolveSize(3.35,2.0)
      self.ContourSize(width,height)
      self.WireSize(width,height)
      self.PlotSize(width,height)
      self.PlotSizeL(width,height)
      self.SurfaceSize(width,height)
      self.LogLogSize(3.35,1.5)
      self.ConvergeSize(2,2)
      self.GraphParamFileOut()

    elif val ==  'basic':
      self.G["Mode"] = 'basic'
      font = {'family' : 'sans-serif', 
              'sans-serif' : 'Helvetica',
              'weight' : 'bold',
              'size' : 16}
      rc('font',**font)
      
      rcParams['figure.dpi'] = 100 
      rcParams['axes.labelsize'] = 16 
      rcParams['xtick.labelsize'] = 14 
      rcParams['ytick.labelsize'] = 14 
      rcParams['font.weight'] = 'bold' 
      rcParams['lines.markersize'] = 2
      rcParams['lines.linewidth'] = 1.3
      rcParams['font.size'] = 16 
      rcParams['font.weight'] = 'bold' 
      rcParams['xtick.major.width'] = 1 
      rcParams['xtick.major.size'] = 4 
      rcParams['ytick.major.width'] = 1 
      rcParams['ytick.major.size'] = 4 
      rcParams['legend.fontsize'] = 'medium' 
      rcParams['legend.frameon'] = True 
      self.EvolveSize(12,8)
      self.ContourSize(12,8)
      self.WireSize(12,8)
      self.PlotSize(8,6)
      self.PlotSizeL(8,6)
      self.ConvergeSize(6,6)
      self.SurfaceSize(12,8)
      self.LogLogSize(16,5)
      self.SetLS('color')
      self.GraphParamFileOut()

    else:
      print("Did not recognize mode setting")

  def ToggleMode(self):
    """
    Mode settings available are
       paper:       high res figures (sizes show up as they will in a paper)  
       basic:    bigger plots for use with presentations/data visualization. 
    """

    item = self.ModeVec.pop(0)
    self.ModeVec.append(item)
    self.SetMode(str(self.ModeVec[0]))
    print(("Mode toggled to " + str(self.ModeVec[0])))







