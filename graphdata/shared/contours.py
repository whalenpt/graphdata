

from graphdata import configs
from graphdata import np

def ProcessContourLimitZ(zlim,Z):
    zmin = float(zlim[0]) 
    zmax = float(zlim[1])
    Z[Z < zmin] = zmin
    Z[Z > zmax] = zmax
    return Z

def ContourLevels(levels,Z):
    zmin = None
    zmax = None
    if levels is None:
        numCont = int(configs._G['contours'])
        zmin = float(np.amin(Z)) 
        zmax = float(np.amax(Z))
        dz = (zmax - zmin)/(numCont-1)
        levels = np.zeros(numCont,dtype = float)
        for i in range(numCont):
            levels[i] = zmin + i*dz

    if not isinstance(levels,int):
        numCont = len(levels)
    if zmin is not None:
        minTick = zmin
    else:
        minTick = float(np.amin(Z))
    if zmax is not None:
        maxTick = zmax
    else:
        maxTick = float(np.amax(Z))

    levelTicks = list(np.linspace(minTick,maxTick,numCont))
    maxLevTick = 6 
    if len(levelTicks) > maxLevTick:
        indxStep = int(np.ceil(float(len(levelTicks))/maxLevTick))
        lastTick = levelTicks[-1]
        levelTicks = levelTicks[0:-1:indxStep]
        if lastTick not in levelTicks:
            levelTicks.append(lastTick)

    levelTickLabels = [str(np.round(tick,2)) for tick in levelTicks]
    return (levels,levelTicks,levelTickLabels)

def ContourLevelsL(numCont,decades,Z): 
    if numCont < 3:
        numCont = 3
    maxVal = np.amax(Z)
    maxDec = 0.5 + np.log10(maxVal)
    minDec = maxDec - decades - 1 
    levels = list(np.linspace(minDec,maxDec,numCont))
    if maxDec not in levels:
        levels.append(maxDec)

    minTick = int(np.ceil(np.amin(levels)))
    maxTick = int(np.floor(np.amax(levels)))
    dLevel = int((maxTick - minTick+1)/numCont)
    if dLevel < 1:
        dLevel = 1
    levels = [10**x for x in levels]
    tick = list(range(minTick,maxTick+1,dLevel))
    levelTicks = [10**x for x in tick]
    maxLevTick = 8 
    if len(levelTicks) > maxLevTick:
        indxStep = int(np.ceil(float(len(levelTicks))/maxLevTick))
        lastTick = levelTicks[-1]
        levelTicks = levelTicks[0:-1:indxStep]
        if lastTick not in levelTicks:
            levelTicks.append(lastTick)

    levelTickLabels = ['$10^{' + str(x) + '}$' for x in levelTicks]

    return (levels,levelTicks,levelTickLabels)


def AuxContourLabel(CS,auxDict):
  xstr = ""
  ystr = ""
  if(configs._G['scale'] == 'nonDim'):
    if 'xscale_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + '[' + auxDict["xscale_str"] + ']' 
    elif 'xscale_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + '[' + auxDict["yscale_str"] + ']' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] 
  elif(configs._G['scale'] == 'noscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel']  + '[' + auxDict["xunit_str"] + ']' 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + '[' + auxDict["yunit_str"] + ']' 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel']
  elif(configs._G['scale'] == 'dimscale'):
    if 'xunit_str' in auxDict and 'xlabel' in auxDict:
      xstr = auxDict['xlabel'] + "[" + configs._G['xdimscale_str'] + auxDict["xunit_str"] + "]" 
    elif 'xunit_str' not in auxDict and 'xlabel' in auxDict:
      xstr = ystr + auxDict['xlabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + "[" + configs._G['ydimscale_str'] + auxDict["yunit_str"] + "]" 
    elif 'yunit_str' not in auxDict and 'ylabel' in auxDict:
      ystr = auxDict['ylabel'] + " [arb.]" 
  CS.ax.set_xlabel(xstr)
  CS.ax.set_ylabel(ystr)



