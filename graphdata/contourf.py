
from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.figsizes import ContourfSize
from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.shared2D import ProcessData2D
from graphdata.shared.shared2D import ProcessContourLimitZ
from graphdata.shared.shared2D import ContourLevels
from graphdata.shared.shared2D import ContourLevelTicks
from graphdata.shared.shared import LabelX
from graphdata.shared.shared import LabelY
from graphdata.shared.shared import ProcessDecadeLimits

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def contourf(filename,levels=None,figsize=None,xlim=None,ylim=None,zlim=None,\
        decades=None,overwrite=False,**kwargs):
    """
    Graph of 2D data file using Matplotlib plt.contourf

    INPUTS:
        filename: string
            name of file containing 2D data to be plotted
        levels : int or array-like (optional) 
            determines number and position of contour lines/regions
        figsize: tuple (width,height)
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            y-axis limits of graph
        zlim: np.array [zmin,zmax]
            zmin -> minimum value data can take
            zmax -> maximum value data can take
        decades: int
            maximum number of log10 decades to be plotted (starting with max value)
        overwrite: bool
            false (default) -> create new contourf plot figure
            true -> clear figure named 'Contourf' and make new contourf plot
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.contourf plot

    OUTPUTS:

        ax : mpl_toolkits.mplot3d.axes3d.Axes3D
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """

    x,y,Z,auxDict = LoadData2D(filename)
    ExtendDictionary(auxDict,levels=levels,figsize=figsize,xlim=xlim,ylim=ylim,zlim=zlim,\
            decades=decades,overwrite=overwrite)
    figsize = ContourfSize(figsize)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
    X,Y = np.meshgrid(x,y)
    if zlim is not None:
        Z = ProcessContourLimitZ(Z,zlim)
    if decades is not None:
        Z = ProcessDecadeLimits(Z,decades)
    levels = ContourLevels(levels,Z)
    levelTicks = ContourLevelTicks(levels,Z)
    if overwrite:
        fig = plt.figure("Contourf",figsize=figsize)
        fig.clf()
    else:
        fig = plt.figure(figsize=figsize)
    ax = plt.gca()

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
        del kwargs['cmap']
    else:
        cmap = str(configs._G["cmap"])

    CS = plt.contourf(X,Y,Z,levels,cmap=cmap,**kwargs)
    ax.set_xlabel(LabelX(auxDict))
    ax.set_ylabel(LabelY(auxDict))
    CB = plt.colorbar(ticks=levelTicks,format='%0.2e')
    plt.ion()
    plt.show()
    return ax

