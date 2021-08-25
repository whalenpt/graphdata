
from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 

from graphdata.shared.figsizes import ContourfSize
from graphdata.shared.shared import ProcessComplex
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared import LabelX
from graphdata.shared.shared import LabelY
from graphdata.shared.shared import ProcessDecadeLimits

from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.shared2D import ProcessData2D

from graphdata.shared.contours import ContourLevels
from graphdata.shared.contours import ContourLevelsL
from graphdata.shared.contours import ProcessContourLimitZ


from graphdata import plt
from graphdata import configs 
from graphdata import np 

def contourf(filename,levels=None,figsize=None,xlim=None,ylim=None,zlim=None,\
        decades=None,complex_op=None,overwrite=False,**kwargs):
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
        complex_op : string in the following list ('real','imag','power','absolute','angle')
            complex operation used to plot complex data
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.contourf plot

    OUTPUTS:

        None

    """

    x,y,Z,auxDict = LoadData2D(filename)
    Z = ProcessComplex(complex_op,Z)
    ExtendDictionary(auxDict,levels=levels,figsize=figsize,xlim=xlim,ylim=ylim,zlim=zlim,\
            decades=decades,overwrite=overwrite)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
    figsize = ContourfSize(figsize)
    X,Y = np.meshgrid(x,y)
    if zlim is not None:
        Z = ProcessContourLimitZ(zlim,Z)

    levels,levelTicks,levelLabels = ContourLevels(levels,Z)
    if overwrite:
        fig = plt.figure("Contourf",figsize=figsize)
        fig.clf()
    else:
        fig = plt.figure(figsize=figsize)

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
        del kwargs['cmap']
    else:
        cmap = str(configs._G["cmap"])

    CS = plt.contourf(X,Y,Z,levels,cmap=cmap,**kwargs)
    ax = plt.gca()
    ax.set_xlabel(LabelX(auxDict))
    ax.set_ylabel(LabelY(auxDict))
    CB = plt.colorbar(ticks=levelTicks,format='%0.2e')
    plt.ion()
    plt.show()

def contourflog(filename,numlevels,decades,figsize=None,xlim=None,ylim=None,
        complex_op=None,overwrite=False,**kwargs):
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
        complex_op : string (note this parameter is not used unless the data is complex)
            cop = 'power' -> for complex data graph the surface of the power of the data
            cop = 'absolute' -> for complex data graph the surface of the absolute value (abs(data))
            cop = 'angle' -> for complex data graph the surface of the absolute value (angle(data))
        overwrite: bool
            false (default) -> create new contourf plot figure
            true -> clear figure named 'Contourf' and make new contourf plot
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.contourf plot

    OUTPUTS:

        None

    """

    x,y,Z,auxDict = LoadData2D(filename)
    Z = ProcessComplex(complex_op,Z)
    ExtendDictionary(auxDict,decades=decades,figsize=figsize,\
            xlim=xlim,ylim=ylim,overwrite=overwrite)
    x,y,Z,auxDict = ProcessData2D(x,y,Z,auxDict)
#    Z = ProcessDecadeLimits(decades,Z)

    figsize = ContourfSize(figsize)
    X,Y = np.meshgrid(x,y)
    levels,levelTicks,levelLabels = ContourLevelsL(numlevels,decades,Z)

    if overwrite:
        fig = plt.figure("Contourflog",figsize=figsize)
        fig.clf()
    else:
        fig = plt.figure(figsize=figsize)

    if 'cmap' in kwargs:
        cmap = kwargs['cmap']
        del kwargs['cmap']
    else:
        cmap = str(configs._G["cmap"])

    CS = plt.contourf(X,Y,Z,levels,cmap=cmap,locator=ticker.LogLocator(),**kwargs)
    ax = plt.gca()
    ax.set_xlabel(LabelX(auxDict))
    ax.set_ylabel(LabelY(auxDict))
    CB = plt.colorbar(ticks = ticker.LogLocator())
    plt.ion()
    plt.show()


