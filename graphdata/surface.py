
#!/usr/bin/python
# Filename: surface.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 

from .helper import GetData2D 
from .helper import GetDataL_2D 
from .shared2D import ProcessData2D 

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def Surface(*args,**kwargs):
  """
  Surface plot of 2D data. 

  Surface(fileID,fileNumber,plotLimits,viewingAngles,figSize,powOnOff):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for RT data are SQ_RT_0.dat,SQ_RT_1.dat,
      SQ_RT_2.dat,..., then the fileID is simply 'SQ_RT'

    fileNumber: Specifies which data file number to plot e.g.
      Surface('RT',10) will make a surface plot of the data file 
      'RT_10.dat' if this data file is available

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the Surface plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. Surface('RT',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. Surface('RT',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. Surface('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits
          between 0 and 1, y-limits between -2 and 2, and z-limits from 0 to 10
        e.g. Surface('RT',10,[]) is the same as Surface('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. This option is primarily useful in
      generating movies since a single plot can be rotated manually
    
    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. Surface('RT',10,[],[],[14,5]) will plot a contour image with
            a width of 14 inches and a height of 5 inches

  """

  width,height = _SurfaceSize(*args)
  fig = plt.figure(figsize=(width,height))
  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  if 'square' in kwargs:
    if kwargs['square'] == 'on':
      Z = pow(Z,2)

  X,Y = np.meshgrid(x,y)
  ang1,ang2 = GetView(*args)
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs.G["cmap"]),linewidth=0,antialiased=True,shade=True) 
  AuxSurfaceLabel(ax,ang1,ang2,auxDict)
  plt.ion()
  plt.show()
  return p 

def SurfaceH(*args):
  """
  Surface plot of 2D data. The functions SurfaceH and Surface differ only in
  that SurfaceH overwrites the current figure plot and replaces it with a
  new one, wheras Surface will create a new figure and plot the Surface
  graph on that new figure instance. 

  SurfaceH(fileID,fileNumber,plotLimits,viewingAngles,figSize):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
      if data files for RT data are SQ_RT_0.dat,SQ_RT_1.dat,
      SQ_RT_2.dat,..., then the fileID is simply 'SQ_RT'

    fileNumber: Specifies which data file number to plot e.g.
      SurfaceH('RT',10) will make a surface plot of the data file 
      'RT_10.dat' if this data file is available

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the SurfaceH plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. SurfaceH('RT',10,[0,1]) will plot data with x-limits between 0 and 1 
        e.g. SurfaceH('RT',10,[0,1,-2,2]) will plot data with x-limits between 
          0 and 1 and y-limits between -2 and 2. 
        e.g. SurfaceH('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits
          between 0 and 1, y-limits between -2 and 2, and z-limits from 0 to 10
        e.g. SurfaceH('RT',10,[]) is the same as SurfaceH('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. This option is primarily useful in
      generating movies since a single plot can be rotated manually

    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. Surface('RT',10,[],[],[14,5]) will plot a contour image with
            a width of 14 inches and a height of 5 inches

  """
  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  X,Y = np.meshgrid(x,y)
  ang1,ang2 = GetView(*args)
  width,height = _SurfaceSize(*args)
  fig = plt.figure("SurfaceH",figsize=(width,height))
  fig.clf()
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs.G["cmap"]),linewidth=0,antialiased=True,shade=True) 
  AuxSurfaceLabel(ax,ang1,ang2,auxDict)
  plt.ion()
  plt.show()
  return p  

def Wire(*args):
  """
  Wire plot of 2D data. 

  Wire(fileID,fileNumber,plotLimits,viewingAngles,figSize):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
    if data files for SQ_RT data are SQ_RT_0.dat,SQ_RT_1.dat,SQ_RT_2.dat,...
    then the fileID is simply 'SQ_RT'

    fileNumber: Specifies which data file number to plot e.g. Wire('RT',10)
    will make a surface plot of the data file 'RT_10.dat' if this data file
    is available

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the Wire plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. Wire('RT',10,[0,1]) will plot data with x-limits between 
          0 and 1 
        e.g. Wire('RT',10,[0,1,-2,2]) will plot data with x-limits between
          0 and 1 and y-limits between -2 and 2.  
        e.g. Wire('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits 
        between 0 and 1, y-limits between -2 and 2, and z-limits from 
        0 to 10 
        e.g. Wire('RT',10,[]) is the same as Wire('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. This option is primarily useful in
      generating movies since a single plot can be rotated manually
  
    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. Wire('RT',10,[],[],[14,5]) will plot a contour image with
            a width of 14 inches and a height of 5 inches

  """

  width,height = _WireSize(*args)
  fig = plt.figure(figsize=(width,height))
  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  X,Y = np.meshgrid(x,y)
  ang1,ang2 = GetView(*args)
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  surf = ax.plot_wireframe(X,Y,Z,rstride=1,cstride=1,color='black') 
  AuxSurfaceLabel(ax,ang1,ang2,auxDict)
  plt.ion()
  plt.show()
  return surf 