#def contourfLog(*args,overwrite=False,**kwargs):
#  """
#  Log color contour plot of 2D data. 
#
#  ContourLF(fileID,fileNumber,[plotLimits],[decades,numContours],[figSize]):
#  Args:
#    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
#      if data files for SRST data are SQ_SRST_0.dat,SQ_SRST_1.dat,
#      SQ_SRST_2.dat,..., then the fileID is simply 'SQ_SRST'
#
#    fileNumber: Specifies which data file number to plot e.g.
#      ContourLF('SRST',10) will make a contour plot of the data file 
#      'SRST_10.dat' if this data file is available
#
#    plotLimits = [minX,maxX,minY,maxY]
#    plotLimits: Specifies the contour plot limits 
#      minX:  Minimum x value limit
#      maxX:  Maximum x value limit
#      minY:  Minimum y value limit
#      maxY:  Maximum y value limit
#      If no plotLimit list is given, then all data is used in the plots and
#      then minimum and maximum graph limits will depend on the minimum and
#      maximum data limits of the input and output variables. The plotLimits
#      list can be empty, contain just xmin and xmax limits, contain just
#      xmin,xmax,ymin,and ymax, or contain all limits
#        e.g. ContourLF('SRST',10,[0,1]) will plot data with x-limits 
#             between 0 and 1 
#        e.g. ContourLF('SRST',10,[0,1,-2,2]) will plot data with x-limits 
#             between 0 and 1 and y-limits between -2 and 2. 
#        e.g. ContourLF('SRST',10) is the same as ContourLF('SRST',10,[])
#
#    numDecades: Number of decades of data below maximum to plot
#        eg. ContourLF('SRST',10,[],8) will plot 8 decades of data 
#    numContours: Specifies number of contour levels to use in contour plot
#        eg. ContourLF('SRST',10,[],[8,100]) will plot 8 decades of data 
#        with 100 contour levels
#    
#    figSize: Specifies the size of the image to be ploted. 
#      width: Width of image in inches 
#      height: Height of image in inches 
#        eg. ContourLF('RT',10,[],[],[14,5]) will plot a contour image with
#            a width of 14 inches and a height of 5 inches
#
#
#  """
#
#  x,y,Z,auxDict = GetData2D(*args)
#  auxDict['decades'] = configs._G['decades']
#  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict,**kwargs)
#  X,Y = np.meshgrid(x,y)
#  width,height = _ContourSize(**kwargs)
#  decades,numCont = ContNumLog(**kwargs)
#  levels,levelTicks,levelTickStr,Z = GetContourLevelsLog(decades,numCont,Z,auxDict) 
#
#  if overwrite:
#      fig = plt.figure("ContourfLog",figsize=(width,height))
#      fig.clf()
#  else:
#      fig = plt.figure(figsize=(width,height))
#
#  CS = plt.contourf(X,Y,Z,levels,cmap=str(configs._G["cmap"]),locator=ticker.LogLocator())
#  AuxContourLabel(CS,auxDict)
#  CB = plt.colorbar(ticks=levelTicks)
#  CB.ax.set_yticklabels(levelTickStr)
#  plt.ion()
#  plt.show()
#  return True
#
#
#def GetContourLevelsLog(decades,numCont,Z,auxDict):
#  if numCont < 3:
#    numCont = 3
#  maxVal = np.amax(Z)
#  maxDec = 0.5 + np.log10(maxVal)
#  minDec = maxDec - decades - 1 
#  if 'minDec' in auxDict:
#    minDec = float(auxDict['minDec'])
#  if 'maxDec' in auxDict:
#    maxDec = float(auxDict['maxDec'])
#  levels = list(np.linspace(minDec,maxDec,numCont))
#  if maxDec not in levels:
#    levels.append(maxDec)
#  minTick = int(np.ceil(np.amin(levels)))
#  maxTick = int(np.floor(np.amax(levels)))
#  dLevel = int((maxTick - minTick+1)/numCont)
#  if dLevel < 1:
#    dLevel = 1
#  levels = [10**x for x in levels]
#
#  tick = list(range(minTick,maxTick+1,dLevel))
#  levelTick = [10**x for x in tick]
#  levelTickStr = []
#  for x in tick:
#    levelTickStr.append('$10^{' + str(x) + '}$') 
#  maxLevTick = 8 
#  if len(levelTick) > maxLevTick:
#    indxStep = int(np.ceil(float(len(levelTick))/maxLevTick))
#    lastTick = levelTick[-1]
#    lastTickStr = levelTickStr[-1]
#    levelTick = levelTick[0:-1:indxStep]
#    levelTickStr = levelTickStr[0:-1:indxStep]
#    if (lastTick) not in levelTick:
#      levelTick.append(lastTick)
#    if (lastTickStr) not in levelTickStr:
#      levelTickStr.append(lastTickStr)
#  return (levels,levelTick,levelTickStr,Z)
#
#def ContNum(**kwargs):
#  numCont = int(configs._G["contours"])
#  if 'contours' in kwargs:
#    numCont = kwargs['contours']
#  if 'conts' in kwargs:
#    numCont = kwargs['conts']
#  return numCont
#
#def ContNumLog(**kwargs):
#  decades = int(configs._G["decades"])
#  numCont = int(configs._G["contours"])
#  if 'decades' in kwargs:
#    decades = kwargs['decades']
#  if 'decs' in kwargs:
#    decades = kwargs['decs']
#  if 'contours' in kwargs:
#    numCont = kwargs['contours']
#  if 'conts' in kwargs:
#    numCont = kwargs['conts']
#  return (decades,numCont)
#
#def _ContourSize(**kwargs):
#
#  width = float(configs._G['ContourWidth'])
#  height = float(configs._G['ContourHeight'])
#  if 'size' in kwargs:
#    array = kwargs['size']
#    width = array[0]
#    height = array[1]
#
#  return (width,height) 
#

