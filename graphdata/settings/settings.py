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
        self._G = self.loadsettings()
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
        self.legendList = []
        self._modeVec = ['basic','paper']
        self.setMode(self._G["Mode"])
    @property
    def LS(self):
        return self._LS
    @LS.setter
    def LS(self,val):
        self._LS = val

    def _loadDefaultsettings(self):
        default_dict = {'points1D': 200,'pointsX_2D':100,'pointsY_2D':100,\
          'scale':'noscale','xdimscale':1.0,'ydimscale':1.0,'zdimscale':1.0,\
          'tdimscale':1.0,'xdimscale_str':'','ydimscale_str':'','zdimscale_str':'',\
          'tdimscale_str':'', 'process data':'on',\
          'LSvec':'color','cmap':'hot','title':'on','legend':'on',\
          'movFormat':'wmv2','movLength':10.0,\
          'elev':30,'azim' : -120,'decades' : 12, 'contours' : 20, \
          'FigWidth':14,'FigHeight':8,'FigWidthL':15,'FigHeightL':5,\
          'PlotWidth':14,'PlotHeight':8,'SemilogyWidth':15,'SemilogyHeight':5,\
          'LogLogWidth':14,'LogLogHeight':8,\
          'SurfaceTickFormat':'%0.02e','NumberSurfaceTicks':6,'SurfaceTickFormat':'%0.02e',\
          'SurfaceWidth':8,'SurfaceHeight':8,\
          'WireframeHeight':8,'WireframeWidth':8,\
          'WaterfallHeight':8,'WaterfallWidth':8,\
          'ContourfHeight':6,'ContourfWidth':15,\
          'WireframeLogHeight':5,'WireframeLogWidth':16,\
          'Mode':'basic'}
        return default_dict

    def loadsettings(self):
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
            configs = self._loadDefaultsettings()
            os.makedirs(pr_dir,exist_ok=True)
            with open(pr_file,'w') as outfile:
                json.dump(configs,outfile)
        return configs

    def scale(self):
        return self._G['scale']

    def settingsDict(self):
        return self._G

    def displaysettings(self):
      for key in sorted(self._G.keys()):
          print((key + ":" + " "*8 + str(self._G[key])))

    def _writesettings(self):
      """ Writes a json configuration file. """
      hm = os.environ.get("HOME")
      pr_file = os.path.join(hm,'.config','graphdata','settings.conf')
      with open(pr_file,'w') as outfile:
          json.dump(self._G,outfile)

    def _processScale(self,scale):
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

    def scaleX(self,scale):
      scale_str, scale_val = self._processScale(scale)
      self._G['xdimscale'] = scale_val
      self._G['xdimscale_str'] = scale_str
      self._writesettings()

    def scaleY(self,scale):
      scale_str, scale_val = self._processScale(scale)
      self._G['ydimscale'] = scale_val
      self._G['ydimscale_str'] = scale_str
      self._writesettings()
    def scaleZ(self,scale):
      scale_str, scale_val = self._processScale(scale)
      self._G['zdimscale'] = scale_val
      self._G['zdimscale_str'] = scale_str
      self._writesettings()
    def scaleT(self,scale):
      scale_str, scale_val = self._processScale(scale)
      self._G['tdimscale'] = scale_val
      self._G['tdimscale_str'] = scale_str
      self._writesettings()

    def addLegend(self,name):
      self.legendList.append(name)

    def setLegend(self,name):
      self.legendList = []
      self.legendList.append(name)

    def contourSize(self,w,h):
      self._G["ContourWidth"] = w
      self._G["ContourHeight"] = h
      self._writesettings()

    def evolveSize(self,w,h):
      self._G["EvolveWidth"] = w
      self._G["EvolveHeight"] = h
      self._writesettings()

    def evolveSizeL(self,w,h):
      self._G["EvolveWidthL"] = w
      self._G["EvolveHeightL"] = h
      self._writesettings()

    def surfaceSize(self,w,h):
      self._G["SurfaceWidth"] = w
      self._G["SurfaceHeight"] = h
      self._writesettings()

    def waterfallSize(self,w,h):
      self._G["WaterfallWidth"] = w
      self._G["WaterfallHeight"] = h
      self._writesettings()


    def plotSize(self,w,h):
      self._G["PlotWidth"] = w
      self._G["PlotHeight"] = h
      self._writesettings()

    def plotSizeL(self,w,h):
      self._G["PlotWidthL"] = w
      self._G["PlotHeightL"] = h
      self._writesettings()

    def wireSize(self,w,h):
      self._G["WireWidth"] = w
      self._G["WireHeight"] = h
      self._writesettings()

    def loglogSize(self,w,h):
      self._G["LogLogWidth"] = w
      self._G["LogLogHeight"] = h
      self._writesettings()

    def toggleLS(self):
      item = self._LSvec.pop(0)
      self._LSvec.append(item)
      self._LS = self._LSvec[0]
      print("Line style toggled to '{}'".format(self._LS))

    def toggleCmap(self):
      item = self._cmapvec.pop(0)
      self._cmapvec.append(item)
      self._G["cmap"] = str(self._cmapvec[0])
      print(("Colormap toggled to " + str(self._G["cmap"])))
      self._writesettings()

    def setCmap(self,val):
      """
      Cmap styles:  hot,jet,bone,gray,binary,gist_yarg,etc.
      """
      self._G["cmap"] = val 
      print(("Colormap set to " + str(self._G["cmap"])))
      self._writesettings()

    def setLS(self,key):
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
        self._writesettings()
        self.defaultLS()
      else:
        print("Did not recognize linestyles. Here is a list of the options: ")
        print(('\n'.join("%s:\t\t %s" % (kkey, ','.join(map(str, values))) for kkey, values in list(self._LSoptions.items()))))

    def defaultLS(self):
      self._LSvec = copy.deepcopy(self._LSoptions[self._G['LSvec']])
      self._LS = self._LSvec[0]

    def setMovieLength(self,num):
      self._G["movLength"] = num
      self._writesettings()

    def decades(self,num):
      self._G["decades"] = num
      self._writesettings()

    def numContours(self,num):
      self._G["contours"] = num
      self._writesettings()

    def surfaceView(self,elev,azim):
      self._G["elev"] = elev
      self._G["azim"] = azim
      self._writesettings()

    def points1D(self,num):
      self._G["points1D"] = num
      self._writesettings()

    def points2D(self,num1,num2):
      self._G["pointsX_2D"] = num1
      self._G["pointsY_2D"] = num2
      self._writesettings()

    def pointsX_2D(self,num):
      self._G["pointsX_2D"] = num
      self._writesettings()

    def pointsY_2D(self,num):
      self._G["pointsY_2D"] = num
      self._writesettings()

    def scaleset(self,val):
      self._G["scale"] = val
      self._writesettings()

    def setNumSurfTicks(self,val):
      self._G['NumberSurfaceTicks'] = val
      self._writesettings()

    def toggleSurfFormat(self):
      if(self._G['SurfaceTickFormat'] == '%0.02e'):
        self._G['SurfaceTickFormat'] = '%0.02f'
      else:
        self._G['SurfaceTickFormat'] = '%0.02e'
      self._writesettings()


    def toggleTitle(self):
        if(str(self._G['title']) == 'on'):
            self._G['title'] = 'off'
            print('Figure title toggled off')
        else:
            self._G['title'] = 'on'
            print('Figure title toggled on')
        self._writesettings()

    def toggleLegend(self):
        if(self._G['legend'] == 'on'):
            self._G['legend'] = 'off'
            print('Legend toggled off')
        else:
            self._G['legend'] = 'on'
            print('Legend toggled on')
        self._writesettings()


    def toggleMovFormat(self):
        if(self._G['movFormat'] == 'mpeg4'):
            self._G['movFormat'] = 'wmv2'
        else:
            self._G['movFormat'] = 'mpeg4'
        self._writesettings()

    def toggleScale(self):
        if(str(self._G['scale']) == 'nonDim'):
            self._G['scale'] = 'noscale'
            print("Scale toggled to noscale")
        elif(str(self._G['scale']) == 'noscale'):
            self._G['scale'] = 'dimscale'
            print("Scale toggled to dimscale")
        else:
            self._G['scale'] = 'nonDim'
            print("Scale toggled to non-dimensional scale")
        self._writesettings()

    def toggleProcessData(self):
        if(str(self._G['process data']) == 'on'):
            self._G['process data'] = 'off'
            print("Data will not be processed")
        elif(str(self._G['process data']) == 'off'):
            self._G['process data'] = 'on'
            print("Data will be processed")
        else:
            self._G['process data'] = 'on'
            print("Data will be processed")
        self._writesettings()

    def setMode(self,val):
        """
        Mode settings available are
           paper:       high res figures (sizes show up as they will in a paper)
           basic:    bigger plots for use with presentations/data visualization.
        """

        if val ==  'paper':
            self._setPaperMode()
            self._writesettings()
        elif val ==  'basic':
            self._setBasicMode()
            self._writesettings()
        else:
            print("Did not recognize mode setting")

    def _setPaperMode(self):
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
        self.evolveSize(3.35,2.0)
        self.contourSize(width,height)
        self.wireSize(width,height)
        self.plotSize(width,height)
        self.plotSizeL(width,height)
        self.surfaceSize(width,height)
        self.loglogSize(3.35,1.5)

    def _setBasicMode(self):
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
        self.evolveSize(12,8)
        self.contourSize(12,8)
        self.wireSize(12,8)
        self.plotSize(8,6)
        self.plotSizeL(8,6)
        self.surfaceSize(12,8)
        self.loglogSize(16,5)
        self.setLS('color')

    def toggleMode(self):
        """
        Mode settings available are
           paper:       high res figures (sizes show up as they will in a paper)
           basic:    bigger plots for use with presentations/data visualization.
        """

        item = self._modeVec.pop(0)
        self._modeVec.append(item)
        self.setMode(str(self._modeVec[0]))
        print(("Mode toggled to " + str(self._modeVec[0])))







