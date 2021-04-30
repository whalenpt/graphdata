
from .shared1D import AuxPlotLabel1D 
from .shared1D import AuxPlotLabelLL1D 
from .shared1D import ProcessData1D 
from .aux import GenFileList 
from .aux import GetData1D 
from .aux import GetFileData1D 
import os 
from GraphData3 import pl
from GraphData3 import np 
from GraphData3 import configs 
from pprint import pprint

def Plot(*args,**kwargs):
  """

  Plot of 1D data. 

  Plot(fileID,fileNumber,plotLimits):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
      fileID is simply 'T'

    fileNumber: Specifies which data file number to plot 
      e.g.  Plot('T',10) will make a plot of the data file 'T_10.dat' if this
      data file is available

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, or contain all
      limits
        e.g. Plot('T',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. Plot('T',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. Plot('T',10,[]) is the same as Plot('T',10)

  """

  
  x,y,auxDict = GetData1D(*args)
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _PlotSize(**kwargs)
  p = pl.figure(figsize=(width,height))
  configs.DefaultLS()

  pl.plot(x,y,configs.LS)
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  if 'legend' in auxDict and configs.G['legend'] == 'on':
    pl.legend([str(auxDict["legend"])],loc='best')
  pl.ion()
  pl.show()
  return p

def PlotH(*args,**kwargs):
  """
  Plot of 1D data. The functions PlotH and Plot differ only in that PlotH will
  plot on top of existing data plots created using PlotH.

  PlotH(fileID,fileNumber,plotLimits,figSize,lineStyle):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
      fileID is simply 'T'

    fileNumber: Specifies which data file number to plot 
      e.g.  PlotH('T',10) will make a plot of the data file 'T_10.dat' if this
      data file is available

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the Surface plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, or contain all
      limits
        e.g. PlotH('T',10,[0,1]) will plot data with x-limits between 0 and 1
        e.g. PlotH('T',10,[0,1,-2,2]) will plot data with x-limits between 0
        and 1 and y-limits between -2 and 2.  
        e.g. PlotH('T',10,[]) is the same as Plot('T',10)

    figSize: [width,height]
      Width and height should be specified in inches. 
      The default figure size is configsored in the settings object under
      configs.G['PlotWidth'] and configs.G['PlotHeight']

    lineStyle: colors, e.g. 'k','b','r','g',etc. and
               marker, e.g. '--','-.','.','s','d','o'
      eg. 'k--' is a black dashed line
      eg. 'ro' plots individual points in the color red 

  """

  x,y,auxDict = GetData1D(*args)
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
#  y = y/1.0e4
  labs = pl.get_figlabels() 
  if "PlotH" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  width,height = _PlotSize(**kwargs)
  p = pl.figure("PlotH",figsize=(width,height))

  ax = pl.gca()
  ax.xaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.yaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))

  if(configs.LS == 'k--'):
    pl.plot(x,y,configs.LS,dashes = (4,2))
  else:
    pl.plot(x,y,configs.LS)

  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  pl.hold(True) 
  pl.ion()
  pl.show()
  return p 

