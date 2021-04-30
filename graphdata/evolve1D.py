

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 
from matplotlib.colors import LightSource

from .shared1D import ProcessData1D 
from pprint import pprint
from .aux import ProcessAux 
from .aux import GenFileList
from .aux import GetDataFileInfo
from .aux import GetData1D 
from .aux import GenFileList
from .aux import GenMovie
from .aux import MovLength
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 

def Evolve(*args,**kwargs):
  """
  Plots the evolution of 1D data in a mesh-like 3D figure. 

  Evolve(fileID,fileRange,plotLimits,evoID):
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
      maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plotting range of the Evolve function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimits list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables.  plotLimits does
      not need to specify a minimum and maximum y value 
      e.g. Evolve('T',10,[0 1]) will plot data with an input value between 0
      and 1 

    
    e.g. Evolve('T',[10,0,60],[0,1,-10,10]) will produce an Evolve plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. Evolve('R') will produce an Evolve plot using all 'R' fileID data
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
        if(configs.G["scale"] == 'nonDim' and "pscale" in auxDict):
          x1.append(float(auxDict['pval'])/float(auxDict['pscale']))
        elif(configs.G["scale"] == 'dimscale'):
          x1.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
        elif(configs.G["scale"] == 'noscale'):
          x1.append(float(auxDict['pval']))
      else:
        if(configs.G["scale"] == 'dimscale'):
          x1.append(float(auxDict[evoID])/float(configs.G['pdimscale']))
        elif(configs.G["scale"] == 'noscale'):
          x1.append(float(auxDict[evoID]))
    else:
      x1.append(num)
      num = num + 1

  ymin = np.amin(x1)
  ymax = np.amax(x1)

  width = float(configs.G['EvolveWidth'])
  height = float(configs.G['EvolveHeight'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  fig = pl.figure(figsize=(width,height))
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


  pl.xlim([x[0],x[-1]])
  pl.ylim([ymin,ymax])
  AuxEvolveLabel(ax,auxDict)
  pl.ion()
  pl.show()
  pl.tight_layout()
  return ax

def AuxEvolveLabel(ax,auxDict):
  xstr = ""
  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + auxDict["xscale_str"] + ')' 
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + auxDict["pscale_str"] + ')' 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + ' (' + auxDict["yscale_str"] + ')' 
  elif(configs.G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + auxDict["xunit_str"] + ')' 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + auxDict["punit_str"] + ')' 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + ' (' + auxDict["yunit_str"] + ')' 
  elif(configs.G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + configs.G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + " (arb.)" 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + ' (' + configs.G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'plabel' in auxDict:
      ystr = auxDict['plabel'] + " (arb.)" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = zstr + auxDict['ylabel'] + ' (' + configs.G['zdimscale_str'] + auxDict["yunit_str"] + ')' 

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

def EvolveR(*args,**kwargs):

# view = [elev,azim]
  numFiles = 6
  if len(args) > 2:
    numFiles = args[2]
  incr = 360/numFiles

  elev = 57
  if 'view' in kwargs:
    view = kwargs['view']
    elev = view[0]
    del kwargs['view']

  if 'elev' in kwargs:
    elev = kwargs['elev']

  kwargs['view'] = [elev,incr]
  ax = Evolve(*args,**kwargs)
  ax.axis('off')
  ax.view_init(elev,0)
  ax.set_title('view = (' + str(elev) + ',0)')
  pl.draw()
  pl.savefig('EvolveR_0.png')
  imageList = ['EvolveR_0.png']

  for angle in range(incr,360,incr):
    ax.view_init(elev,angle)
    ax.set_title('view = (' + str(elev) + ',' + str(angle) + ')')
    pl.draw()
    imageFile = 'EvolveR_' + str(angle) + '.png'
    pl.savefig(imageFile)
    imageList.append(imageFile)

  print(imageList)
  movLength = MovLength(**kwargs)
  GenMovie(imageList,'EvolveR',movLength)

def EvolveL(*args,**kwargs):
  """
  Plots the log10(y) evolution of 1D data in a mesh-like 3D figure. 

  EvolveL(fileID,fileRange,plotLimits):
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
      maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,decades]
    plotLimits: Specifies the plotting range of the Evolve function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      decades: Number of decades of output to include in log plots
    
    e.g. Evolve('T',[10,0,60],[0,1,-10,10]) will produce an Evolve plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. Evolve('R') will produce an Evolve plot using all 'R' fileID data
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
      if(configs.G["scale"] == 'nonDim'):
        x1.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x1.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x1.append(float(auxDict['pval']))
    else:
      x1.append(num)
      num = num + 1

  ymin = np.amin(x1)
  ymax = np.amax(x1)

  width = float(configs.G['EvolveWidthL'])
  height = float(configs.G['EvolveHeightL'])
  if 'size' in kwargs:
    array = kwargs['size']
    width = array[0]
    height = array[1]

  fig = pl.figure(figsize=(width,height))
  ax = fig.add_subplot(1,1,1,projection = '3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  count = 0
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    x,y,auxDict = GetData1D(fileID,repNum)
    auxDict['decades'] = configs.G['decades']
    x,y,auxDict = ProcessData1D(x,y,auxDict,**kwargs)
    y = np.log10(y)
    ax.plot(x,x1[count]*np.ones_like(x),y,color = 'black')
    count = count + 1

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    auxDict['zlim'] = ylim
  auxDict['ylim'] = [ymin,ymax]

  pl.tight_layout()
  pl.xlim([x[0],x[-1]])
  pl.ylim([ymin,ymax])
  AuxEvolveLabel(ax,auxDict)
  pl.ion()
  pl.show()
  return ax

def EvolveM(*args,**kwargs):
  fileList = GenFileList(*args)
  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,60)

  if len(args) > 3:
    view = args[3]  
    if len(view) > 0:
      auxDict['angle1'] = view[0]
    if len(view) > 1:
      auxDict['angle2'] = view[1]

  count = 0; 
  Z = np.zeros((len(x),len(y)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,60)
    Z[count,:] = z 
    count = count + 1

  X,Y = np.meshgrid(y,x)

  width = float(configs.G['EvolveWidth'])
  height = float(configs.G['EvolveHeight'])
  fig = pl.figure(figsize=(width,height))
  fig.clf()
  ax = fig.add_subplot(1,1,1,projection = '3d')
  wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1,color='black')
  pl.xlim([x[0],x[-1]])
  AuxSurfaceLabel(ax,auxDict)
  pl.ion()
  pl.show()
  return True



