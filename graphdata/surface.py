
#!/usr/bin/python
# Filename: surface.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.figsizes import PlotSize
from graphdata.shared.shared2D import GetView
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared2D import AuxAxes3DLabel

#from graphdata.shared.shared2D import GetDataLog2D 
#from graphdata.shared.shared2D import ProcessData2D 

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def surface(filename,figsize=None,xlim=None,ylim=None,zlim=None,overwrite=False,**kwargs)
    """
    Graph of 2D data file using Matplotlib plt.surface

    INPUTS:
        filename: string
            name of file containing 1D data to be plotted
        figsize: tuple (width,height)
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            x-axis limits of graph
        overwrite: bool
            add lines to an existing plt.plot graph if it exists
            (default is False which will plot graph on a new figure)
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.loglog plot

    OUTPUTS:

        ax : matplotlib.axes.Axes
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """

    x,y,Z,auxDict = LoadData2D(filename)
    figsize = PlotSize(figsize)
    if xlim is None:
        xlim = [x[0],x[-1]]
    if ylim is None:
        ylim = [y[0],y[-1]]
    if zlim is None:
        zlim = [np.min(Z),np.max(Z)]

    elev,azim = GetView(**kwargs)
    auxDict['elev'] = elev 
    auxDict['azim'] = azim
    ExtendDictionary(auxDict,figsize=figsize,xlim=xlim,ylim=ylim,zlim=zlim,overwrite=overwrite)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
    X,Y = np.meshgrid(x,y)

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
    else
        cmap = str(configs._G["cmap"])

    if overwrite:
        fig = plt.figure("Surface",figsize=figsize)
        fig.clf()
    else:
        fig = plt.figure(figsize=figsize)

    ax = fig.gca(projection='3d')
    ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=cmap,linewidth=0,antialiased=True,shade=True) 
  
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




