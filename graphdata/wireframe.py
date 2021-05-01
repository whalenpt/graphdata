
from graphdata import plt
from graphdata import np 
from graphdata import configs 
from graphdata.shared.shared2D import GetData2D 
from graphdata.shared.shared2D import ProcessData2D 
from graphdata.shared.shared2D import GetView
from graphdata.shared.shared2D import AuxAxes3DLabel


def wireframe(*args,**kwargs):
  """
  Wireframe plot of 2D data. 

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

    **kwargs (optional)
    figsize : array or tuple containing width and height of figure

    overwrite : np.bool
        True -> current wireframe graph will be overwritten if it exists 
        False -> new figure created for each wireframe graph

    elev : float
        figure elevation as used in view_init
    azim : float
        figure azimuth as used in view_init

  """

  x,y,Z,auxDict = GetData2D(*args)
  x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
  X,Y = np.meshgrid(x,y)
  elev,azim = GetView(*args)
  auxDict['elev'] = elev
  auxDict['azim'] = azim

  width,height = _WireSize(*args)
  if 'overwrite' in kwargs and kwargs['overwrite']:
      fig = plt.figure("Wireframe",figsize=(width,height))
      fig.clf()
  else:
      fig = plt.figure(figsize=(width,height))

  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  surf = ax.plot_wireframe(X,Y,Z,rstride=1,cstride=1,color='black') 
  AuxAxes3DLabel(ax,auxDict)
  plt.ion()
  plt.show()
  return surf 

def _WireSize(**kwargs):

    if 'figsize' in kwargs:
        width,height = kwargs['figsize']
    else:
        width = int(configs._G['WireWidth'])
        height = int(configs._G['WireHeight'])
    return width,height