def EvolveS(*args,**kwargs):
  fileList = GenFileList(*args)
  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,50)

  if len(args) > 3:
    view = args[3]  
    if len(view) > 0:
      auxDict['angle1'] = view[0]
    if len(view) > 1:
      auxDict['angle2'] = view[1]

  count = 0; 
  Z = np.zeros((len(x),len(y)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,50)
    Z[count,:] = z 
    count = count + 1

  X,Y = np.meshgrid(y,x)
  width,height = _SurfaceSize(*args)
  fig = pl.figure(figsize=(width,height))
  ang1,ang2 = GetView(*args)
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs.G["cmap"]),linewidth=0,antialiased=True,shade=True) 
  pl.xlim([y[0],y[-1]])
  pl.ylim([x[0],x[-1]])
  AuxSurfaceLabel(ax,auxDict)
  pl.ion()
  pl.show()
  return True

def AuxSurfaceLabel(ax,auxDict):
  xstr = ""
  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + auxDict["xscale_str"] + ')' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
       xstr = auxDict['xlabel']
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + configs.G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + " [arb.]" 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + configs.G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = ystr + auxDict['plabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + '(' + configs.G['ydimscale_str'] + auxDict["yunit_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + " [arb.]" 

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    ax.set_zlim3d(ylim)

  xstr = '$' + xstr + '$'
  ystr = '$' + ystr + '$'
  zstr = '$' + zstr + '$'
  ax.set_xlabel(xstr)
  ax.set_ylabel(ystr)
  ax.set_zlabel(zstr)

  if 'angle1' in auxDict and 'angle2' in auxDict:
    ax.view_init(auxDict['angle1'],auxDict['angle2'])

  numTicks = int(configs.G['NumberSurfaceTicks'])
  ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.zaxis.set_major_locator(ticker.LinearLocator(4))
  
  labelType = str(configs.G['SurfaceTickFormat'])
  ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))