def WireH(*args):
  """
  Wire plot of 2D data. The functions WireH and Wire differ only in that 
  WireH overwrites the current figure plot and replaces it with a new one,
  wheras Wire will create a new figure and plot the Wire graph on that
  new figure instance. 

  WireH(fileID,fileNumber,plotLimits,viewingAngles,figSize):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat e.g.
    if data files for SQ_RT data are SQ_RT_0.dat,SQ_RT_1.dat,SQ_RT_2.dat,...
    then the fileID is simply 'SQ_RT'

    fileNumber: Specifies which data file number to plot e.g. WireH('RT',10)
    will make a surface plot of the data file 'RT_10.dat' if this data file
    is available

    plotLimits = [minX,maxX,minY,maxY,minZ,maxZ]
    plotLimits: Specifies the WireH plot limits 
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      minZ:  Minimum z value limit
      maxZ:  Maximum z value limit
      If no plotLimit list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables. The plotLimits
      list can be empty, contain just xmin and xmax limits, contain just
      xmin,xmax,ymin,and ymax, or contain all limits
        e.g. WireH('RT',10,[0,1]) will plot data with x-limits between 
          0 and 1 
        e.g. WireH('RT',10,[0,1,-2,2]) will plot data with x-limits between
          0 and 1 and y-limits between -2 and 2.  
        e.g. WireH('RT',10,[0,1,-2,2,0,10]) will plot data with x-limits 
        between 0 and 1, y-limits between -2 and 2, and z-limits from 
        0 to 10 
        e.g. WireH('RT',10,[]) is the same as WireH('RT',10)

    viewingAngles = [azimuth,elevation]
    viewingAngles: Determines angles at which you see the surface plot from an 
      elevation and from the side. This option is primarily useful in
      generating movies since a single plot can be rotated manually

    figSize = [width,height]
    figSize: Specifies the size of the image to be ploted. 
      width: Width of image in inches 
      height: Height of image in inches 
        eg. WireH('RT',10,[],[],[14,5]) will plot a contour image with
            a width of 14 inches and a height of 5 inches

  """
  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  X,Y = np.meshgrid(x,y)
  ang1,ang2 = GetView(*args)
  width,height = _WireSize(*args)
  fig = plt.figure("WireH",figsize=(width,height))
  fig.clf()
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  surf = ax.plot_wireframe(X,Y,Z,rstride=1,cstride=1,color='black') 
  AuxSurfaceLabel(ax,ang1,ang2,auxDict)
  plt.ion()
  plt.show()
  return surf 

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

def _WireSize(*args):

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
    width = int(configs.G['WireWidth'])
    height = int(configs.G['WireHeight'])

  return (width,height) 



def AuxSurfaceLabel(ax,ang1,ang2,auxDict):

  numTicks = int(configs.G['NumberSurfaceTicks'])
  ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
#  ax.zaxis.set_major_locator(ticker.LinearLocator(4))

  xstr = ""
  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '[' + auxDict["xscale_str"] + ']' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + '[' + auxDict["yscale_str"] + ']' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] 
    if 'zscale_str' in auxDict and 'zlabel' in auxDict:
      zstr =  auxDict['zlabel'] + '[' + auxDict["zscale_str"] + ']' 
    elif 'zscale_str' not in auxDict and 'zlabel' in auxDict:
      zstr =  auxDict['zlabel'] 
#    labelType = str(configs.G['SurfaceTickFormat'])
#    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))

  elif(configs.G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '[' + auxDict["xunit_str"] + ']' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
       xstr = auxDict['xlabel']
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel']  + '[' + auxDict["yunit_str"] + ']' 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] 
    if 'zunit_str' in auxDict and 'zlabel' in auxDict:
      zstr =  auxDict['zlabel'] + '[' + auxDict["zunit_str"] + ']' 
    elif 'zscale_str' not in auxDict and 'zlabel' in auxDict:
      zstr =  auxDict['zlabel'] 
    labelType = str(configs.G['SurfaceTickFormat'])

#    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    zfmt = ax.zaxis.get_major_formatter() 
#    zfmt.set_powerlimits([-1,1])

  elif(configs.G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + "[" + configs.G['xdimscale_str'] + auxDict["xunit_str"] + "]" 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + "[" + configs.G['ydimscale_str'] + auxDict["yunit_str"] + "]" 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = ystr + auxDict['ylabel'] + " [arb.]" 
    if 'zunit_str' in auxDict and 'zlabel' in auxDict:
      zstr = auxDict['zlabel'] + "[" + configs.G['zdimscale_str'] + auxDict["zunit_str"] + "]" 
    elif 'zscale_str' not in auxDict and 'zlabel' in auxDict:
      zstr = auxDict['zlabel'] + " [arb.]" 

#    labelType = str(configs.G['SurfaceTickFormat'])
#    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
#    zfmt = ax.zaxis.get_major_formatter() 
#    zfmt.set_powerlimits([-2,2])

  if 'zmin' in auxDict and 'zmax' in auxDict:
    ax.set_zlim3d([auxDict['zmin'],auxDict['zmax']])

  xstr = '$' + xstr + '$'
  ystr = '$' + ystr + '$'
  zstr = '$' + zstr + '$'
  ax.set_xlabel(xstr)
  ax.set_ylabel(ystr)
  ax.set_zlabel(zstr)

  ax.view_init(ang1,ang2)

 




