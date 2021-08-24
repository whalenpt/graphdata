
import sys
import glob
import os
from matplotlib import ticker

from graphdata.shared.shared import validateFileName
from graphdata.shared.shared import LabelX
from graphdata.shared.shared import LabelY
from graphdata.shared.shared import LabelZ
from graphdata.shared.datfile import ReadDatFile2D
from graphdata.shared.jsonfile import ReadJSONFile2D

from graphdata import plt
from graphdata import configs
from graphdata import np

def LoadData2D(fileName):
    if not validateFileName(fileName):
        raise Exception('Failed to find file: {}'.format(fileName))
    filepath,extension = os.path.splitext(fileName)
    if extension == '.json':
        return ReadJSONFile2D(fileName)
    elif extension == '.dat':
        return ReadDatFile2D(fileName)
    else:
        raise Exception('Failed to recognize data format for file extension {}'.format(extension))

def ProcessData2D(x,y,z,auxDict):
    if 'swapxy' in auxDict:
        tempy = y
        y = x
        x = tempy
        z = np.transpose(z)
    x,y,z = ProcessNonScaledData2D(x,y,z,auxDict)
    z = np.transpose(z)
    return (x,y,z,auxDict)


def ProcessPointsXYZ(x,y,z,auxDict): 
    if 'xlim' in auxDict and auxDict['xlim'] is not None:
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

    if 'ylim' in auxDict and auxDict['ylim'] is not None:
        ylim = auxDict['ylim']
        indxMax = y < float(ylim[1])
        y = y[indxMax]
        z = z[:,indxMax]
        indxMin = y >= float(ylim[0]) 
        y = y[indxMin]
        z = z[:,indxMin]
  
    ny = len(y)
    if ny == 0:
        print('No points within specfied y-limits: ') 
        print('EXITING!')
        sys.exit()

    indxStep = 1;
    if nx > int(configs._G["pointsX_2D"]):
        indxStep = int(np.ceil(float(nx)/int(configs._G["pointsX_2D"])))
    x = x[0:nx:indxStep]
    z = z[0:nx:indxStep,:]
  
    indxStep = 1;
    if ny > int(configs._G["pointsY_2D"]):
        indxStep = int(np.ceil(float(ny)/int(configs._G["pointsY_2D"])))
    y = y[0:ny:indxStep];
    z = z[:,0:ny:indxStep]

    if 'ycordID' in auxDict:
        if(auxDict['ycordID'] == 'R' or auxDict['ycordID'] == 'SR'):
            y = np.hstack([-np.flipud(y),y])
            z = np.hstack([np.fliplr(z),z])
  
    if 'decades' in auxDict and auxDict['decades'] is not None:
        z = ProcessDecadeLimits(float(auxDict['decades']),z)

    return (x,y,z)


def GetView(**kwargs):
    if 'elev' in kwargs:
        elev = int(kwargs['elev'])
    else:
        elev = int(configs._G['elev'])
    if 'azim' in kwargs:
        azim = int(kwargs['azim'])
    else:
        azim = int(configs._G['azim'])
    return elev,azim


def Labels2D(auxDict):
    xstr = LabelX(auxDict)
    ystr = LabelY(auxDict)
    zstr = LabelZ(auxDict)
    return (xstr,ystr,zstr)


def GetData2D(*arg):
  if len(arg) < 2:
    print("GetData2D requires at least two arguments: the fileID and file# ")
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  x,y,z,auxDict = LoadData2D(fileName)
  if len(arg) > 2:
    auxDict = SetLimits2D(arg[2],auxDict)
  return (x,y,z,auxDict)

def SetLimits2D(glist,auxDict):
  if len(glist) > 0:
    xmin = glist[0] 
    auxDict['xmin'] = xmin
  if len(glist) > 1:
    xmax = glist[1] 
    auxDict['xmax'] = xmax
  if len(glist) > 2:
    ymin = glist[2] 
    auxDict['ymin'] = ymin
  if len(glist) > 3:
    ymax = glist[3] 
    auxDict['ymax'] = ymax
  if len(glist) > 4:
    zmin = glist[4] 
    auxDict['zmin'] = zmin
  if len(glist) > 5:
    zmax = glist[5] 
    auxDict['zmax'] = zmax
  return auxDict

def GetDataLog2D(*arg):
  if len(arg) < 2:
    print("GetData2D requires at least two arguments: the fileID and file# ") 
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  print(fileName)
  x,y,z,auxDict = LoadData2D(fileName)
  if len(arg) > 2:
    auxDict = SetLimits2D(arg[2],auxDict)

  return (x,y,z,auxDict)


#def ProcessPointsZ(x,y,z,auxDict): 
#    if 'zcordID' in auxDict:
#        if(auxDict['zcordID'] == 'AU'):
#            z = z/np.amax(z)
#    if 'decades' in auxDict:
#        z = SetDecadeLimits(auxDict['decades'],z)

  #if 'zmin' in auxDict:
  #  indxMin = z >= float(auxDict['zmin']) 
  #  z[indxMin] = float(auxDict['zmin'])
  #if 'zmax' in auxDict:
  #  indxMax = z < float(auxDict['zmax']) 
  #  z[indxMax] = float(auxDict['zmax'])

#  return (x,y,z)


def ProcessNonDimData2D(x,y,z,auxDict):
  if 'xscale' in auxDict:
    x = x/(float(auxDict["xscale"]))
  if 'yscale' in auxDict:
    y = y/(float(auxDict["yscale"]))
  if 'zscale' in auxDict: 
    z = z/(float(auxDict["zscale"]))
  return ProcessPointsXYZ(x,y,z,auxDict)

def ProcessScaledData2D(x,y,z,auxDict):

  x = x/float(configs._G["xdimscale"]) 
  y = y/float(configs._G["ydimscale"]) 
  z = z/float(configs._G["zdimscale"]) 
  return ProcessPointsXYZ(x,y,z,auxDict)


def ProcessNonScaledData2D(x,y,z,auxDict):
  return ProcessPointsXYZ(x,y,z,auxDict)


def AuxAxes3DLabel(ax,auxDict):
  xstr = ""
  ystr = ""
  zstr = ""
  if(configs._G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + auxDict["xscale_str"] + ')' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs._G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
       xstr = auxDict['xlabel']
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs._G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '(' + configs._G['xdimscale_str'] + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + " [arb.]" 
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + configs._G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = ystr + auxDict['plabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + '(' + configs._G['ydimscale_str'] + auxDict["yunit_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + " [arb.]" 

  if 'zlim' in auxDict:
    ax.set_zlim3d(auxDict['zlim'])

  print(auxDict)

  ax.set_xlabel(xstr)
  ax.set_ylabel(ystr)
  ax.set_zlabel(zstr)

  if 'elev' in auxDict and 'azim' in auxDict:
    ax.view_init(auxDict['elev'],auxDict['azim'])

  numTicks = int(configs._G['NumberSurfaceTicks'])
  ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.zaxis.set_major_locator(ticker.LinearLocator(4))
  
  labelType = str(configs._G['SurfaceTickFormat'])
  ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))








