
import graphdata.plot
import graphdata.semilogy
import graphdata.loglog
from graphdata.shared.idnum import GetDataFileName


def plot(fileID,fileNumber,figsize=None,xlim=None,ylim=None,\
        complex_op=None,overwrite=False,**kwargs):
    """
    Graph of 1D data file using Matplotlib plt.plot with fileID and fileNumber format
    INPUTS:
        fileID: string
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (extension is a catchall, doesnt have to be dat)
        fileNumber: int
            Specifies which data file number to plot 
            e.g.  plot('T',10) will make a plot of the data file 'T_10.dat' if this
            data file is available
        (see graphdata.plot.plot for info on other arguments)

    OUTPUTS:
        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """
    filename = GetDataFileName(fileID,fileNumber)
    return graphdata.plot(filename,figsize=figsize,xlim=xlim,ylim=ylim,\
            overwrite=overwrite,complex_op=complex_op,**kwargs)

def semilogy(fileID,fileNumber,figsize=None,decades=None,xlim=None,ylim=None,\
        overwrite=False,complex_op=None,**kwargs):
    """
    Log graph of 1D data file (log in y-axis) using Matplotlib plt.semilogy 
    with fileID and fileNumber format
    INPUTS:
        fileID: string
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (or .txt or some other extension)
        fileNumber: int
            Specifies which data file number to plot 
            e.g.  plot('T',10) will make a plot of the data file 'T_10.dat' if this
            data file is available
        (see graphdata.semilogy.semilogy for info on other arguments)

    OUTPUTS:
        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """
    filename = GetDataFileName(fileID,fileNumber)
    return graphdata.semilogy(filename,figsize=figsize,decades=decades,\
            xlim=xlim,ylim=ylim,overwrite=overwrite,complex_op=complex_op,**kwargs)


def loglog(fileID,fileNumber,figsize=None,decades=None,xlim=None,ylim=None,\
        overwrite=False,complex_op=None,**kwargs):
    """
    Log graph of 1D data file (log in both x-axis and y-axis) using Matplotlib plt.semilogy 
    with fileID and fileNumber format
    INPUTS:
        fileID: string
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (or .txt or some other extension)
        fileNumber: int
            Specifies which data file number to plot 
            e.g.  plot('T',10) will make a plot of the data file 'T_10.dat' if this
            data file is available
        (see graphdata.semilogy.semilogy for info on other arguments)

    OUTPUTS:
        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """
    filename = GetDataFileName(fileID,fileNumber)
    return graphdata.loglog(filename,figsize=figsize,decades=decades,\
            xlim=xlim,ylim=ylim,overwrite=overwrite,complex_op=complex_op,**kwargs)




