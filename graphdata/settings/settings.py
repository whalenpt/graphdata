# Filename: settings.py

import os
import sys
import copy
import json
from matplotlib import rc,rcParams
from pathlib import Path

class PlotSettings(object):
    """ Class which holds configuration settings for graphdata."""

    def __init__(self):
        self._G = self.LoadSettings()
        self._LSoptions = {'basic':['k-o','k--d','k-.s','r-o','r--d','r-.s'],\
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
        self._LSvec = copy.deepcopy(self._LSoptions[self._G['LSvec']])
        self._LS = self._LSvec[0] 
        self._cmapvec = ['hot','jet','bone','gray','binary','gist_yarg']
        self.LegendList = []
        self._ModeVec = ['basic','paper']
        self.SetMode(self._G["Mode"])
    @property
    def LS(self):
        return self._LS
    @LS.setter
    def LS(self,val):
        self._LS = val

    def _LoadDefaultSettings(self):
        default_dict = {'Points1D': 200,'PointsX_2D':100,'PointsY_2D':100,\
          'scale':'noscale','xdimscale':1.0,'ydimscale':1.0,'zdimscale':1.0,\
          'tdimscale':1.0,'xdimscale_str':'','ydimscale_str':'','zdimscale_str':'',\
          'tdimscale_str':'', 'process data':'on',\
          'LSvec':'color','cmap':'hot','title':'on','legend':'on',\
          'movFormat':'wmv2','movLength':10.0,\
          'FigWidth':14,'FigHeight':8,'FigWidthL':15,'FigHeightL':5,\
          'PlotWidth':14,'PlotHeight':8,'SemilogyWidth':15,'SemilogyHeight':5,\
          'LogLogWidth':14,'LogLogHeight':8,\
          'SurfaceTickFormat':'%0.02e','NumberSurfaceTicks':6,'SurfaceTickFormat':'%0.02e',\
          'SurfaceWidth':8,'SurfaceHeight':8,'WireframeHeight':8,'WireframeWidth':8,\
          'ContourfHeight':6,'ContourfWidth':15,'contours':50,\
          'WireframeLogHeight':5,'WireframeLogWidth':16,\
          'decades':12,\
          'Mode':'basic'}
        return default_dict

    def LoadSettings(self):
        """ Internal function which sets configuration dictionary by
            loading values from $HOME/.configs/graphdata/graphdata.conf or
            using specified default values.

            OUTPUTS:
                configs : dict
                    dictionary of configuration values. 
        """
        configs = dict()
        hm = os.environ.get("HOME")
        pr_dir = os.path.join(hm,'.config','graphdata')
        pr_file = os.path.join(pr_dir,'settings.conf')
        try:
            with open(pr_file) as f:
                configs = json.load(f)
        except IOError as e:
            configs = self._LoadDefaultSettings()
            os.makedirs(pr_dir,exist_ok=True)
            with open(pr_file,'w') as outfile:
                json.dump(configs,outfile)
        return configs

    def scale(self):
        return self._G['scale']

    def SettingsDict(self):
        return self._G

    def DisplaySettings(self):
      for key in sorted(self._G.keys()):
          print((key + ":" + " "*8 + str(self._G[key])))

    def _WriteSettings(self):
      """ Writes a json configuration file. """
      hm = os.environ.get("HOME")
      pr_file = os.path.join(hm,'.config','graphdata','settings.conf')
      with open(pr_file,'w') as outfile:
          json.dump(self._G,outfile)

    def _ProcessScale(self,scale):
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
      scale_str, scale_val = self._ProcessScale(scale)
      self._G['xdimscale'] = scale_val
      self._G['xdimscale_str'] = scale_str
      self._WriteSettings()

    def ScaleY(self,scale):
      scale_str, scale_val = self._ProcessScale(scale)
      self._G['ydimscale'] = scale_val
      self._G['ydimscale_str'] = scale_str
      self._WriteSettings()
    def ScaleZ(self,scale):
      scale_str, scale_val = self._ProcessScale(scale)
      self._G['zdimscale'] = scale_val
      self._G['zdimscale_str'] = scale_str
      self._WriteSettings()
    def ScaleT(self,scale):
      scale_str, scale_val = self._ProcessScale(scale)
      self._G['tdimscale'] = scale_val
      self._G['tdimscale_str'] = scale_str
      self._WriteSettings()

    def AddLegend(self,name):
      self.LegendList.append(name)

    def SetLegend(self,name):
      self.LegendList = []
      self.LegendList.append(name)

    def ContourSize(self,w,h):
      self._G["ContourWidth"] = w
      self._G["ContourHeight"] = h
      self._WriteSettings()

    def EvolveSize(self,w,h):
      self._G["EvolveWidth"] = w
      self._G["EvolveHeight"] = h
      self._WriteSettings()

    def EvolveSizeL(self,w,h):
      self._G["EvolveWidthL"] = w
      self._G["EvolveHeightL"] = h
      self._WriteSettings()

    def SurfaceSize(self,w,h):
      self._G["SurfaceWidth"] = w
      self._G["SurfaceHeight"] = h
      self._WriteSettings()

    def PlotSize(self,w,h):
      self._G["PlotWidth"] = w
      self._G["PlotHeight"] = h
      self._WriteSettings()

    def PlotSizeL(self,w,h):
      self._G["PlotWidthL"] = w
      self._G["PlotHeightL"] = h
      self._WriteSettings()

    def WireSize(self,w,h):
      self._G["WireWidth"] = w
      self._G["WireHeight"] = h
      self._WriteSettings()

    def LogLogSize(self,w,h):
      self._G["LogLogWidth"] = w
      self._G["LogLogHeight"] = h
      self._WriteSettings()

    def ConvergeSize(self,w,h):
      self._G["ConvergeWidth"] = w
      self._G["ConvergeHeight"] = h
      self._WriteSettings()

    def ToggleLS(self):
      item = self._LSvec.pop(0)
      self._LSvec.append(item)
      self._LS = self._LSvec[0]
      print("Line style toggled to '{}'".format(self._LS))

    def ToggleCmap(self):
      item = self._cmapvec.pop(0)
      self._cmapvec.append(item)
      self._G["cmap"] = str(self._cmapvec[0])
      print(("Colormap toggled to " + str(self._G["cmap"])))
      self._WriteSettings()

    def SetCmap(self,val):
      """
      Cmap styles:  hot,jet,bone,gray,binary,gist_yarg,etc.
      """
      self._G["cmap"] = val 
      print(("Colormap set to " + str(self._G["cmap"])))
      self._WriteSettings()

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
      if key in self._LSoptions:
        self._G['LSvec'] = key
        self._WriteSettings()
        self.DefaultLS()
      else:
        print("Did not recognize linestyles. Here is a list of the options: ")
        print(('\n'.join("%s:\t\t %s" % (kkey, ','.join(map(str, values))) for kkey, values in list(self._LSoptions.items()))))

    def DefaultLS(self):
      self._LSvec = copy.deepcopy(self._LSoptions[self._G['LSvec']])
      self._LS = self._LSvec[0]

    def SetMovieLength(self,num):
      self._G["movLength"] = num
      self._WriteSettings()

    def Decades(self,num):
      self._G["decades"] = num
      self._WriteSettings()

    def NumContours(self,num):
      self._G["contours"] = num
      self._WriteSettings()

    def SurfaceView(self,num1,num2):
      self._G["surfaceElevation"] = num1
      self._G["surfaceAzimuth"] = num2
      self._WriteSettings()

    def Points1D(self,num):
      self._G["Points1D"] = num
      self._WriteSettings()

    def Points2D(self,num1,num2):
      self._G["PointsX_2D"] = num1
      self._G["PointsY_2D"] = num2
      self._WriteSettings()

    def PointsX_2D(self,num):
      self._G["PointsX_2D"] = num
      self._WriteSettings()

    def PointsY_2D(self,num):
      self._G["PointsY_2D"] = num
      self._WriteSettings()

    def ScaleSet(self,val):
      self._G["scale"] = val
      self._WriteSettings()

    def SetNumSurfTicks(self,val):
      self._G['NumberSurfaceTicks'] = val
      self._WriteSettings()

    def ToggleSurfFormat(self):
      if(self._G['SurfaceTickFormat'] == '%0.02e'):
        self._G['SurfaceTickFormat'] = '%0.02f'
      else:
        self._G['SurfaceTickFormat'] = '%0.02e'
      self._WriteSettings()


    def ToggleTitle(self):
        if(str(self._G['title']) == 'on'):
            self._G['title'] = 'off'
            print('Figure title toggled off')
        else:
            self._G['title'] = 'on'
            print('Figure title toggled on')
        self._WriteSettings()

    def ToggleLegend(self):
        if(self._G['legend'] == 'on'):
            self._G['legend'] = 'off'
            print('Legend toggled off')
        else:
            self._G['legend'] = 'on'
            print('Legend toggled on')
        self._WriteSettings()


    def ToggleMovFormat(self):
        if(self._G['movFormat'] == 'mpeg4'):
            self._G['movFormat'] = 'wmv2'
        else:
            self._G['movFormat'] = 'mpeg4'
        self._WriteSettings()

    def ToggleScale(self):
        if(str(self._G['scale']) == 'nonDim'):
            self._G['scale'] = 'noscale'
            print("Scale toggled to noscale")
        elif(str(self._G['scale']) == 'noscale'):
            self._G['scale'] = 'dimscale'
            print("Scale toggled to dimscale")
        else:
            self._G['scale'] = 'nonDim'
            print("Scale toggled to non-dimensional scale")
        self._WriteSettings()

    def ToggleProcessData(self):
        if(str(self._G['process data']) == 'on'):
            self._G['process data'] = 'off'
            print("Data will not be processed")
        elif(str(self._G['process data']) == 'off'):
            self._G['process data'] = 'on'
            print("Data will be processed")
        else:
            self._G['process data'] = 'on'
            print("Data will be processed")
        self._WriteSettings()

    def SetMode(self,val):
        """
        Mode settings available are
           paper:       high res figures (sizes show up as they will in a paper)
           basic:    bigger plots for use with presentations/data visualization.
        """

        if val ==  'paper':
            self._SetPaperMode()
            self._WriteSettings()
        elif val ==  'basic':
            self._SetBasicMode()
            self._WriteSettings()
        else:
            print("Did not recognize mode setting")

    def _SetPaperMode(self):
        self._G["Mode"] = 'paper'
        font = {'family' : 'sans-serif',
                'sans-serif' : 'Helvetica',
                'weight' : 'bold',
                'size' : 6}
        font = {'family' : 'sans-serif',
               'sans-serif' : 'Helvetica',
               'weight' : 'bold',
               'size' : 8}

        rc('font',**font)
        rcParams['figure.dpi'] = 240 
        width = 1.1*3.35; height = 1.1*1.6
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
        rcParams['ytick.labelsize'] = 6 
        rcParams['figure.subplot.left'] =  0.2 #the left side of the subplots of the figure
        rcParams['figure.subplot.right'] = 0.8    # the right side of the subplots of the figure
        rcParams['figure.subplot.bottom'] = 0.2    # the bottom of the subplots of the figure
        rcParams['figure.subplot.top'] = 0.8 
        rcParams['figure.subplot.wspace'] = 0.2 
        rcParams['figure.subplot.hspace'] = 0.2 
        rcParams['axes.labelsize'] = 8 
        rcParams['axes.labelsize'] = 7 
        rcParams['savefig.dpi'] = 600      # figure dots per inch
        rcParams['legend.handlelength'] =  2.2     # the length of the legend lines in fraction of fontsize
        rcParams['legend.handlelength'] =  2.2     # the length of the legend lines in fraction of fontsize
        rcParams['legend.handleheight'] = 0.2     # the height of the legend handle in fraction of fontsize
        rcParams['legend.handletextpad'] = 0.4    # the space between the legend line and legend text in fraction of fontsize
        rcParams['legend.handlelength'] =  1.6     # the length of the legend lines in fraction of fontsize
        rcParams['legend.fontsize'] = 'small' 
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

    def _SetBasicMode(self):
        self._G["Mode"] = 'basic'
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

    def ToggleMode(self):
        """
        Mode settings available are
           paper:       high res figures (sizes show up as they will in a paper)
           basic:    bigger plots for use with presentations/data visualization.
        """

        item = self._ModeVec.pop(0)
        self._ModeVec.append(item)
        self.SetMode(str(self._ModeVec[0]))
        print(("Mode toggled to " + str(self._ModeVec[0])))