def ProcessEvolvePoints(x,y,numX):
  xvals = np.linspace(x[0],x[-1],numX)
  y = np.interp(xvals,x,y)
  x = xvals
  return (x,y)


def EvolveLS(*args,**kwargs):
  fileList = GenFileList(*args)
  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  auxDict['decades'] = configs.G['decades']
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,120)

  if 'view' in kwargs:
    view = kwargs['view']
    auxDict['angle1'] = view[0]
    auxDict['angle2'] = view[1]

  count = 0; 
  Z = np.zeros((len(x),len(y)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    auxDict['decades'] = configs.G['decades']
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,120)
    z = np.log10(z)
    Z[count,:] = z 
    count = count + 1

  X,Y = np.meshgrid(y,x)
  fig = pl.figure(figsize=(float(configs.G['EvolveWidth']),float(configs.G['EvolveHeight'])))
  fig.clf()
  ax = fig.gca(projection='3d')
  surf = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=cm.jet,linewidth=0,antialiased=False) 
  AuxSurfaceLabel(ax,auxDict)
  pl.xlim([y[0],y[-1]])
  pl.ylim([x[0],x[-1]])
  pl.ion()
  pl.show()
  return True

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
    print("Evolve fileList not generated. ")  
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
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum,*plotArgs)
  y,z,auxDict = ProcessData1D(y,z,auxDict)
  y,z = ProcessEvolvePoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum,*plotArgs)
    y,z,auxDict = ProcessData1D(y,z,auxDict)
    y,z = ProcessEvolvePoints(y,z,50)
    Z[:,count] = z 
    count = count + 1

  Y,X = np.meshgrid(y,x)
#  X,Y = np.meshgrid(x,y)
#  X = np.transpose(X)
#  Y = np.transpose(Y)
  Z = np.transpose(Z)
  return (X,Y,Z,auxDict)

def EvolveC(*args):
  (X,Y,Z,auxDict) = GetContourData(*args)
  width = 6;
  height = 8;
  fig = pl.figure(figsize=(width,height))
  CS = pl.contourf(Y,X,Z,200,interpolation='bicubic')
  AuxContourLabel(CS,auxDict)
  pl.ion()
  pl.show()
  return True

def EvolveI(*args):
  (X,Y,Z,auxDict) = GetContourData(*args)
  width = 6;
  height = 8;
  lightS = LightSource(azdeg=0,altdeg=5)
  rgb = lightS.shade(Z,pl.cm.hot)
  fig = pl.figure(figsize=(width,height))
  ax = pl.subplot(111)
  #im = ax.imshow(rgb,aspect='auto',interpolation='bicubic')
  im = ax.imshow(rgb,aspect='auto',interpolation='bicubic')
#  AuxContourLabel(CS,auxDict)
  pl.ion()
  pl.show()
  return True


