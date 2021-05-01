

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 
from matplotlib.colors import LightSource

from graphdata.shared.shared1D import GetData1D,ProcessData1D
from graphdata.shared.shared import GenFileList,GetDataFileInfo,ProcessAux
from graphdata import plt
from graphdata import configs 
from graphdata import np 

def waterfall(*args,**kwargs):
  """
  Plots the evolution of 1D data in a mesh-like 3D figure. 

  waterfall(fileID,fileRange,plotLimits,evoID):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat 
    e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the
    fileID is simply 'T'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the
      fileID are used.  fileRange does not need to specify minFileNum or
      maxFileNum e.g. waterfall('T',[10]) and waterfall('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plotting range of the waterfall function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimits list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables.  plotLimits does
      not need to specify a minimum and maximum y value 
      e.g. waterfall('T',10,[0 1]) will plot data with an input value between 0
      and 1 

    
    e.g. waterfall('T',[10,0,60],[0,1,-10,10]) will produce an waterfall plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. waterfall('R') will produce an waterfall plot using all 'R' fileID data
    R_0.dat, R_1.dat, ..., R_MAX#.dat

    evoID: y-propagated evolution values to use (default is propagation
    distance (pval) ID for data files where files look like fileID_fileNum.dat 
    e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the
    fileID is simply 'T'
  """

  fileList = []
  if 'fileList' in kwargs:
    fileList = kwargs['fileList']
  else:
    fileList = GenFileList(*args)
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x1 = []
  num = 0
  evoID = 'pval'

  for file in fileList:
    auxDict = ProcessAux(file) 
    if evoID in auxDict: 
      if evoID == 'pval':
        if(configs._G["scale"] == 'nonDim' and "pscale" in auxDict):
          x1.append(float(auxDict['pval'])/float(auxDict['pscale']))
        elif(configs._G["scale"] == 'dimscale'):
          x1.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
        elif(configs._G["scale"] == 'noscale'):
          x1.append(float(auxDict['pval']))
      else:
        if(configs._G["scale"] == 'dimscale'):
          x1.append(float(auxDict[evoID])/float(configs._G['pdimscale']))
        elif(configs._G["scale"] == 'noscale'):
          x1.append(float(auxDict[evoID]))
    else:
      x1.append(num)
      num = num + 1

  ymin = np.amin(x1)
  ymax = np.amax(x1)

  width = float(configs._G['WaterfallWidth'])
  height = float(configs._G['WaterfallHeight'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  fig = plt.figure(figsize=(width,height))
  ax = fig.add_subplot(1,1,1,projection = '3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  count = 0
  normFact = 1.0
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    x,y,auxDict = GetData1D(fileID,repNum)
    x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
    y = np.sqrt(y)
    #y = y/1e4
    #y = y/np.amax(np.absolute(y))
    ax.plot(x,x1[count]*np.ones_like(x),y,color = 'black')
    count = count + 1

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    auxDict['zlim'] = ylim
  auxDict['ylim'] = [ymin,ymax]

  if 'view' in kwargs:
    auxDict['view'] = kwargs['view']
  else:
    auxDict['view'] = [57,-57]


  plt.xlim([x[0],x[-1]])
  plt.ylim([ymin,ymax])
  AuxWaterfallLabel(ax,auxDict)
  plt.ion()
  plt.show()
  plt.tight_layout()
  return ax

def AuxWaterfallLabel(ax,auxDict):
  xstr = ""
  ystr = ""
  zstr = ""
  if(configs._G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + auxDict["xscale_str"] + ')' 
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + auxDict["pscale_str"] + ')' 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + ' (' + auxDict["yscale_str"] + ')' 
  elif(configs._G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + auxDict["xunit_str"] + ')' 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + auxDict["punit_str"] + ')' 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + ' (' + auxDict["yunit_str"] + ')' 
  elif(configs._G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + configs._G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + " (arb.)" 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + configs._G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'plabel' in auxDict:
      ystr = auxDict['plabel'] + " (arb.)" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = zstr + auxDict['ylabel'] + ' (' + configs._G['zdimscale_str'] + auxDict["yunit_str"] + ')' 

  if 'zlim' in auxDict:
    zlim = auxDict['zlim']
    ax.set_zlim3d(zlim)
  view = [57,-57]
  if 'view' in auxDict:
    view = auxDict['view']

  ax.set_xlabel(xstr,labelpad = 40)
  ax.set_ylabel(ystr,labelpad = 40)
  ax.set_zlabel(zstr,labelpad = 40)
  ax.view_init(view[0],view[1])


def waterfallLog(*args,**kwargs):
  """
  Plots the log10(y) evolution of 1D data in a mesh-like 3D figure. 

  waterfallLog(fileID,fileRange,plotLimits):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat
      e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...
      then the fileID is simply 'T'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the
      fileID are used.  fileRange does not need to specify minFileNum or
      maxFileNum e.g. waterfallLog('T',[10]) and waterfallLog('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,decades]
    plotLimits: Specifies the plotting range of the waterfallLog function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      decades: Number of decades of output to include in log plots
    
    e.g. waterfallLog('T',[10,0,60],[0,1,-10,10]) will produce an waterfallLog plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. waterfallLog('R') will produce an waterfallLog plot using all 'R' fileID data
    R_0.dat, R_1.dat, ..., R_MAX#.dat
  """

  fileList = GenFileList(*args)
  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict()
  x1 = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs._G["scale"] == 'nonDim'):
        x1.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs._G["scale"] == 'dimscale'):
        x1.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
      elif(configs._G["scale"] == 'noscale'):
        x1.append(float(auxDict['pval']))
    else:
      x1.append(num)
      num = num + 1

  ymin = np.amin(x1)
  ymax = np.amax(x1)

  width = float(configs._G['WaterfallWidthL'])
  height = float(configs._G['WaterfallHeightL'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  fig = plt.figure(figsize=(width,height))
  ax = fig.add_subplot(1,1,1,projection = '3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  count = 0
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    x,y,auxDict = GetData1D(fileID,repNum)
    auxDict['decades'] = configs._G['decades']
    x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
    y = np.log10(y)
    ax.plot(x,x1[count]*np.ones_like(x),y,color = 'black')
    count = count + 1

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    auxDict['zlim'] = ylim
  auxDict['ylim'] = [ymin,ymax]

  plt.tight_layout()
  plt.xlim([x[0],x[-1]])
  plt.ylim([ymin,ymax])
  AuxWaterfallLabel(ax,auxDict)
  plt.ion()
  plt.show()
  return ax


def ProcessWaterfallPoints(x,y,numX):
  xvals = np.linspace(x[0],x[-1],numX)
  y = np.interp(xvals,x,y)
  x = xvals
  return (x,y)


def GetContourData(*args):
  fileID = '' 
  fileList = []
  if len(args) == 0:
    return False
  elif len(args) == 1:
    fileID = args[0] 
    fileList = GenFileList(fileID) 
  elif len(args) > 1:
    fileID = args[0] 
    fileSpec = args[1]
    fileList = GenFileList(fileID,fileSpec) 
  if not fileList:
    print("waterfall fileList not generated. ")  
    return False

  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs._G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs._G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
      elif(configs._G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum,*plotArgs)
  y,z,auxDict = ProcessData1D(y,z,auxDict)
  y,z = ProcessWaterfallPoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum,*plotArgs)
    y,z,auxDict = ProcessData1D(y,z,auxDict)
    y,z = ProcessWaterfallPoints(y,z,50)
    Z[:,count] = z 
    count = count + 1

  Y,X = np.meshgrid(y,x)
#  X,Y = np.meshgrid(x,y)
#  X = np.transpose(X)
#  Y = np.transpose(Y)
  Z = np.transpose(Z)
  return (X,Y,Z,auxDict)

def WaterfallC(*args):
  (X,Y,Z,auxDict) = GetContourData(*args)
  width = 6;
  height = 8;
  fig = plt.figure(figsize=(width,height))
  CS = plt.contourf(Y,X,Z,200,interpolation='bicubic')
  AuxContourLabel(CS,auxDict)
  plt.ion()
  plt.show()
  return True

def WaterfallI(*args):
  (X,Y,Z,auxDict) = GetContourData(*args)
  width = 6;
  height = 8;
  lightS = LightSource(azdeg=0,altdeg=5)
  rgb = lightS.shade(Z,plt.cm.hot)
  fig = plt.figure(figsize=(width,height))
  ax = plt.subplot(111)
  im = ax.imshow(rgb,aspect='auto',interpolation='bicubic')
  plt.ion()
  plt.show()
  return True


def AuxContourLabel(CS,auxDict):
  xstr = ""
  ystr = ""
  if(configs._G['scale'] == 'nonDim'):
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] 
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + auxDict["xscale_str"] + ')' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] 
  elif(configs._G['scale'] == 'noscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] 
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel']
  elif(configs._G['scale'] == 'dimscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] + '(' + configs._G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      xstr = ystr + auxDict['plabel'] + " [arb.]" 
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + configs._G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + " [arb.]" 
  xstr = '$' + xstr + '$'
  ystr = '$' + ystr + '$'
  CS.ax.set_xlabel(ystr)
  CS.ax.set_ylabel(xstr)


def WaterfallB(*args,**kwargs):
  fileID = '' 
  fileList = []
  if len(args) == 0:
    return False
  elif len(args) == 1:
    fileID = args[0] 
    fileList = GenFileList(fileID) 
  elif len(args) > 1:
    fileID = args[0] 
    fileSpec = args[1]
    fileList = GenFileList(fileID,fileSpec) 
  if not fileList:
    print("waterfall fileList not generated. ")  
    return False

  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs._G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs._G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
      elif(configs._G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessWaterfallPoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessWaterfallPoints(y,z,50)
    Z[:,count] = z 
    count = count + 1

  X,Y = np.meshgrid(x,y)
  plt.figure(figsize=(float(configs._G['WaterfallWidth']),float(configs._G['WaterfallHeight'])))
  CS = plt.contour(X,Y,Z,6,colors='k')
  AuxContourLabel(CS,auxDict)
  plt.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
  plt.ion()
  plt.show()
  return True

def waterfallLog(*args,**kwargs):
  fileID = '' 
  fileList = []
  if len(args) == 0:
    return False
  elif len(args) == 1:
    fileID = args[0] 
    fileList = GenFileList(fileID) 
  elif len(args) > 1:
    fileID = args[0] 
    fileSpec = args[1]
    fileList = GenFileList(fileID,fileSpec) 
  if not fileList:
    print("waterfall fileList not generated. ")  
    return False

  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs._G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs._G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
      elif(configs._G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessWaterfallPoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    auxDict['decades'] = configs._G['decades']
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessWaterfallPoints(y,z,50)
    Z[:,count] = z
    count = count + 1

  X,Y = np.meshgrid(x,y)
  plt.figure(figsize=(float(configs._G['WaterfallWidth']),float(configs._G['WaterfallHeight'])))
  CS = plt.contour(X,Y,Z,colors = 'k',locator=ticker.LogLocator())
  AuxContourLabel(CS,auxDict)
  plt.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
  plt.ion()
  plt.show()
  return True


def _SurfaceSize(*args):

  if len(args) > 4:
    figSz = args[4]
    if isinstance(figSz,int):
      width = figSz
      height = figSz
    elif len(figSz) == 1:
      width = figSz[0]
      height = figSz[0]
    elif len(figSz) == 2:
      width = figSz[0]
      height = figSz[1]
  else:
    width = float(configs._G['SurfaceWidth'])
    height = float(configs._G['SurfaceHeight'])

  return (width,height) 

def GetView(*args):
  if len(args) > 3:
    view = args[3]  
    if len(view) ==  1:
      ang1 = view[0] 
      ang2 = int(configs._G['surfaceAzimuth'])
    elif len(view) == 2:
      ang1 = view[0] 
      ang2 = view[1] 
    else:
      ang1 = int(configs._G['surfaceElevation'])
      ang2 = int(configs._G['surfaceAzimuth'])
  else:
    ang1 = int(configs._G['surfaceElevation'])
    ang2 = int(configs._G['surfaceAzimuth'])
  return(ang1,ang2)


