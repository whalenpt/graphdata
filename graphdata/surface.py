
#!/usr/bin/python
# Filename: surface.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 

from graphdata.shared.shared import ProcessComplex
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.figsizes import SurfaceSize
from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.shared2D import ProcessData2D
from graphdata.shared.shared2D import GetView
from graphdata.shared.shared2D import Labels2D

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def surface(filename,figsize=None,xlim=None,ylim=None,zlim=None,\
        overwrite=False,complex_op=None,**kwargs):
    """
    Graph of 2D data file using Matplotlib plt.surface

    INPUTS:
        filename: string
            name of file containing 2D data to be plotted
        figsize: tuple (width,height)
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            y-axis limits of graph
        zlim: np.array
            z-axis limits of graph
        overwrite: bool
            false (default) -> create new surface plot figure
            true -> clear figure named 'Surface' and make new surface plot
        complex_op : string in the following list ('real','imag','power','absolute','angle')
            complex operation used to plot complex data
            
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.surface plot

    OUTPUTS:

        None

    """

    x,y,Z,auxDict = LoadData2D(filename)
    Z = ProcessComplex(complex_op,Z)
    ExtendDictionary(auxDict,figsize=figsize,xlim=xlim,ylim=ylim,overwrite=overwrite)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)

    figsize = SurfaceSize(figsize)
    elev,azim = GetView(**kwargs)
    auxDict['elev'] = elev 
    auxDict['azim'] = azim

    if xlim is None:
        xlim = [x[0],x[-1]]
    if ylim is None:
        ylim = [y[0],y[-1]]

    X,Y = np.meshgrid(x,y)

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
    else:
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
    if zlim:
        ax.set_zlim3d(zlim)
  
    xlabel,ylabel,zlabel = Labels2D(auxDict)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.view_init(auxDict['elev'],auxDict['azim'])
  
    numTicks = int(configs._G['NumberSurfaceTicks'])
    ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
    ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
    ax.zaxis.set_major_locator(ticker.LinearLocator(4))
    
    labelType = str(configs._G['SurfaceTickFormat'])
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
    ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))

    plt.ion()
    plt.show()



