"""Top-level package for GraphData"""
__author__ = """Patrick Whalen"""
__email__ = 'whalenpt@gmail.com'
__version__ = '0.0.1'

from matplotlib import rc,rcParams
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

global configs
from .settings.settings import PlotSettings
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


from .plot import Plot 
from .plot import PlotH
from .plot import PlotL 
from .plot import PlotHL
from .plot import PlotLH
from .plot import PlotF
from .plot import PlotLF
from .plot import PlotHF
from .plot import PlotHLF
from .plot import LogLogF 
from .plot import LogLogHF
from .movie.mov1D import PlotM
from .movie.mov1D import PlotLM
from .helper import LoadData1D
from .helper import LoadData2D
from .helper import LoadComplexData1D
from .helper import GenFileList
from .evolve import Evolve
from .evolve import EvolveL
from .evolve import EvolveC
from .evolve import EvolveI
from .evolve import EvolveS
from .evolve import EvolveM
from .evolve import EvolveLS
from .evolve import EvolveB
from .evolve import EvolveLB
from .evolve import EvolveR
from .contour import ContourF
from .contour import ContourHF
from .contour import ContourLF
from .contour import ContourHLF
from .movie.contour import ContourFM
from .movie.contour import ContourLFM
from .surface import Surface
from .surface import SurfaceH
from .surface import Wire
from .surface import WireH
from .movie.surface import SurfaceM
from .movie.surface import WireM
from .maxplot import Max
from .maxplot import MaxH
from .maxplot import MaxEvolveS
from .maxplot import MaxMaxEvolveS


