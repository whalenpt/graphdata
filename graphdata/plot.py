
from graphdata.shared.shared1D import AuxPlotLabel1D
from graphdata.shared.shared1D import ProcessData1D
from graphdata.shared.shared1D import LoadData1D
from graphdata.shared.figsizes import PlotSize
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared import ProcessComplex
from graphdata import plt
from graphdata import np
from graphdata import configs

def plot(filename,figsize=None,xlim=None,ylim=None,\
        overwrite=False,complex_op=None,**kwargs):
    """
    Graph of 1D data file using Matplotlib plt.plot

    INPUTS:
        filename: string
            name of file containing 1D data to be plotted
        figsize: tuple (width,height)
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            y-axis limits of graph
        overwrite: bool
            add lines to an existing plt.plot graph if it exists
            (default is False which will plot graph on a new figure)
        complex_op : string in the following list ('real','imag','power','absolute','angle')
            complex operation used to plot complex data
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.loglog plot

    OUTPUTS:

        ax : matplotlib.axes.Axes
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """
    x,y,auxDict = LoadData1D(filename)
    if complex_op is not None:
        y = ProcessComplex(complex_op,y)
    ExtendDictionary(auxDict,figsize=figsize,xlim=xlim,ylim=ylim,overwrite=overwrite)
    x,y,auxDict = ProcessData1D(x,y,auxDict)

    figsize = PlotSize(figsize)
    if xlim is None:
        xlim = [x[0],x[-1]]
    if ylim is None:
        ylim = [np.min(y),np.max(y)]

    labs = plt.get_figlabels()
    if overwrite:
        if "Plot" not in labs:
            configs.defaultLS()
        else:
            configs.toggleLS()
        plt.figure("Plot",figsize=figsize)
        if(configs.LS == 'k--'):
            plt.plot(x,y,configs.LS,dashes = (4,2),**kwargs)
        else:
            plt.plot(x,y,configs.LS,**kwargs)
    else:
        plt.figure(figsize=figsize)
        configs.defaultLS()
        plt.plot(x,y,configs.LS,**kwargs)

    AuxPlotLabel1D(auxDict)
    if 'legend' in auxDict and configs._G['legend'] == 'on':
        plt.legend([str(auxDict["legend"])],loc='best')
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.ion()
    plt.show()
    ax = plt.gca()
    return ax




