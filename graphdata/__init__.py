"""Top-level package for GraphData"""
__author__ = """Patrick Whalen"""
__email__ = 'whalenpt@gmail.com'
__version__ = '0.0.1'

from matplotlib import rc,rcParams
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

global configs
from graphdata.settings.settings import PlotSettings
configs = PlotSettings()

#rc('text',usetex=True)
rc('text',usetex=False)
rcParams['contour.negative_linestyle'] = 'solid' 
rcParams['image.cmap'] = 'hot'
rcParams['lines.antialiased'] = True
#rcParams['legend.frameon'] = True 
rcParams['figure.facecolor'] = 'white'   
newbonemap = mpl.colors.LinearSegmentedColormap.from_list('bone',
   [(0.81234674617027558, 0.87990196078431371, 0.87990193376227044),
       (0.4392156862745098, 0.48412986868103691, 0.56421558822309559),
  (0.12009803921568628, 0.12009799222075436, 0.16709292412617219) ])
plt.register_cmap(cmap = newbonemap)
mpl.colors.colorConverter.colors['f'] = (0.0/256,0.0/256,205.0/256)
mpl.colors.colorConverter.colors['t'] = (105.0/256,105.0/256,105.0/256)

cdict = {'blue': ((0.0, 0.0, 0.0), (0.74, 0.0, 0.0), (1.0, 0.7, 0.7)),
 'green': ((0.0, 0.0, 0.0), (0.365079, 0.0, 0.0), (0.746032, 1.0, 1.0), (1.0, 1.0, 1.0)), 
 'red': ((0.0, 0.0416, 0.0416), (0.365079, 1.0, 1.0), (1.0, 1.0, 1.0))}

newhotmap = mpl.colors.LinearSegmentedColormap('hot',cdict)
plt.register_cmap(cmap = newhotmap)


from graphdata.plot import plot 
from graphdata.semilogy import semilogy
from graphdata.loglog import loglog
from graphdata import idnum
from graphdata.surface import surface
from graphdata.contourf import contourf
from graphdata.contourf import contourflog
from graphdata.shared.shared1D import LoadData1D
from graphdata.shared.shared2D import LoadData2D
from graphdata.shared.shared import LoadMetadata
#from graphdata.shared.shared import GenFileList

#from graphdata.movie.plot import plotMovie
#from graphdata.movie.plot import semilogyMovie

#from graphdata.wireframe import wireframe
#from graphdata.waterfall import waterfall
#from graphdata.waterfall import waterfallLog
#from graphdata.contour import contourfLog
#from graphdata.movie.contour import contourfMovie
#from graphdata.movie.contour import contourfLogMovie
#from graphdata.wireframe import wireframe
#from graphdata.movie.surface import surfaceMovie
#from graphdata.movie.wireframe import wireframeMovie



