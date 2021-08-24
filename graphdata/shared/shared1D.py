
import sys
import os
import glob
from graphdata.shared.shared import ProcessDecadeLimits
from graphdata.shared.shared import ProcessComplex
from graphdata.shared.shared import validateFileName
from graphdata.shared.datfile import ReadDatFile1D
from graphdata.shared.jsonfile import ReadJSONFile1D
from graphdata import plt
from graphdata import configs
from graphdata import np
from matplotlib import ticker

        
def LoadData1D(filename):
    """
    Loading of 1D data from a file into numpy arrays

    INPUTS:
        filename: string
            name of file containing 1D data to be loaded
    OUTPUTS:
        x : numpy array 
            x - coordinate (dependent variable) data 
        y : numpy array
            y - coordinate (independent variable) data, possibly of the float or complex type
        auxDict : dictionary
            metadata extracted from the data file (anything not data)
    """

    if not validateFileName(filename):
        raise Exception('Failed to find file: {}'.format(filename))
    filepath,extension = os.path.splitext(filename)
    if extension == '.json':
        return ReadJSONFile1D(filename)
    elif extension == '.dat':
        return ReadDatFile1D(filename)
    else:
        raise Exception('Failed to recognize data format for file extension {}'.format(extension))


def ProcessData1D(x,y,auxDict):
    if 'mirror horizontal' in auxDict:
        x = np.hstack([np.flipud(-x),x])
        y = np.hstack([np.flipud(y),y])
    if(configs.scale() == 'nonDim'):
        x,y = ProcessNonDimData1D(x,y,auxDict)
    elif(configs.scale() == 'dimscale'):
        x,y = ProcessScaledData1D(x,y,auxDict)
    elif(configs.scale() == 'noscale'):
        x,y = ProcessNonScaledData1D(x,y,auxDict)
    return (x,y,auxDict)

def ProcessPointsX(x,y,auxDict): 

  if 'xlim' in auxDict and auxDict['xlim'] is not None:
    xlim = auxDict['xlim']
    indxMax = x < float(xlim[1])
    x = x[indxMax]
    y = y[indxMax]
    indxMin = x >= float(xlim[0]) 
    x = x[indxMin]
    y = y[indxMin]

  nx = len(x)
  if nx == 0:
      raise Exception('No points within specified x-limits')

  indxStep = 1
  if nx > int(configs._G["points1D"]):
    indxStep = int(np.ceil(float(nx)/int(configs._G["points1D"])))
    x = x[0:nx:indxStep]
    y = y[0:nx:indxStep]
  else:
    xvals = np.linspace(x[0],x[-1],int(configs._G["points1D"]))
    y = np.interp(xvals,x,y)
    x = xvals

  if 'xcordID' in auxDict:
    if(auxDict['xcordID'] == 'R'):
      x = np.hstack([-np.flipud(x),x])
      y = np.hstack([np.flipud(y),y])
  return (x,y)

def ProcessPointsY(x,y,auxDict): 
  if 'ylim' in auxDict and auxDict['ylim'] is not None:
    ylim = auxDict['ylim']
    indxMax = y < float(ylim[1])
    x = x[indxMax]
    y = y[indxMax]
    indxMin = y >= float(ylim[0])
    x = x[indxMin]
    y = y[indxMin]

  ny = len(y)
  if ny == 0:
      raise Exception('No points within specified y-limits')

  if 'ycordID' in auxDict:
    if(auxDict['ycordID'] == 'AU'):
      y = y/np.amax(y)
  if 'decades' in auxDict and auxDict['decades'] is not None:
      y = ProcessDecadeLimits(float(auxDict['decades']),y)
    
  return (x,y)

def ProcessNonDimData1D(x,y,auxDict):
  if 'xscale' in auxDict: 
    x = x/(float(auxDict["xscale"]))
  x,y = ProcessPointsX(x,y,auxDict)
  if 'yscale' in auxDict: 
    y = y/(float(auxDict["yscale"]))
  x,y = ProcessPointsY(x,y,auxDict)
  return (x,y)

def ProcessScaledData1D(x,y,auxDict):
  x = x/float(configs._G["xdimscale"]) 
  x,y = ProcessPointsX(x,y,auxDict)
  y = y/float(configs._G["ydimscale"]) 
  x,y = ProcessPointsY(x,y,auxDict)
  return (x,y)

def ProcessNonScaledData1D(x,y,auxDict):
  x,y = ProcessPointsX(x,y,auxDict)
  x,y = ProcessPointsY(x,y,auxDict)
  return (x,y)

def AuxPlotLabel1D(auxDict):
    xstr = ""
    ystr = ""
    xlab = ""
    ylab = ""
    if(configs._G['scale'] == 'nonDim'):
        if 'xscale_str' in auxDict and 'xlabel' in auxDict:
            xstr = str(auxDict['xlabel']) + ' (' + auxDict["xscale_str"] + ')'
        elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
            xstr = str(auxDict['xlabel'])
        if 'yscale_str' in auxDict and 'ylabel' in auxDict:
            ystr = ystr + auxDict['ylabel'] + ' (' + auxDict["yscale_str"] + ')'
        elif 'ylabel' in auxDict:
            ystr = ystr + auxDict['ylabel']
    elif(configs._G['scale'] == 'noscale'):
        if 'xunit_str' in auxDict and 'xlabel' in auxDict:
            xstr = auxDict['xlabel'] + ' (' + auxDict["xunit_str"] + ')'
        elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
            xstr = auxDict['xlabel']
        if 'yunit_str' in auxDict and 'ylabel' in auxDict:
            ystr = str(auxDict['ylabel']) + ' (' + auxDict["yunit_str"] + ')'
        elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
            ystr = auxDict['ylabel']

    elif(configs._G['scale'] == 'dimscale'):
        if 'xunit_str' in auxDict and 'xlabel' in auxDict:
            xstr = str(auxDict['xlabel']) + ' (' + \
                str(configs._G['xdimscale_str']) + str(auxDict["xunit_str"]) + ')'
        elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
            xstr = str(auxDict['xlabel']) + ' (arb.)'
        if 'yunit_str' in auxDict and 'ylabel' in auxDict:
            ystr = str(auxDict['ylabel']) + ' (' + configs._G['ydimscale_str'] + auxDict["yunit_str"] + ')'
        elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
            ystr = ystr + auxDict['ylabel'] + " [arb.]"

    if 'ylim' in auxDict:
        ylim = auxDict['ylim']
        plt.ylim(ylim)

    plt.xlabel(xstr)
    plt.ylabel(ystr)

    if(configs._G['title'] == 'on' and 'title_str' in auxDict):
        titstr = str(auxDict['title_str'])
        plt.title(titstr)

def AuxPlotLabelLL1D(auxDict):
  AuxPlotLabel1D(auxDict)
  ax = plt.gca()
  ax.xaxis.set_major_locator(ticker.LogLocator(numdecs=6))
  ax.yaxis.set_major_locator(ticker.LogLocator(numdecs=4))
  ax.xaxis.grid(b =
      True,which='minor',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.xaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.yaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))



