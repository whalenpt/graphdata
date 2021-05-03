
from graphdata.shared.shared1D import AuxPlotLabelLL1D 
from graphdata.shared.shared1D import ProcessData1D 
from graphdata.shared.shared1D import LoadData1D 
from graphdata.shared.figsizes import LogLogSize
from graphdata.shared.shared import ExtendDictionary
from graphdata import plt
from graphdata import np 
from graphdata import configs 

def loglog(filename,figsize=None,decades=None,xlim=None,ylim=None,overwrite=False,**kwargs):
    """
    Loglog graph of 1D data file using Matplotlib plt.loglog

    INPUTS:

        filename: string
            name of file containing 1D data to be plotted
        figsize: tuple (width,height)
            size of figure to be displayed
        xlim: np.array
            x-axis limits of graph
        ylim: np.array
            x-axis limits of graph
        decades: int
            number of decades of data below maximum to plot
        overwrite: bool
            add lines to an existing plt.semilogy graph if it exists
            (default is False which will create graph on a new figure)
        **kwargs: dictionary 
            (optional) arguments to be passed onto plt.loglog plot

    OUTPUTS:

        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """

 
    x,y,auxDict = LoadData1D(filename)
    figsize = LogLogSize(figsize)
    if decades is None:
        decades = configs._G['decades']
    if xlim is None:
        xlim = [x[0],x[-1]]
    if ylim is None:
        ylim = [np.min(y),np.max(y)]
  
    ExtendDictionary(auxDict,figsize=figsize,decades=decades,\
            xlim=xlim,ylim=ylim,overwrite=overwrite)
    x,y,auxDict = ProcessData1D(x,y,auxDict)
    figsize = LogLogSize(figsize)
    if overwrite:
        labs = plt.get_figlabels() 
        if "LogLog" not in labs:
          configs.DefaultLS()
        else:
          configs.ToggleLS()
        plt.figure("LogLog",figsize=figsize)
    else:
        configs.DefaultLS()
        plt.figure(figsize=figsize)
  
    fig = plt.loglog(x,y,configs.LS,**kwargs)
    plt.grid(True)
    AuxPlotLabelLL1D(auxDict)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    plt.ion()
    plt.show()
    return fig 



