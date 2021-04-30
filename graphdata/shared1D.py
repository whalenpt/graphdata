
import sys 
from pprint import pprint
from .aux import ProcessAux 
from .aux import SetDecadeLimits
from GraphData3 import pl
from GraphData3 import configs 
from GraphData3 import np 
from matplotlib import ticker 

def ProcessData1D(x,y,auxDict,**kwargs):
  auxDict = ProcessCmdLineOpts(auxDict,**kwargs)
  if 'mirror horizontal' in auxDict:
    x = np.hstack([np.flipud(-x),x])
    y = np.hstack([np.flipud(y),y])
  if(configs.G["scale"] == 'nonDim'):
    x,y = ProcessNonDimData1D(x,y,auxDict)
  elif(configs.G["scale"] == 'dimscale'):
    x,y = ProcessScaledData1D(x,y,auxDict)
  elif(configs.G["scale"] == 'noscale'):
    x,y = ProcessNonScaledData1D(x,y,auxDict)
  return (x,y,auxDict)

def ProcessCmdLineOpts(auxDict,**kwargs):
  if 'lim' in kwargs:
    kwargs['limits'] = kwargs['lim']
  if 'limits' in kwargs:
    limits = kwargs['limits']
    if len(limits) > 1:
      auxDict['xlim'] = limits[0:2]
    if len(limits) > 3:
      auxDict['ylim'] = limits[2:4]
  if 'xlim' in kwargs:
    auxDict['xlim'] = kwargs['xlim']
  if 'ylim' in kwargs:
    auxDict['ylim'] = kwargs['ylim']
  if 'LS' in kwargs:
    auxDict['LS'] = kwargs['LS']
  if 'decades' in kwargs:
    auxDict['decades'] = float(kwargs['decades'])
  return auxDict

def ProcessPointsX(x,y,auxDict): 

  if 'xlim' in auxDict:
    xlim = auxDict['xlim']
    indxMax = x < float(xlim[1])
    x = x[indxMax]
    y = y[indxMax]
    indxMin = x >= float(xlim[0]) 
    x = x[indxMin]
    y = y[indxMin]

  nx = len(x)
  if nx == 0:
    print('No points within specfied x-limits: ') 
    print('EXITING!')
    sys.exit()

  indxStep = 1;
  if nx > int(configs.G["Points1D"]):
    indxStep = int(np.ceil(float(nx)/int(configs.G["Points1D"])))
    x = x[0:nx:indxStep]
    y = y[0:nx:indxStep]
  else: 
    xvals = np.linspace(x[0],x[-1],int(configs.G["Points1D"]))
    y = np.interp(xvals,x,y)
    x = xvals

  if 'xcordID' in auxDict:
    if(auxDict['xcordID'] == 'R'):
      x = np.hstack([-np.flipud(x),x])
      y = np.hstack([np.flipud(y),y])
  return (x,y)

def ProcessPointsY(x,y,auxDict): 
  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    indxMax = y < float(ylim[1])
    x = x[indxMax]
    y = y[indxMax]
    indxMin = y >= float(ylim[0])
    x = x[indxMin]
    y = y[indxMin]

  ny = len(y)
  if ny == 0:
    print('No points within specfied y-limits: ') 
    print('EXITING!')
    sys.exit()

  if 'ycordID' in auxDict:
    if(auxDict['ycordID'] == 'AU'):
      y = y/np.amax(y)
  if 'decades' in auxDict:
    y = SetDecadeLimits(float(auxDict['decades']),y)
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
  x = x/float(configs.G["xdimscale"]) 
  x,y = ProcessPointsX(x,y,auxDict)
  y = y/float(configs.G["ydimscale"]) 
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
  if(configs.G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = str(auxDict['xlabel']) + ' (' + auxDict["xscale_str"] + ')' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = str(auxDict['xlabel'])
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      ystr = ystr + auxDict['ylabel'] + ' (' + auxDict["yscale_str"] + ')' 
    elif 'ylabel' in auxDict:
      ystr = ystr + auxDict['ylabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + ' (' + auxDict["xunit_str"] + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
       xstr = auxDict['xlabel']
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = str(auxDict['ylabel']) + ' (' + auxDict["yunit_str"] + ')' 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] 

  elif(configs.G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = str(auxDict['xlabel']) + ' (' + \
      str(configs.G['xdimscale_str']) + str(auxDict["xunit_str"]) + ')' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = str(auxDict['xlabel']) + ' (arb.)' 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = str(auxDict['ylabel']) + ' (' + configs.G['ydimscale_str'] + auxDict["yunit_str"] + ')' 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = ystr + auxDict['ylabel'] + " [arb.]" 

  if 'ylim' in auxDict:
    ylim = auxDict['ylim']
    pl.ylim(ylim)

  pl.xlabel(xstr)
  pl.ylabel(ystr)

  if(configs.G['title'] == 'on'):
    titstr = ""
    if 'title_str' in auxDict:
      titstr = titstr + str(auxDict['title_str'])
    if 'pval' in auxDict:
      if(configs.G["scale"] == 'nonDim' and 'pscale' in auxDict and 'pscale_str' in auxDict):
        val = float(auxDict["pval"])/float(auxDict['pscale']) 
        titstr = titstr + str("%0.2f" % val) + ' (' + str(auxDict['pscale_str'])  + ')'
      elif(configs.G["scale"] == 'noscale' and 'punit_str' in auxDict):
        val = float(auxDict["pval"])
        titstr = titstr + str("%0.2f" % val) + ' (' + str(auxDict['punit_str']) + ')'
      elif(configs.G["scale"] == 'dimscale' and 'punit_str' in auxDict):
        val = float(auxDict['pval'])/float(configs.G['pdimscale'])
        titstr = titstr + str("%0.2f" % val) + ' (' + \
        str(configs.G['pdimscale_str']) + str(auxDict['punit_str']) + ")"
    pl.title(titstr)

def AuxPlotLabelLL1D(auxDict):
  AuxPlotLabel1D(auxDict)
  ax = pl.gca()
#  ax.xaxis.set_major_locator(ticker.LogLocator(numticks=6))
#  ax.yaxis.set_major_locator(ticker.LogLocator(numticks=6))
  ax.xaxis.set_major_locator(ticker.LogLocator(numdecs=6))
  ax.yaxis.set_major_locator(ticker.LogLocator(numdecs=4))
  ax.xaxis.grid(b =
      True,which='minor',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.xaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  ax.yaxis.grid(b =
      True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))