def PlotL(*args,**kwargs):
  """
  Semilogy  plot of 1D data. 

  PlotL(fileID,fileNumber,plotLimits,numDecades):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
      fileID is simply 'T'

    fileNumber: Specifies which data file number to plot 
      e.g.  PlotL('T',10) will make a plot of the data file 'T_10.dat' if this
      data file is available

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
    numDecades:
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. PlotL('T',10,[0,1]) will plot data with x-limits between 0 and 1
        e.g. PlotL('T',10,[0,1,1,1e10]) will plot data with x-limits between 0
        and 1 and y-limits between 1 and 1e10.  
        e.g. PlotL('T',10,[0,1],5) will plot data with x-limits between 0
        and 1 and 5 decades of y-data.  
        e.g. PlotL('T',10,[]) is the same as Plot('T',10)

  """
 
  x,y,auxDict = GetData1D(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _PlotSizeL(**kwargs)
  pl.figure(figsize=(width,height))
  configs.DefaultLS()
  pl.semilogy(x,y,configs.LS)
  pl.grid(True)
  AuxPlotLabel1D(auxDict)
  if 'legend' in auxDict and configs.G['legend'] == 'on':
    pl.legend([str(auxDict["legend"])],loc='best')
  
  pl.xlim([x[0],x[-1]])
  pl.ion()
  pl.show()
  return True

def PlotLH(*args,**kwargs):
  """
  See PlotHL
  """
  PlotHL(args)

def PlotHL(*args,**kwargs):

  """
  Semilogy plot of 1D data. The functions PlotHL and PlotL differ only in that
  PlotHL will plot on top of existing data while PlotL creates a new figure.

  PlotL(fileID,fileNumber,plotLimits):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
      fileID is simply 'T'

    fileNumber: Specifies which data file number to plot 
      e.g.  PlotL('T',10) will make a plot of the data file 'T_10.dat' if this
      data file is available

    plotLimits = [minX,maxX,numDecades]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. PlotL('T',10,[0,1]) will plot data with x-limits between 0 and 1
        e.g. PlotL('T',10,[0,1,20]) will plot data with x-limits between 0
        and 1 and 20 decades of output y-data.  
        e.g. PlotL('T',10,[]) is the same as Plot('T',10)

  """
 
  x,y,auxDict = GetData1D(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  labs = pl.get_figlabels() 
  if "PlotHL" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  width,height = _PlotSizeL(**kwargs)
  pl.figure("PlotHL",figsize=(width,height))
  pl.semilogy(x,y,configs.LS)
#  pl.semilogy(x,y,'b--',dashes = (2,1))
#  pl.semilogy(x,y,'ko',markevery=50,markersize=1.5)
#  pl.semilogy(x,y,'rs',markevery=30,markersize=1.5)
#  pl.semilogy(x,y,'k-',dashes = (2,2))
#  pl.semilogy(x,y,'r')
#  pl.semilogy(x,y,'b')
  pl.grid(True)
  pl.hold(True) 
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  pl.ion()
  pl.show()
  return True

def PlotF(*args,**kwargs):
  """

  Plot of 1D data. 

  PlotF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. PlotF('DataFileX.dat') makes a 1D plot of the x-y data.

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, or contain all
      limits
        e.g. PlotF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1 
        e.g. PlotF('DataFileX.dat',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 

  """

  x,y,auxDict = GetFileData1D(*args)
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  y = y/1.0e4
  width,height = _PlotSize(**kwargs)
  pl.figure(figsize=(width,height))
  configs.DefaultLS()
  pl.plot(x,y,configs.LS)
  if 'mirror vertical' in auxDict:
    pl.plot(x,-y,configs.LS)
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  if 'legend' in auxDict and configs.G['legend'] == 'on':
    pl.legend([str(auxDict["legend"])],loc='best')
  pl.ion()
  pl.show()
  return True

def PlotHF(*args,**kwargs):
  """

  Plot of 1D data in figure window 'PlotHF'. Will plot over previous results

  PlotHF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. PlotF('DataFileX.dat') makes a 1D plot of the x-y data.

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, or contain all
      limits
        e.g. PlotF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1 
        e.g. PlotF('DataFileX.dat',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 

  """

  x,y,auxDict = GetFileData1D(*args)
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
#  y = y/1.0e4
  labs = pl.get_figlabels() 
  if "PlotHF" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()

  width,height = _PlotSize(**kwargs)
  p = pl.figure("PlotHF",figsize=(width,height))
  pl.plot(x,y,configs.LS)

  if 'mirror vertical' in auxDict:
    pl.plot(x,-y,configs.LS)

#  pl.plot(x,y,'bo',mfc='b',markeredgecolor = 'b',markevery=40,fillstyle='full')
#  pl.plot(x,y,'b',dashes=(1,2,3,2))
#  pl.plot(x,y,'r')
#  pl.plot(x,y,'k',dashes = (2,2))

  pl.hold(True) 
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  pl.ion()
  pl.show()
  return p 

def PlotLF(*args,**kwargs):
  """
  Semilogy  plot of 1D data. 

  PlotLF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. PlotLF('DataFileX.dat') makes a semilofy 1D plot of the x-y data.

    plotLimits = [minX,maxX,numDecades]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. PlotLF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1
        e.g. PlotLF('DataFileX.dat',[0,1,20]) will plot data with x-limits between 0
        and 1 and 20 decades of output y-data.  

  """
 
  x,y,auxDict = GetFileData1D(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _PlotSizeL(**kwargs)
  pl.figure(figsize=(width,height))
  configs.DefaultLS()
  pl.semilogy(x,y,configs.LS)
  pl.grid(True)
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  if 'legend' in auxDict and configs.G['legend'] == 'on':
    pl.legend([str(auxDict["legend"])],loc='best')
  pl.ion()
  pl.show()
  return True

def PlotHLF(*args,**kwargs):
  """
  Semilogy  plot of 1D data in figure window 'PlotHLF'.
  Plots over previous results.

  PlotHLF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. PlotLF('DataFileX.dat') makes a semilofy 1D plot of the x-y data.

    plotLimits = [minX,maxX,numDecades]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. PlotLF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1
        e.g. PlotLF('DataFileX.dat',[0,1,20]) will plot data with x-limits between 0
        and 1 and 20 decades of output y-data.  

  """
 
  x,y,auxDict = GetFileData1D(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)

#  y = y/1.0e6
  labs = pl.get_figlabels() 
  if "PlotHLF" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  width,height = _PlotSizeL(**kwargs)
  pl.figure("PlotHLF",figsize=(width,height))
  pl.semilogy(x,y,configs.LS)

#  pl.semilogy(x,y,'b',dashes=(1,2,3,2))
#  pl.semilogy(x,y,'r')
#  pl.semilogy(x,y,'k',dashes=(2,2))

  ax = pl.gca()
  ax.xaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.yaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))

  pl.hold(True) 
  AuxPlotLabel1D(auxDict)
  pl.xlim([x[0],x[-1]])
  pl.ion()
  pl.show()
  return True

def _PlotSize(**kwargs):

  width = float(configs.G['PlotWidth'])
  height = float(configs.G['PlotHeight'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  return (width,height) 

def _PlotSizeL(**kwargs):
  width = float(configs.G['PlotWidthL'])
  height = float(configs.G['PlotHeightL'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  return (width,height) 

def LogLogF(*args,**kwargs):
  """
  LogLog plot of 1D data. 

  LogLogF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. LogLogF('DataFileX.dat') makes a loglog 1D plot of the x-y data.

    plotLimits = [minX,maxX,numDecades]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. LogLogF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1
        e.g. LogLogF('DataFileX.dat',[0,1,20]) will plot data with x-limits between 0
        and 1 and 20 decades of output y-data.  

  """
 
  x,y,auxDict = GetFileData(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width = float(configs.G['LogLogWidth'])
  height = float(configs.G['LogLogHeight'])
  p = pl.figure(figsize=(width,height))
  configs.DefaultLS()
  pl.loglog(x,y,configs.LS)
  pl.grid(True)
  AuxPlotLabelLL1D(auxDict)
  pl.ion()
  pl.show()
  return p 

def LogLogHF(*args,**kwargs):
  """
  LogLog plot of 1D data. 

  LogLogF(fileName,plotLimits):
  Args:
    fileName: Name of data file with two columns of 1D x-y data 
      e.g. LogLogF('DataFileX.dat') makes a loglog 1D plot of the x-y data.

    plotLimits = [minX,maxX,numDecades]
    plotLimits: Specifies the plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      numDecades: Number of decades of data below maximum to plot

      If no plotLimit list is given, then the graph x-limits will depend on the
      minimum and maximum input data and the y-limits will depend on the
      default number of decades.  The plotLimits list can be empty, contain
      just xmin and xmax limits, or contain all limits

        e.g. LogLogF('DataFileX.dat',[0,1]) will plot data with x-limits between 0 and 1
        e.g. LogLogF('DataFileX.dat',[0,1,20]) will plot data with x-limits between 0
        and 1 and 20 decades of output y-data.  

  """
 
  x,y,auxDict = GetFileData(*args)
  auxDict['decades'] = configs.G['decades']
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width = float(configs.G['LogLogWidth'])
  height = float(configs.G['LogLogHeight'])
  labs = pl.get_figlabels() 

  if "LogLogHF" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  p = pl.figure("LogLogHF",figsize=(width,height))

  x = x/1.0e4
#  pl.loglog(x,y,'r')
#  pl.loglog(x,y,'k',dashes=(3,3))
#  pl.loglog(x,y,'b',dashes=(1,2,3,2))

  pl.loglog(x,y,configs.LS)
  ax = pl.gca()
  ax.xaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.yaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))

  AuxPlotLabelLL1D(auxDict)
  pl.ion()
  pl.show()
  return p 



