#!/usr/bin/python
# Filename: waterfall.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 
from matplotlib.colors import LightSource

from graphdata.shared.idnum import GetDataFileList
from graphdata.shared.shared import ProcessComplex
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared1D import LoadData1D
from graphdata.shared.shared1D import ProcessData1D
from graphdata.shared.shared2D import GetView
from graphdata.shared.figsizes import WaterfallSize

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def waterfall(fileID : str, fileNumbers : list,figsize=None,xlim=None,ylim=None,\
        complex_op=None,zvalstr=None,aspect=None,**kwargs):
    """
    INPUTS:
        fileID: str
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (extension is a catchall, doesnt have to be dat)
        fileNumbers: list[int]
            Specifies which data file numbers to plot 
            e.g.  waterfall('T',[0:2:100]) will plot files T_0.dat,T_2.dat,...,T_100.dat
        (see graphdata.plot.plot for info on other arguments)

        xlim: np.array
            x-axis limits of graph
        zlim: np.array
            z-axis limits of graph
        complex_op : string in the following list ('real','imag','power','absolute','angle')
            complex operation used to plot complex data
        zvalstr: str
            looks for metadata labeled zvalstr in the files, and will use these to plot z-axis with units
        aspect: tuple
            aspect ratio to use for xyz graph, e.g. (1,1,1) corresponds to a box
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.plot plots

    OUTPUTS:
        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """

    fileList = GetDataFileList(fileID,fileNumbers)
    fileLen = len(fileList)
    count = 0
    auxDict = dict() 
    x1 = [0]*len(fileList)
    figsize = WaterfallSize(figsize)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection='3d')

    ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    count = 0
    normFact = 1.0
    for i,filename in enumerate(fileList):
        x,y,auxDict = LoadData1D(filename)
        y = ProcessComplex(complex_op,y)
        ExtendDictionary(auxDict,figsize=figsize,xlim=xlim,\
                ylim=ylim,complex_op=complex_op)
        x,y,auxDict = ProcessData1D(x,y,auxDict)
        if zvalstr is not None and zvalstr in auxDict:
            x1[i] = float(auxDict[zvalstr])
        else:
            x1[i] = i
        ax.plot(x,x1[i]*np.ones_like(x),y,color = 'black',**kwargs)

    if xlim is None:
        xlim = [x[0],x[-1]]
    plt.xlim(xlim)

    if ylim is not None:
        ax.set_zlim3d(ylim)

    zmin = np.amin(x1)
    zmax = np.amax(x1)
    plt.ylim([zmin,zmax])

    if 'xlabel' in auxDict:
        ax.set_xlabel(auxDict['xlabel'])
    else:
        ax.set_xlabel(auxDict['x'])

    if 'ylabel' in auxDict:
        ax.set_zlabel(auxDict['ylabel'])
    else:
        ax.set_zlabel(auxDict['y'])

    if zvalstr is not None:
        ax.set_ylabel(zvalstr)
    else:
        ax.set_ylabel('file')

    elev,azim = GetView(**kwargs)
    ax.view_init(elev,azim)
    if aspect is not None:
        ax.set_box_aspect(aspect = aspect)
    plt.ion()
    plt.show()
    plt.tight_layout()
    return ax

#def AuxWaterfallLabel(ax,auxDict):
#  xstr = ""
#  ystr = ""
#  zstr = ""
#  if(configs._G['scale'] == 'nonDim'):
#    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
#      xstr = auxDict['xlabel'] + ' (' + auxDict["xscale_str"] + ')' 
#    if 'pscale_str' in auxDict and 'plabel' in auxDict:
#      ystr = auxDict['plabel'] + ' (' + auxDict["pscale_str"] + ')' 
#    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
#      zstr = auxDict['ylabel'] + ' (' + auxDict["yscale_str"] + ')' 
#  elif(configs._G['scale'] == 'noscale'):
#    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
#      xstr = auxDict['xlabel'] + ' (' + auxDict["xunit_str"] + ')' 
#    if 'punit_str' in auxDict and 'plabel' in auxDict:
#      ystr = auxDict['plabel'] + ' (' + auxDict["punit_str"] + ')' 
#    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
#      zstr = auxDict['ylabel'] + ' (' + auxDict["yunit_str"] + ')' 
#  elif(configs._G['scale'] == 'dimscale'):
#    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
#      xstr = auxDict['xlabel'] + ' (' + configs._G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
#    elif 'xlabel' in auxDict:
#      xstr = auxDict['xlabel'] + " (arb.)" 
#    if 'punit_str' in auxDict and 'plabel' in auxDict:
#      ystr = auxDict['plabel'] + ' (' + configs._G['pdimscale_str'] + auxDict["punit_str"] + ')' 
#    elif 'plabel' in auxDict:
#      ystr = auxDict['plabel'] + " (arb.)" 
#    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
#      zstr = zstr + auxDict['ylabel'] + ' (' + configs._G['zdimscale_str'] + auxDict["yunit_str"] + ')' 
#
#  if 'zlim' in auxDict:
#    zlim = auxDict['zlim']
#    ax.set_zlim3d(zlim)
#
#  view = [57,-57]
#  if 'view' in auxDict:
#    view = auxDict['view']
#
#  ax.set_xlabel(xstr,labelpad = 40)
#  ax.set_ylabel(ystr,labelpad = 40)
#  ax.set_zlabel(zstr,labelpad = 40)
#  ax.view_init(view[0],view[1])


