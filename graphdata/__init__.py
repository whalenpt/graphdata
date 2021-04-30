"""Top-level package for GraphData"""
__author__ = """Patrick Whalen"""
__email__ = 'whalenpt@gmail.com'
__version__ = '0.0.1'

from matplotlib import rc,rcParams 
import matplotlib as mpl
import matplotlib.pylab as pl 
import numpy as np

global configs
from .Settings.settings import PlotSettings
configs = PlotSettings()
from pprint import pprint
pprint(configs.G)

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
pl.register_cmap(cmap = newbonemap)
mpl.colors.colorConverter.colors['f'] = (0.0/256,0.0/256,205.0/256)
mpl.colors.colorConverter.colors['t'] = (105.0/256,105.0/256,105.0/256)

cdict = {'blue': ((0.0, 0.0, 0.0), (0.74, 0.0, 0.0), (1.0, 0.7, 0.7)),
 'green': ((0.0, 0.0, 0.0), (0.365079, 0.0, 0.0), (0.746032, 1.0, 1.0), (1.0, 1.0, 1.0)), 
 'red': ((0.0, 0.0416, 0.0416), (0.365079, 1.0, 1.0), (1.0, 1.0, 1.0))}

newhotmap = mpl.colors.LinearSegmentedColormap('hot',cdict)
pl.register_cmap(cmap = newhotmap)


from .plot1D import Plot 
from .plot1D import PlotH
from .plot1D import PlotL 
from .plot1D import PlotHL
from .plot1D import PlotLH
from .plot1D import PlotF
from .plot1D import PlotLF
from .plot1D import PlotHF
from .plot1D import PlotHLF
from .plot1D import LogLogF 
from .plot1D import LogLogHF
from .mov1D import PlotM
from .mov1D import PlotLM
from .aux import LoadData1D
from .aux import LoadData2D
from .aux import LoadComplexData1D
from .aux import GenFileList
from .evolve1D import Evolve
from .evolve1D import EvolveL
from .evolve1D import EvolveC
from .evolve1D import EvolveI
from .evolve1D import EvolveS
from .evolve1D import EvolveM
from .evolve1D import EvolveLS
from .evolve1D import EvolveB
from .evolve1D import EvolveLB
from .evolve1D import EvolveR
from .contour2D import ContourF
from .contour2D import ContourHF
from .contour2D import ContourLF
from .contour2D import ContourHLF
from .movContour2D import ContourFM
from .movContour2D import ContourLFM
from .surface import Surface
from .surface import SurfaceH
from .surface import Wire 
from .surface import WireH
from .movSurface import SurfaceM
from .movSurface import WireM
from .converg import Converge
from .converg import Speed
from .converg import SpeedH
from .converg import ConvergeH
from .converg import ConvergeHRS
from .converg import ConvergeO
from .converg import Converge2DH
from .converg import TableP
from .converg import TableS
from .converg import TablePS
from .optic import FreqToWave1D
from .optic import FreqToWaveF1D
from .optic import FreqToWave2D
from .optic import FreqToWaveF2D
from .optic import WaveToFreq1D
from .optic import WaveToFreqF1D
from .optic import SwapIndx1D
from .maxplot import Max
from .maxplot import MaxH
from .maxplot import MaxEvolveS
from .maxplot import MaxMaxEvolveS


