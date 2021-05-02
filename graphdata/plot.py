
from graphdata.shared.shared1D import AuxPlotLabel1D 
from graphdata.shared.shared1D import AuxPlotLabelLL1D 
from graphdata.shared.shared1D import ProcessData1D 
from graphdata.shared.shared1D import GetData1D 
import os 
from graphdata import plt
from graphdata import np 
from graphdata import configs 

def plot(fileID,fileNumber=None,**kwargs):
  """

  Plot of 1D data. 

  Plot(fileID,**kwargs):
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

  x,y,auxDict = GetData1D(fileID,fileNumber)
  if 'xlim' in kwargs:
      auxDict['xlim'] = kwargs['xlim']
  else: 
      auxDict['xlim'] = [x[0],x[-1]]
  if 'ylim' in kwargs:
      auxDict['ylim'] = kwargs['ylim']
  else: 
      auxDict['ylim'] = [np.min(y),np.max(y)]

  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _PlotSize(**kwargs)
  labs = plt.get_figlabels() 

  if 'overwrite' in kwargs and kwargs['overwrite']:
      if "Plot" not in labs:
          configs.DefaultLS()
      else:
          configs.ToggleLS()
      fig = plt.figure("Plot",figsize=(width,height))
      if(configs.LS == 'k--'):
          plt.plot(x,y,configs.LS,dashes = (4,2))
      else:
          plt.plot(x,y,configs.LS)
  else:
      fig = plt.figure(figsize=(width,height))
      configs.DefaultLS()
      plt.plot(x,y,configs.LS)

  AuxPlotLabel1D(auxDict)
  plt.xlim([x[0],x[-1]])
  if 'legend' in auxDict and configs._G['legend'] == 'on':
      plt.legend([str(auxDict["legend"])],loc='best')
  plt.ion()
  plt.show()
  ax = plt.gca()
  return ax

def semilogy(*args,**kwargs):
  """
  Semilog plot of 1D data with log taken in y-axis. 

  semilogy(fileID,fileNumber,plotLimits,numDecades):
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
  auxDict['decades'] = configs._G['decades']
  if 'xlim' in kwargs:
      auxDict['xlim'] = kwargs['xlim']
  else: 
      auxDict['xlim'] = [x[0],x[-1]]
  if 'ylim' in kwargs:
      auxDict['ylim'] = kwargs['ylim']
  else: 
      auxDict['ylim'] = [np.min(y),np.max(y)]
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _SemilogySize(**kwargs)
  if 'overwrite' in kwargs and kwargs['overwrite']:
      labs = plt.get_figlabels() 
      if "Semilogy" not in labs:
        configs.DefaultLS()
      else:
        configs.ToggleLS()
      plt.figure("Semilogy",figsize=(width,height))
  else:
      configs.DefaultLS()
      plt.figure(figsize=(width,height))

  plt.semilogy(x,y,configs.LS)
  plt.grid(True)
  AuxPlotLabel1D(auxDict)
  if 'legend' in auxDict and configs._G['legend'] == 'on':
    plt.legend([str(auxDict["legend"])],loc='best')
  
  plt.xlim([x[0],x[-1]])
  plt.ion()
  plt.show()
  ax = plt.gca()
  return ax

def _PlotSize(**kwargs):
    if 'figsize' in kwargs:
        return kwargs['figsize']
    return (float(configs._G['PlotWidth']),float(configs._G['PlotHeight']))

def _SemilogySize(**kwargs):
    if 'figsize' in kwargs:
        return kwargs['figsize']
    return (float(configs._G['SemilogyWidth']),float(configs._G['SemilogyHeight']))

def _LogLogSize(**kwargs):
    if 'figsize' in kwargs:
        return kwargs['figsize']
    return (float(configs._G['LogLogWidth']),float(configs._G['LogLogHeight']))

def loglog(*args,**kwargs):
  """
  LogLog plot of 1D data. 

  LogLog(fileName,plotLimits):
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
 
  x,y,auxDict = GetData1D(*args)
  auxDict['decades'] = configs._G['decades']
  if 'xlim' in kwargs:
      auxDict['xlim'] = kwargs['xlim']
  else: 
      auxDict['xlim'] = [x[0],x[-1]]
  if 'ylim' in kwargs:
      auxDict['ylim'] = kwargs['ylim']
  else: 
      auxDict['ylim'] = [np.min(y),np.max(y)]
  x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
  width,height = _LogLogSize(**kwargs)
  if 'overwrite' in kwargs and kwargs['overwrite']:
      labs = plt.get_figlabels() 
      if "LogLog" not in labs:
        configs.DefaultLS()
      else:
        configs.ToggleLS()
      plt.figure("LogLog",figsize=(width,height))
  else:
      configs.DefaultLS()
      plt.figure(figsize=(width,height))

  fig = plt.loglog(x,y,configs.LS)
  plt.grid(True)
  AuxPlotLabelLL1D(auxDict)
  plt.ion()
  plt.show()
  return fig 



