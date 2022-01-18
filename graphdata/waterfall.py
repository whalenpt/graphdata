#!/usr/bin/python
# Filename: waterfall.py

from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 
from matplotlib.colors import LightSource

from graphdata.shared.idnum import GetDataFileList
from graphdata.shared.shared import ProcessComplex
from graphdata.shared.shared import ExtendDictionary
from graphdata.shared.shared1D import LoadData1D
from graphdata.shared.shared1D import ProcessData1D
from graphdata.shared.shared2D import GetView
from graphdata.shared.figsizes import WaterfallSize

from graphdata import plt
from graphdata import configs 
from graphdata import np 

def waterfall(fileID : str, fileNumbers : list,figsize=None,xlim=None,ylim=None,\
        complex_op=None,zvalstr=None,aspect=None,**kwargs):
    """
    INPUTS:
        fileID: str
            ID for data files where files look like fileID_fileNum.dat e.g.
            if data files for T data are T_0.dat,T_1.dat, T_2.dat,..., then the
            fileID is simply 'T' (extension is a catchall, doesnt have to be dat)
        fileNumbers: list[int]
            Specifies which data file numbers to plot 
            e.g.  waterfall('T',[0:2:100]) will plot files T_0.dat,T_2.dat,...,T_100.dat
        (see graphdata.plot.plot for info on other arguments)

        xlim: np.array
            x-axis limits of graph
        zlim: np.array
            z-axis limits of graph
        complex_op : string in the following list ('real','imag','power','absolute','angle')
            complex operation used to plot complex data
        zvalstr: str
            looks for metadata labeled zvalstr in the files, and will use these to plot z-axis with units
        aspect: tuple
            aspect ratio to use for xyz graph, e.g. (1,1,1) corresponds to a box
        **kwargs: dictionary
            (optional) arguments to be passed onto plt.plot plots

    OUTPUTS:
        ax : matplotlib.axes.Axes 
            Matplotlib axes object, allows for setting limits and other manipulation of the axes
            (e.g. ax.set_xlim([0,1]) would set the graph x-limits to be between 0 and 1)

    """

    fileList = GetDataFileList(fileID,fileNumbers)
    fileLen = len(fileList)
    count = 0
    auxDict = dict() 
    x1 = [0]*len(fileList)
    figsize = WaterfallSize(figsize)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection='3d')

    ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
    count = 0
    normFact = 1.0
    for i,filename in enumerate(fileList):
        x,y,auxDict = LoadData1D(filename)
        if complex_op is not None:
            y = ProcessComplex(complex_op,y)
        ExtendDictionary(auxDict,figsize=figsize,xlim=xlim,\
                ylim=ylim,complex_op=complex_op)
        x,y,auxDict = ProcessData1D(x,y,auxDict)
        if zvalstr is not None and zvalstr in auxDict:
            x1[i] = float(auxDict[zvalstr])
        else:
            x1[i] = i
        ax.plot(x,x1[i]*np.ones_like(x),y,color = 'black',**kwargs)

    if xlim is None:
        xlim = [x[0],x[-1]]
    plt.xlim(xlim)

    if ylim is not None:
        ax.set_zlim3d(ylim)

    zmin = np.amin(x1)
    zmax = np.amax(x1)
    plt.ylim([zmin,zmax])

    if 'xlabel' in auxDict:
        ax.set_xlabel(auxDict['xlabel'])
    else:
        ax.set_xlabel('x')

    if 'ylabel' in auxDict:
        ax.set_zlabel(auxDict['ylabel'])
    else:
        ax.set_zlabel('y')

    if zvalstr is not None:
        ax.set_ylabel(zvalstr)
    else:
        ax.set_ylabel('file')

    elev,azim = GetView(**kwargs)
    ax.view_init(elev,azim)
    if aspect is not None:
        ax.set_box_aspect(aspect = aspect)
    plt.ion()
    plt.show()
    plt.tight_layout()
    return ax

