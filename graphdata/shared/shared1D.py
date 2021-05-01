
import sys
from graphdata.shared.shared import SetDecadeLimits
from graphdata import plt
from graphdata import configs
from graphdata import np
from matplotlib import ticker

def LoadData1D(fileName):
  fileList = glob.glob(fileName)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()
  auxDict = ProcessAux(fileName) 
  with open(fileName,'rb') as f:
    data = np.genfromtxt(f,skip_header=len(auxDict))
    x = data[:,0]; y = data[:,1];
  return (x,y,auxDict)

def LoadComplexData1D(fileName):
  fileList = glob.glob(fileName)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()
  auxDict = ProcessAux(fileName) 
  with open(fileName) as f:
    data = np.genfromtxt(f,skip_header=len(auxDict))
    x = data[:,0]; yr = data[:,1]; yi = data[:,2];
  return (x,yr,yi,auxDict)

def GetData1D(*arg):
  if len(arg) < 2:
    print("GetData1D requires at least two arguments: the fileID and file# ") 
    return False
  fileID = arg[0]
  num = arg[1]
  fileID = str(fileID)
  fileName = fileID + '_' + str(num) + '.dat'
  print(fileName)
  x,y,auxDict = LoadData1D(fileName)
  return (x,y,auxDict)

def GetFileData1D(*arg):
  if len(arg) < 1:
    print("GetFileData1D requires at least one arguments: the file name ") 
    return False
  fileName = str(arg[0])
  print(fileName)
  x,y,auxDict = LoadData1D(fileName)
  return (x,y,auxDict)

def ProcessData1D(x,y,auxDict,**kwargs):
  auxDict = ProcessCmdLineOpts(auxDict,**kwargs)
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

  indxStep = 1
  if nx > int(configs._G["Points1D"]):
    indxStep = int(np.ceil(float(nx)/int(configs._G["Points1D"])))
    x = x[0:nx:indxStep]
    y = y[0:nx:indxStep]
  else: 
    xvals = np.linspace(x[0],x[-1],int(configs._G["Points1D"]))
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

  if(configs._G['title'] == 'on'):
    titstr = ""
    if 'title_str' in auxDict:
      titstr = titstr + str(auxDict['title_str'])
    if 'pval' in auxDict:
      if(configs._G["scale"] == 'nonDim' and 'pscale' in auxDict and 'pscale_str' in auxDict):
        val = float(auxDict["pval"])/float(auxDict['pscale']) 
        titstr = titstr + str("%0.2f" % val) + ' (' + str(auxDict['pscale_str'])  + ')'
      elif(configs._G["scale"] == 'noscale' and 'punit_str' in auxDict):
        val = float(auxDict["pval"])
        titstr = titstr + str("%0.2f" % val) + ' (' + str(auxDict['punit_str']) + ')'
      elif(configs._G["scale"] == 'dimscale' and 'punit_str' in auxDict):
        val = float(auxDict['pval'])/float(configs._G['pdimscale'])
        titstr = titstr + str("%0.2f" % val) + ' (' + \
        str(configs._G['pdimscale_str']) + str(auxDict['punit_str']) + ")"
    plt.title(titstr)

def AuxPlotLabelLL1D(auxDict):
  AuxPlotLabel1D(auxDict)
  ax = plt.gca()
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



