
import sys
from pprint import pprint
from .aux import ProcessAux 
from .aux import SetDecadeLimits
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 

def ProcessData2D(x,y,z,auxDict,**kwargs):
  auxDict = ProcessCmdLineOpts(auxDict,**kwargs)
  if 'swapxy' in auxDict:
    ty = y
    y = x
    x = ty
    z = np.transpose(z)
  if(configs.G["scale"] == 'nonDim'):
    x,y,z = ProcessNonDimData2D(x,y,z,auxDict)
  elif(configs.G["scale"] == 'dimscale'):
    x,y,z = ProcessScaledData2D(x,y,z,auxDict)
  elif(configs.G["scale"] == 'noscale'):
    x,y,z = ProcessNonScaledData2D(x,y,z,auxDict)
  z = np.transpose(z)
  return (x,y,z,auxDict)

def ProcessCmdLineOpts(auxDict,**kwargs):
  if 'lim' in kwargs:
    kwargs['limits'] = kwargs['lim']
  if 'limits' in kwargs:
    limits = kwargs['limits']
    if len(limits) > 1:
      auxDict['xlim'] = limits[0:2]
    if len(limits) > 3:
      auxDict['ylim'] = limits[2:4]
    if len(limits) > 5:
      auxDict['zlim'] = limits[4:6]
  if 'xlim' in kwargs:
    auxDict['xlim'] = kwargs['xlim']
  if 'ylim' in kwargs:
    auxDict['ylim'] = kwargs['ylim']
  if 'zlim' in kwargs:
    auxDict['zlim'] = kwargs['zlim']
  if 'LS' in kwargs:
    auxDict['LS'] = kwargs['LS']
  if 'decades' in kwargs:
    auxDict['decades'] = float(kwargs['decades'])
  return auxDict

def ProcessPointsXY(x,y,z,auxDict): 

  if 'xlim' in auxDict:
    xlim = auxDict['xlim']
    indxMax = x < float(xlim[1])
    x = x[indxMax]
    z = z[indxMax,:]
    indxMin = x >= float(xlim[0]) 
    x = x[indxMin]
    z = z[indxMin,:]

  nx = len(x)
  if nx == 0:
    print('No points within specfied x-limits: ') 
    print('EXITING!')
    sys.exit()

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    indxMax = y < float(ylim[1])
    y = y[indxMax]
    z = z[:,indxMax]
    indxMin = y >= float(ylim[0]) 
    y = y[indxMin]
    z = z[:,indxMin]

  ny = len(y)
  if ny == 0:
    print('No points within specfied x-limits: ') 
    print('EXITING!')
    sys.exit()

  indxStep = 1;
  if nx > int(configs.G["PointsX_2D"]):
    indxStep = int(np.ceil(float(nx)/int(configs.G["PointsX_2D"])))
  x = x[0:nx:indxStep]
  z = z[0:nx:indxStep,:]

  indxStep = 1;
  if ny > int(configs.G["PointsY_2D"]):
    indxStep = int(np.ceil(float(ny)/int(configs.G["PointsY_2D"])))
  y = y[0:ny:indxStep];
  z = z[:,0:ny:indxStep]

  if 'ycordID' in auxDict:
    if(auxDict['ycordID'] == 'R' or auxDict['ycordID'] == 'SR'):
      y = np.hstack([-np.flipud(y),y])
      z = np.hstack([np.fliplr(z),z])
  return (x,y,z)

def ProcessPointsZ(x,y,z,auxDict): 
  if 'zcordID' in auxDict:
    if(auxDict['zcordID'] == 'AU'):
      z = z/np.amax(z)
  if 'decades' in auxDict:
    z = SetDecadeLimits(auxDict['decades'],z)

  #if 'zmin' in auxDict:
  #  indxMin = z >= float(auxDict['zmin']) 
  #  z[indxMin] = float(auxDict['zmin'])
  #if 'zmax' in auxDict:
  #  indxMax = z < float(auxDict['zmax']) 
  #  z[indxMax] = float(auxDict['zmax'])
  return (x,y,z)


def ProcessNonDimData2D(x,y,z,auxDict):
  if 'xscale' in auxDict:
    x = x/(float(auxDict["xscale"]))
  if 'yscale' in auxDict:
    y = y/(float(auxDict["yscale"]))
  if 'zscale' in auxDict: 
    z = z/(float(auxDict["zscale"]))

  x,y,z = ProcessPointsXY(x,y,z,auxDict)
  x,y,z = ProcessPointsZ(x,y,z,auxDict)
  return (x,y,z)

def ProcessScaledData2D(x,y,z,auxDict):

  x = x/float(configs.G["xdimscale"]) 
  y = y/float(configs.G["ydimscale"]) 
  z = z/float(configs.G["zdimscale"]) 

  x,y,z = ProcessPointsXY(x,y,z,auxDict)
  x,y,z = ProcessPointsZ(x,y,z,auxDict)
  return (x,y,z)


def ProcessNonScaledData2D(x,y,z,auxDict):
  x,y,z = ProcessPointsXY(x,y,z,auxDict)
  x,y,z = ProcessPointsZ(x,y,z,auxDict)
  return (x,y,z)

def AuxContourLabel(CS,auxDict):
  xstr = ""
  ystr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '[' + auxDict["xscale_str"] + ']' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + '[' + auxDict["yscale_str"] + ']' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel']  + '[' + auxDict["xunit_str"] + ']' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + '[' + auxDict["yunit_str"] + ']' 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel']
  elif(configs.G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + "[" + configs.G['xdimscale_str'] + auxDict["xunit_str"] + "]" 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = ystr + auxDict['xlabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + "[" + configs.G['ydimscale_str'] + auxDict["yunit_str"] + "]" 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + " [arb.]" 
  CS.ax.set_xlabel(xstr)
  CS.ax.set_ylabel(ystr)