#def waterfallLog(*args,**kwargs):
#  """
#  Plots the log10(y) evolution of 1D data in a mesh-like 3D figure. 
#
#  waterfallLog(fileID,fileRange,plotLimits):
#  Args:
#    fileID: ID for data files where files look like fileID_fileNum.dat
#      e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...
#      then the fileID is simply 'T'
#
#    fileRange = [numFiles,minFileNum,maxFileNum]
#    fileRange: Specifies the files from which to accept data.
#      numFiles:     Number of 1D data files to plot
#      minFileNum:   Start file number.  
#      maxFileNum:   End file number.  
#      If no fileRange is given, then all data files corresponding to the
#      fileID are used.  fileRange does not need to specify minFileNum or
#      maxFileNum e.g. waterfallLog('T',[10]) and waterfallLog('T',10) evolve 10 evenly
#      spaced data files of fileID 'T' starting with the first available data
#      file and ending with the last available data
#
#    plotLimits = [minX,maxX,decades]
#    plotLimits: Specifies the plotting range of the waterfallLog function data.
#      minX:  Minimum x value limit
#      maxX:  Maximum x value limit
#      decades: Number of decades of output to include in log plots
#    
#    e.g. waterfallLog('T',[10,0,60],[0,1,-10,10]) will produce an waterfallLog plot using
#    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
#    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
#    range of 0 to 1 and plot output in the range of -10 to 10
#
#    e.g. waterfallLog('R') will produce an waterfallLog plot using all 'R' fileID data
#    R_0.dat, R_1.dat, ..., R_MAX#.dat
#  """
#
#  fileList = GenFileList(*args)
#  plotArgs = args[2:]
#  fileLen = len(fileList)
#  count = 0
#  auxDict = dict()
#  x1 = []
#  num = 0
#  for file in fileList:
#    auxDict = ProcessAux(file) 
#    if "pscale" in auxDict: 
#      if(configs._G["scale"] == 'nonDim'):
#        x1.append(float(auxDict['pval'])/float(auxDict['pscale']))
#      elif(configs._G["scale"] == 'dimscale'):
#        x1.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
#      elif(configs._G["scale"] == 'noscale'):
#        x1.append(float(auxDict['pval']))
#    else:
#      x1.append(num)
#      num = num + 1
#
#  ymin = np.amin(x1)
#  ymax = np.amax(x1)
#
#  SetWaterfallFigsize(auxDict,**kwargs)
#  fig = plt.figure(figsize=auxDict['figsize'])
#  ax = fig.add_subplot(1,1,1,projection = '3d')
#  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
#  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
#  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
#  count = 0
#  for file in fileList:
#    fileID,repNum = GetDataFileInfo(file) 
#    x,y,auxDict = LoadData1D(fileID,repNum)
#    auxDict['decades'] = configs._G['decades']
#    x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
#    y = np.log10(y)
#    ax.plot(x,x1[count]*np.ones_like(x),y,color = 'black')
#    count = count + 1
#
#  if 'ylim' in auxDict:
#    ylim = auxDict['ylim']
#    auxDict['zlim'] = ylim
#  auxDict['ylim'] = [ymin,ymax]
#
#  plt.tight_layout()
#  plt.xlim([x[0],x[-1]])
#  plt.ylim([ymin,ymax])
#  SetWaterfallView(auxDict,**kwargs)
#  AuxWaterfallLabel(ax,auxDict)
#  plt.ion()
#  plt.show()
#  return ax
#
#
#def ProcessWaterfallPoints(x,y,numX):
#  xvals = np.linspace(x[0],x[-1],numX)
#  y = np.interp(xvals,x,y)
#  x = xvals
#  return (x,y)
#
#
#def GetContourData(*args):
#  fileID = '' 
#  fileList = []
#  if len(args) == 0:
#    return False
#  elif len(args) == 1:
#    fileID = args[0] 
#    fileList = GenFileList(fileID) 
#  elif len(args) > 1:
#    fileID = args[0] 
#    fileSpec = args[1]
#    fileList = GenFileList(fileID,fileSpec) 
#  if not fileList:
#    print("waterfall fileList not generated. ")  
#    return False
#
#  plotArgs = args[2:]
#  fileLen = len(fileList)
#  count = 0
#  auxDict = dict() 
#  x = []
#  num = 0
#  for file in fileList:
#    auxDict = ProcessAux(file) 
#    if "pscale" in auxDict: 
#      if(configs._G["scale"] == 'nonDim'):
#        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
#      elif(configs._G["scale"] == 'dimscale'):
#        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
#      elif(configs._G["scale"] == 'noscale'):
#        x.append(float(auxDict['pval']))
#    else:
#      x.append(num)
#      num = num + 1
#
#  fileID,repNum = GetDataFileInfo(fileList[0]) 
#  y,z,auxDict = LoadData1D(fileID,repNum,*plotArgs)
#  y,z,auxDict = ProcessData1D(y,z,auxDict)
#  y,z = ProcessWaterfallPoints(y,z,50)
#
#  count = 0; 
#  Z = np.zeros((len(y),len(x)))
#  for file in fileList:
#    fileID,repNum = GetDataFileInfo(file) 
#    y,z,auxDict = LoadData1D(fileID,repNum,*plotArgs)
#    y,z,auxDict = ProcessData1D(y,z,auxDict)
#    y,z = ProcessWaterfallPoints(y,z,50)
#    Z[:,count] = z 
#    count = count + 1
#
#  Y,X = np.meshgrid(y,x)
##  X,Y = np.meshgrid(x,y)
##  X = np.transpose(X)
##  Y = np.transpose(Y)
#  Z = np.transpose(Z)
#  return (X,Y,Z,auxDict)
#
#def WaterfallC(*args):
#  (X,Y,Z,auxDict) = GetContourData(*args)
#  width = 6;
#  height = 8;
#  fig = plt.figure(figsize=(width,height))
#  CS = plt.contourf(Y,X,Z,200,interpolation='bicubic')
#  AuxContourLabel(CS,auxDict)
#  plt.ion()
#  plt.show()
#  return True
#
#def WaterfallI(*args):
#  (X,Y,Z,auxDict) = GetContourData(*args)
#  width = 6;
#  height = 8;
#  lightS = LightSource(azdeg=0,altdeg=5)
#  rgb = lightS.shade(Z,plt.cm.hot)
#  fig = plt.figure(figsize=(width,height))
#  ax = plt.subplot(111)
#  im = ax.imshow(rgb,aspect='auto',interpolation='bicubic')
#  plt.ion()
#  plt.show()
#  return True
#
#
#def AuxContourLabel(CS,auxDict):
#  xstr = ""
#  ystr = ""
#  if(configs._G['scale'] == 'nonDim'):
#    if 'pscale_str' in auxDict and 'plabel' in auxDict:
#      xstr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
#    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
#      xstr = auxDict['plabel'] 
#    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel'] + '(' + auxDict["xscale_str"] + ')' 
#    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel'] 
#  elif(configs._G['scale'] == 'noscale'):
#    if 'punit_str' in auxDict and 'plabel' in auxDict:
#      xstr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
#    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
#      xstr = auxDict['plabel'] 
#    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel'] + '(' + auxDict["xunit_str"] + ')' 
#    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel']
#  elif(configs._G['scale'] == 'dimscale'):
#    if 'punit_str' in auxDict and 'plabel' in auxDict:
#      xstr = auxDict['plabel'] + '(' + configs._G['pdimscale_str'] + auxDict["punit_str"] + ')' 
#    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
#      xstr = ystr + auxDict['plabel'] + " [arb.]" 
#    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel'] + '(' + configs._G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
#    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
#      ystr = auxDict['xlabel'] + " [arb.]" 
#  xstr = '$' + xstr + '$'
#  ystr = '$' + ystr + '$'
#  CS.ax.set_xlabel(ystr)
#  CS.ax.set_ylabel(xstr)
#
#
#def WaterfallB(*args,**kwargs):
#  fileID = '' 
#  fileList = []
#  if len(args) == 0:
#    return False
#  elif len(args) == 1:
#    fileID = args[0] 
#    fileList = GenFileList(fileID) 
#  elif len(args) > 1:
#    fileID = args[0] 
#    fileSpec = args[1]
#    fileList = GenFileList(fileID,fileSpec) 
#  if not fileList:
#    print("waterfall fileList not generated. ")  
#    return False
#
#  plotArgs = args[2:]
#  fileLen = len(fileList)
#  count = 0
#  auxDict = dict() 
#  x = []
#  num = 0
#  for file in fileList:
#    auxDict = ProcessAux(file) 
#    if "pscale" in auxDict: 
#      if(configs._G["scale"] == 'nonDim'):
#        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
#      elif(configs._G["scale"] == 'dimscale'):
#        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
#      elif(configs._G["scale"] == 'noscale'):
#        x.append(float(auxDict['pval']))
#    else:
#      x.append(num)
#      num = num + 1
#
#  fileID,repNum = GetDataFileInfo(fileList[0]) 
#  y,z,auxDict = LoadData1D(fileID,repNum)
#  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
#  y,z = ProcessWaterfallPoints(y,z,50)
#
#  count = 0; 
#  Z = np.zeros((len(y),len(x)))
#  for file in fileList:
#    fileID,repNum = GetDataFileInfo(file) 
#    y,z,auxDict = LoadData1D(fileID,repNum)
#    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
#    y,z = ProcessWaterfallPoints(y,z,50)
#    Z[:,count] = z 
#    count = count + 1
#
#  X,Y = np.meshgrid(x,y)
#  plt.figure(figsize=(float(configs._G['WaterfallWidth']),float(configs._G['WaterfallHeight'])))
#  CS = plt.contour(X,Y,Z,6,colors='k')
#  AuxContourLabel(CS,auxDict)
#  plt.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
#  plt.ion()
#  plt.show()
#  return True
#
##def waterfallLog(*args,**kwargs):
##  fileID = '' 
##  fileList = []
##  if len(args) == 0:
##    return False
##  elif len(args) == 1:
##    fileID = args[0] 
##    fileList = GenFileList(fileID) 
##  elif len(args) > 1:
##    fileID = args[0] 
##    fileSpec = args[1]
##    fileList = GenFileList(fileID,fileSpec) 
##  if not fileList:
##    print("waterfall fileList not generated. ")  
##    return False
##
##  plotArgs = args[2:]
##  fileLen = len(fileList)
##  count = 0
##  auxDict = dict() 
##  x = []
##  num = 0
##  for file in fileList:
##    auxDict = ProcessAux(file) 
##    if "pscale" in auxDict: 
##      if(configs._G["scale"] == 'nonDim'):
##        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
##      elif(configs._G["scale"] == 'dimscale'):
##        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
##      elif(configs._G["scale"] == 'noscale'):
##        x.append(float(auxDict['pval']))
##    else:
##      x.append(num)
##      num = num + 1
##
##  fileID,repNum = GetDataFileInfo(fileList[0]) 
##  y,z,auxDict = GetData(fileID,repNum)
##  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
##  y,z = ProcessWaterfallPoints(y,z,50)
##
##  count = 0; 
##  Z = np.zeros((len(y),len(x)))
##  for file in fileList:
##    fileID,repNum = GetDataFileInfo(file) 
##    y,z,auxDict = LoadData1D(fileID,repNum)
##    auxDict['decades'] = configs._G['decades']
##    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
##    y,z = ProcessWaterfallPoints(y,z,50)
##    Z[:,count] = z
##    count = count + 1
##
##  X,Y = np.meshgrid(x,y)
##  plt.figure(figsize=(float(configs._G['WaterfallWidth']),float(configs._G['WaterfallHeight'])))
##  CS = plt.contour(X,Y,Z,colors = 'k',locator=ticker.LogLocator())
##  AuxContourLabel(CS,auxDict)
##  plt.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
##  plt.ion()
##  plt.show()
##  return True
##