def AuxContourLabel(CS,auxDict):
  xstr = ""
  ystr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] 
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + auxDict["xscale_str"] + ')' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] 
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel']
  elif(configs.G['scale'] == 'dimscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      xstr = auxDict['plabel'] + '(' + configs.G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      xstr = ystr + auxDict['plabel'] + " [arb.]" 
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + '(' + configs.G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      ystr = auxDict['xlabel'] + " [arb.]" 
  xstr = '$' + xstr + '$'
  ystr = '$' + ystr + '$'
  CS.ax.set_xlabel(ystr)
  CS.ax.set_ylabel(xstr)


def EvolveB(*args,**kwargs):
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
    print("Evolve fileList not generated. ")  
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
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,50)
    Z[:,count] = z 
    count = count + 1

  X,Y = np.meshgrid(x,y)
  pl.figure(figsize=(float(configs.G['EvolveWidth']),float(configs.G['EvolveHeight'])))
  CS = pl.contour(X,Y,Z,6,colors='k')
  AuxContourLabel(CS,auxDict)
  pl.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
  pl.ion()
  pl.show()
  return True

def EvolveLB(*args,**kwargs):
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
    print("Evolve fileList not generated. ")  
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
      if(configs.G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,50)

  count = 0; 
  Z = np.zeros((len(y),len(x)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    auxDict['decades'] = configs.G['decades']
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,50)
    Z[:,count] = z
    count = count + 1

  X,Y = np.meshgrid(x,y)
  pl.figure(figsize=(float(configs.G['EvolveWidth']),float(configs.G['EvolveHeight'])))
  CS = pl.contour(X,Y,Z,colors = 'k',locator=ticker.LogLocator())
  AuxContourLabel(CS,auxDict)
  pl.clabel(CS,fontsize=9,inline=1,fmt='%0.02e')
  pl.ion()
  pl.show()
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
    width = float(configs.G['SurfaceWidth'])
    height = float(configs.G['SurfaceHeight'])

  return (width,height) 

def GetView(*args):
  if len(args) > 3:
    view = args[3]  
    if len(view) ==  1:
      ang1 = view[0] 
      ang2 = int(configs.G['surfaceAzimuth'])
    elif len(view) == 2:
      ang1 = view[0] 
      ang2 = view[1] 
    else:
      ang1 = int(configs.G['surfaceElevation'])
      ang2 = int(configs.G['surfaceAzimuth'])
  else:
    ang1 = int(configs.G['surfaceElevation'])
    ang2 = int(configs.G['surfaceAzimuth'])
  return(ang1,ang2)


#def EvolveContour(fileID,evolveNum = 40,simNum = 0):
#  pl.clf()
#  configs.DefaultLS()
#  fileList = GetEvolveFileList(fileID,evolveNum,simNum)
#  if not fileList:
#    return False
#  fileLen = len(fileList)
#  xmin = 0.0; xmax = 0.0; ymin = 0.0; ymax = 0.0; zmin = 0.0; zmax = 0.0
#  count = 0; titleList = []; xscale = 1.0; yscale = 1.0; zscale = 1.0 
#  yminVec = []; ymaxVec = []; xminVec = []; xmaxVec = []; 
#
#  auxDict = ProcessAux(fileList[0])
#  xlen = 0
#  x = []
#  with open(fileList[0]) as f:
#    data = np.genfromtxt(f,skip_header=len(auxDict))
#    x,z,xmin,xmax,zmin,zmax = ProcessData1D(data[:,0],data[:,1],auxDict)
#    xlen = len(x)
#    if "xscale" in auxDict:
#      if(configs.G["scale"] == 'nonDim'):
#        x = x/float(auxDict["xscale"])
#      elif(configs.G["scale"] == 'dimscale'):
#        x = x/float(configs.G['xdimscale'])
#
#  if 'pscale' in auxDict:
#    yscale = float(auxDict['pscale']); 
#  if 'xscale' in auxDict:
#    xscale = float(auxDict['xscale'])
#  if 'yscale' in auxDict:
#    zscale = float(auxDict['yscale'])
#
#  count = 0; 
#  y = []
#  Z = np.zeros((fileLen,xlen))
#  for file in fileList:
#    auxDict = ProcessAux(file) 
#    if "pscale" in auxDict:
#      if(configs.G["scale"] == 'nonDim'):
#        y.append(float(auxDict['pval'])/float(auxDict['pscale']))
#      elif(configs.G["scale"] == 'dimscale'):
#        y.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
#    else:
#      y.append(float(auxDict['pval']))
#    with open(file) as f:
#      data = np.genfromtxt(f,skip_header=len(auxDict))
#      xgarb,ztemp,xmin,xmax,zmin,zmax = ProcessData1D(data[:,0],data[:,1],auxDict)
#      if "yscale" in auxDict:
#        if(configs.G["scale"] == 'nonDim'):
#          ztemp = ztemp/float(auxDict["yscale"])
#        elif(configs.G["scale"] == 'dimscale'):
#          ztemp = ztemp/float(configs.G['ydimscale'])
#    Z[count,:] = ztemp 
#    count = count + 1
#
#
#  ymin = np.amin(y); ymax = np.amax(y) 
#  X,Y = np.meshgrid(x,y)
#  CS = pl.contourf(X,Y,Z)
#  AuxContourLabel(auxDict,CS,xmin,xmax,ymin,ymax,xscale,yscale)
#  pl.ion()
#  pl.show()
#  return True



