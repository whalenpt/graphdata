
from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.shared2D import ProcessData2D

from graphdata.shared.contours import ContourLevels
from graphdata.shared.contours import ContourLevelsL
from graphdata.shared.contours import ProcessContourLimitZ

from graphdata.shared.figsizes import ContourfSize
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared import LabelX
from graphdata.shared.shared import LabelY
from graphdata.shared.shared import ProcessDecadeLimits
from graphdata.shared.shared import ProcessComplex

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def contourf(filename,levels=None,figsize=None,xlim=None,ylim=None,zlim=None,\
        decades=None,cop='power',overwrite=False,**kwargs):
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

        ax : matplotlib.axes._base._AxesBase

    """

    x,y,Z,auxDict = LoadData2D(filename)
    if(np.iscomplexobj(Z)):
        Z = ProcessComplex(Z,cop)
    ExtendDictionary(auxDict,levels=levels,figsize=figsize,xlim=xlim,ylim=ylim,zlim=zlim,\
            decades=decades,overwrite=overwrite)
    figsize = ContourfSize(figsize)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
    X,Y = np.meshgrid(x,y)
    if zlim is not None:
        Z = ProcessContourLimitZ(zlim,Z)
    if decades is not None:
        Z = ProcessDecadeLimits(Z,decades)

    levels,levelTicks,levelLabels = ContourLevels(levels,Z)
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

def contourflog(filename,numlevels,decades,figsize=None,xlim=None,ylim=None,
        cop='power',overwrite=False,**kwargs):
    """
    Logged data contour plot of 2D data file using Matplotlib plt.contourf

    INPUTS:
        filename: string
            name of file containing 2D data to be plotted
        numlevels : int
            number of contour levels to plot
        decades: int
            maximum number of log10 decades to be plotted (starting with max value)
        figsize: tuple (width,height) 
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            y-axis limits of graph
        overwrite: bool
            false (default) -> create new contourf plot figure
            true -> clear figure named 'Contourf' and make new contourf plot
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.contourf plot

    OUTPUTS:

        ax : matplotlib.axes._base._AxesBase

    """

    x,y,Z,auxDict = LoadData2D(filename)
    if(np.iscomplexobj(Z)):
        Z = ProcessComplex(Z,cop)
    ExtendDictionary(auxDict,decades=decades,figsize=figsize,\
            xlim=xlim,ylim=ylim,overwrite=overwrite)
    figsize = ContourfSize(figsize)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
    X,Y = np.meshgrid(x,y)
    Z = ProcessDecadeLimits(Z,decades)
    levels,levelTicks,levelLabels = ContourLevelsL(numlevels,decades,Z)

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

    CS = plt.contourf(X,Y,Z,levels,cmap=cmap,locator=ticker.LogLocator(),**kwargs)
    ax.set_xlabel(LabelX(auxDict))
    ax.set_ylabel(LabelY(auxDict))
    CB = plt.colorbar(ticks=levelTicks)
    ax.set_yticklabels(levelLabels)
    plt.ion()
    plt.show()
    return ax


