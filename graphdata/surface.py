
#!/usr/bin/python
# Filename: surface.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 

from graphdata.shared.shared2D import GetData2D 
from graphdata.shared.shared2D import GetDataLog2D 
from graphdata.shared.shared2D import ProcessData2D 
from graphdata.shared.shared2D import GetView
from graphdata.shared.shared2D import AuxAxes3DLabel

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def surface(*args,**kwargs):
  """
  Surface plot of 2D data. 

  Surface(fileID,fileNumber,plotLimits,**kwargs):
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

  """

  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  if 'square' in kwargs:
    if kwargs['square'] == 'on':
      Z = pow(Z,2)

  X,Y = np.meshgrid(x,y)
  elev,azim = GetView(**kwargs)
  auxDict['elev'] = elev 
  auxDict['azim'] = azim

  width,height = _SurfaceSize(*args)
  if 'overwrite' in kwargs and kwargs['overwrite']:
      fig = plt.figure("Surface",figsize=(width,height))
      fig.clf()
  else:
      fig = plt.figure(figsize=(width,height))

  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs._G["cmap"]),linewidth=0,antialiased=True,shade=True) 
  
  AuxAxes3DLabel(ax,auxDict)
  plt.ion()
  plt.show()
  return p 

def _SurfaceSize(**kwargs):
    if 'figsize' in kwargs:
        return kwargs['figsize']
    else:
        width = float(configs._G['SurfaceWidth'])
        height = float(configs._G['SurfaceHeight'])
        return width,height




