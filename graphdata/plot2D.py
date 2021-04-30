

#from shared2D import AuxPlotLabel1D 
#from shared2D import ProcessData2D 
#from shared2D import LoadFileData2D 
#from aux import GenFileList
#from aux import GetPlotFiles 
#from aux import ProcessAux 
#from aux import SortNumericStringList
#
##from matplotlib import ticker 
##from matplotlib import rc,rcParams 
##import numpy as np
##import matplotlib.pylab as pl 
##from mpl_toolkits.mplot3d.axes3d import Axes3D 
##from matplotlib import cm 
##import glob
##import os 
##import string
##import subprocess
##from pprint import pprint
##
##from aux import SortNumericStringList
##from aux import GetMovieCommand
##from aux import fmtcols
##from aux import GetPlotFile 
##from aux import ProcessAux
##
##rc('text',usetex=True)
##rc('font',**{'family':'serif','serif':['Computer Modern']})
##plt.rcParams['lines.markersize'] = 2
##plt.rcParams['axes.labelsize'] = 'large' 
##plt.rcParams['font.weight'] = 'bold' 
##plt.rcParams['font.size'] = 16 
#
##def ProcessData2D(x,y,z,auxDict):
##
##  if 'swapxy' in auxDict:
##    ty = y
##    y = x
##    x = ty
##    z = np.transpose(z)
##
##  xmin = 0.0
##  xmax = 0.0
##  if(auxDict['xcordID'] == 'T'):
##    xmin = float(configs.G["minT"])
##    xmax = float(configs.G["maxT"])
##  elif(auxDict['xcordID'] == 'ST'):
##    xmin = float(configs.G["minST"])
##    xmax = float(configs.G["maxST"])
##  elif(auxDict['xcordID'] == 'Z'):
##    xmin = float(configs.G["minZ"])
##    xmax = float(configs.G["maxZ"])
##  elif(auxDict['xcordID'] == 'X'):
##    xmin = float(configs.G["minX"])
##    xmax = float(configs.G["maxX"])
##
##  ymin = 0.0
##  ymax = 0.0
##  if(auxDict['ycordID'] == 'R'):
##    ymin = float(configs.G["minR"])
##    ymax = float(configs.G["maxR"])
##  elif(auxDict['ycordID'] == 'ST'):
##    ymin = float(configs.G["minST"])
##    ymax = float(configs.G["maxST"])
##  elif(auxDict['ycordID'] == 'SR'):
##    ymin = float(configs.G["minSR"])
##    ymax = float(configs.G["maxSR"])
##  elif(auxDict['ycordID'] == 'Z'):
##    ymin = float(configs.G["minZ"])
##    ymax = float(configs.G["maxZ"])
##  elif(auxDict['ycordID'] == 'Y'):
##    ymin = float(configs.G["minY"])
##    ymax = float(configs.G["maxY"])
##
##  zmin = 0.0
##  zmax = 0.0
##  if(auxDict['zcordID'] == 'I'):
##    zmin = 0.0
##    zmax = float(configs.G["maxI"])
##  elif(auxDict['zcordID'] == 'E'):
##    zmin = -np.sqrt(float((configs.G["maxI"])))
##    zmax = np.sqrt(float((configs.G["maxI"])))
##  elif(auxDict['zcordID'] == 'AU'):
##    zmin = np.amin(z)
##    zmax = np.amax(z)
##
##  if 'xscale' in auxDict:
##    indxMax = x/(float(auxDict["xscale"])) < xmax 
##    x = x[indxMax]
##    z = z[indxMax,:]
##    indxMin = x/(float(auxDict["xscale"])) >= xmin 
##    x = x[indxMin]
##    z = z[indxMin,:]
##
##  if 'yscale' in auxDict:
##    indxMax = y/(float(auxDict["yscale"])) < ymax 
##    y = y[indxMax]
##    z = z[:,indxMax]
##    indxMin = y/(float(auxDict["yscale"])) >= ymin 
##    y = y[indxMin]
##    z = z[:,indxMin]
##
##  nx = len(x)
##  indxStep = 1;
##  if(auxDict['xcordID'] == 'T'):
##    if nx > int(configs.G["Nt_2D"]):
##      indxStep = int(np.ceil(float(nx)/int(configs.G["Nt_2D"])))
##  elif(auxDict['xcordID'] == 'X'):
##    if nx > int(configs.G["Nx_2D"]):
##      indxStep = int(np.ceil(float(nx)/int(configs.G["Nx_2D"])))
##  elif(auxDict['xcordID'] == 'SR'):
##    if nx > int(configs.G["Nsr_2D"]):
##      indxStep = int(np.ceil(float(nx)/int(configs.G["Nsr_2D"])))
##  elif(auxDict['xcordID'] == 'SX'):
##    if nx > int(configs.G["Nsx_2D"]):
##      indxStep = int(np.ceil(float(nx)/int(configs.G["Nsx_2D"])))
##
##  x = x[0:nx:indxStep]
##  z = z[0:nx:indxStep,:]
##
##  ny = len(y)
##  indxStep = 1;
##  if(auxDict['ycordID'] == 'R'):
##    if ny > int(0.5*int(configs.G["Nr_2D"])):
##      indxStep = int(np.ceil(float(ny)/int(configs.G["Nr_2D"])))
##  elif(auxDict['ycordID'] == 'Y'):
##    if ny > int(configs.G["Ny_2D"]):
##      indxStep = int(np.ceil(float(ny)/int(configs.G["Ny_2D"])))
##  elif(auxDict['ycordID'] == 'ST'):
##    if ny > int(configs.G["Nconfigs_2D"]):
##      indxStep = int(np.ceil(float(ny)/int(configs.G["Nconfigs_2D"])))
##  elif(auxDict['ycordID'] == 'SY'):
##    if ny > int(configs.G["Nsy_2D"]):
##      indxStep = int(np.ceil(float(ny)/int(configs.G["Nsy_2D"])))
##
##  y = y[0:ny:indxStep];
##  z = z[:,0:ny:indxStep]
##
##  if(auxDict['ycordID'] == 'R' or auxDict['ycordID'] == 'SR'):
##    ny = 2*ny
##    y = np.hstack([-np.flipud(y),y])
##    z = np.hstack([np.fliplr(z),z])
##
##  if(auxDict['logz'] == 'logz'):
##    Imax = np.max(z)
##    mxI = float(configs.G["maxI"])
##    if(auxDict['zcordID'] == 'AU'):
##      z = mxI*z/Imax
##      indxNew = z < pow(10,float(configs.G["minDec"]))*mxI
##      z[indxNew] = pow(10,float(configs.G["minDec"]))*mxI
##    else:
##      indxNew = z < mxI*pow(10,float(configs.G["minDec"]))
##      z[indxNew] = pow(10,float(configs.G["minDec"]))*mxI
##
##
##  z = np.transpose(z)
##  return (x,y,z,xmin,xmax,ymin,ymax,zmin,zmax)
#
#def Contour2D(fileID,num = 0,simNum = 0):
#  plt.clf()
#  file = GetPlotFile(fileID,num,simNum)
#  if not file:
#    return False
#  auxDict,xmin,xmax,ymin,ymax,zmin,zmax,xscale,yscale,zscale,title = AuxContour(file)
#  AuxContourLabel(auxDict,xmin,xmax,ymin,ymax,xscale,yscale,title)
#  plt.ion()
#  plt.show()
#  return True
#
#def MovieContour2D(fileID,simNum = 0):
#  plt.clf()
#  fileList = []
#  numList = GetNumListMovie2D(fileID)
#  print numList
#  for num in numList:
#    Contour2D(fileID,num,simNum)
#    fName = str(fileID) + "_" + str(num) + '.png' 
#    plt.savefig(fName)
#    fileList.append(fName)
#    print fName
#  try:
#    command = GetMovieCommand(fileList,fileID)
#    os.spawnvp(os.P_WAIT,'mencoder',command)
#    print str(fileID) + ".avi generated." 
#  except:
#    print str(fileID) + ".avi NOT generated." 
#    return
#
#def GetNumListMovie2D(fileID):
#  file = fileID + '_0_0.dat'
#  auxDict = ProcessAux(file) 
#  pprint(auxDict)
#  z = np.genfromtxt('Zdiconfigsance2D.dat')
#  numList = np.arange(np.size(z))
#  indxMax = z/float(auxDict["pscale"]) <= float(configs.G["maxZ"]) 
#  numList = numList[indxMax]
#  z = z[indxMax]
#  indxMin =  z/float(auxDict["pscale"]) >= float(configs.G["minZ"]) 
#  numList = numList[indxMin]
#  z = z[indxMin]
#  sz = len(numList)
#  if sz > int(configs.G['mov2D']):
#    indxStep = round(float(sz)/int(configs.G['mov1D']))
#    if indxStep == 0:
#      indxStep = 1
#    numList = numList[0:sz:indxStep]
#  return numList
#
#
#def LoadFileData2D(file):
#
#  f = open(file)
#  line = f.readline()
#  while(line.startswith('#')):
#    line = f.readline()
#  nRow,nCol = line.split()
#  nRow = int(nRow)
#  nCol = int(nCol)
#  x = []
#  y = []
#  for i in range(nRow):
#    x.append(float(f.readline()))
#  for i in range(nCol):
#    y.append(float(f.readline()))
#  z = np.genfromtxt(f)
#  f.close()
#
#  x = np.array(x)
#  y = np.array(y)
#  return (x,y,z)
#
#def AuxContour(file):
#  xscale = 1.0 
#  yscale = 1.0 
#  zscale = 1.0 
#  pscale = 1.0 
#  vmax = 0.0
#  vmin = 0.0
#  title = []
#  auxDict = ProcessAux(file)
#  x,y,z = LoadFileData2D(file)
#  x,y,z,xmin,xmax,ymin,ymax,zmin,zmax = ProcessData2D(x,y,z,auxDict)
#  if(configs.G["scale"] == 'nonDim'):
#    if "xscale" in auxDict:
#      xscale = float(auxDict['xscale'])
#    if "yscale" in auxDict:
#      yscale = float(auxDict['yscale'])
#    if 'zscale' in auxDict:
#      zscale = float(auxDict['zscale'])
#      vmax = zmax
#    if 'pscale' in auxDict:
#      pscale = float(auxDict['pscale'])
#  elif(configs.G["scale"] == 'dimscale'):
#    if 'xscale' in auxDict:
#      if(auxDict['xcordID'] == 'ST'):
#        xscale = 1.0/float(configs.G['xdimscale'])
#      else:
#        xscale = float(configs.G['xdimscale'])
#    if 'yscale' in auxDict:
#      if(auxDict['ycordID'] == 'SR'):
#        yscale = 1.0/float(configs.G['ydimscale'])
#      else:
#        yscale = float(configs.G['ydimscale'])
#    if 'zscale' in auxDict:
#      zscale = float(configs.G['zdimscale'])
#      vmax = zmax*float(auxDict['zscale'])/zscale
#    if 'pscale' in auxDict:
#      pscale = float(configs.G['pdimscale'])
#  elif(configs.G["scale"] == 'noscale'):
#    if 'zscale' in auxDict:
#      vmax = zmax*float(auxDict['zscale'])
#
#  x = x/xscale
#  y = y/yscale
#  z = z/zscale
#
#  X,Y = np.meshgrid(x,y)
#  if(auxDict['logz'] == 'logz'):
#    CS = plt.contourf(X,Y,z,locator=ticker.LogLocator())
#  else:
#    CS = plt.contourf(X,Y,z)
#  CB = plt.colorbar()
#
##  vmin = vmax/10.0
##  v = np.linspace(vmin,vmax,10,endpoint = 'true')
##  pprint(v)
##  if 'zscale' in auxDict:
##    if(configs.G["scale"] == 'nonDim'):
##      CB = plt.colorbar(ticks=v,format='%0.2f')
##    else:
##      CB = plt.colorbar(ticks=v,format='%0.2e')
##  else:
##    CB = plt.colorbar()
#
#  plt.hold(True)
#
#  if 'legend' in auxDict:
#    title.append(auxDict['legend'])
#
#  return (auxDict,xmin,xmax,ymin,ymax,zmin,zmax,xscale,yscale,zscale,title)
#
#
#def AuxContourLabel(auxDict,xmin,xmax,ymin,ymax,xscale,yscale,title):
#  xstr = ""
#  ystr = ""
##  zstr = ""
#  if(configs.G['scale'] == 'nonDim'):
#    xstr = xstr + auxDict['xlabel'] + '[' + auxDict["xscale_str"] + ']' 
#    ystr = ystr + auxDict['ylabel'] + '[' + auxDict["yscale_str"] + ']' 
##    zstr = zstr + auxDict['zlabel'] + '[' + auxDict["zscale_str"] + ']' 
##    plt.zlim([zmin,zmax])
#  elif(configs.G['scale'] == 'noscale'):
#    xstr = xstr + auxDict['xlabel'] + '[' + auxDict["xunit_str"] + ']' 
#    ystr = ystr + auxDict['ylabel'] + '[' + auxDict["yunit_str"] + ']' 
##    zstr = zstr + auxDict['zlabel'] + '[' + auxDict["zunit_str"] + ']' 
##    plt.zlim([zmin*zscale,zmax*zscale])
#  elif(configs.G['scale'] == 'dimscale'):
#    if 'xscale' in auxDict:
#      xstr = xstr + auxDict['xlabel'] + "[" + configs.G['xdimscale_str'] + auxDict["xunit_str"] + "]" 
#    else:
#      xstr = xstr + auxDict['xlabel'] + " [arb.]" 
#    if 'yscale' in auxDict:
#      ystr = auxDict['ylabel'] + "[" + configs.G['ydimscale_str'] + auxDict["yunit_str"] + "]" 
#    else:
#      ystr = auxDict['ylabel'] + " [arb.]" 
#
#  xstr = '$' + xstr + '$'
#  ystr = '$' + ystr + '$'
#  plt.xlabel(xstr)
#  plt.ylabel(ystr)
#
#  if(configs.G['title'] == 'on'):
#    titstr = ""
#    if 'title_str' in auxDict:
#      titstr = titstr + str(auxDict['title_str'])
#    if 'pval' in auxDict:
#      if(configs.G["scale"] == 'nonDim'):
#        val = float(auxDict["pval"])/float(auxDict['pscale']) 
#        titstr = titstr + str(auxDict['pval']) + ' [$' + str(auxDict['pscale_str']) + '$]'
#      elif(configs.G["scale"] == 'noscale'):
#        val = float(auxDict["pval"])
#        titstr = titstr + str(val) + ' [' + str(auxDict['punit_str']) + ']'
#      elif(configs.G['scale'] == 'dimscale'):
#        val = float(auxDict['pval'])/float(configs.G['pdimscale'])
#        titstr = titstr + str(val) + ' [$' + configs.G['pdimscale_str'] + str(auxDict['punit_str']) + '$]'
#      
#    plt.title(titstr)
#     
##  if(configs.G['legend'] == 'on'):
##    plt.legend(title,loc='best')
#
##
##def MultiPlotH1D(fileID,num = 0):
##  fileList = GetMultiPlotFileList(fileID,num)
##  auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList = AuxMultiPlot1D(fileList)
##  AuxPlotLabel1D(auxDict,xmin,xmax,ymin,ymax,xscale,yscale,titleList)
##  plt.ion()
##  plt.show()
##  return True
##
##def MultiPlot1D(fileID,num = 0):
##  plt.clf()
##  return MultiPlotH1D(fileID,num)
##
##def GetNumListMovie1D(fileID):
##  file = fileID + '_0_0.dat'
##  auxDict = ProcessAux(file) 
##  print auxDict
##  pprint(auxDict)
##  z = np.genfromtxt('Zdiconfigsance1D.dat')
##  numList = np.arange(np.size(z))
##  indxMax = z/float(auxDict["pscale"]) <= float(configs.G["maxZ"]) 
##  numList = numList[indxMax]
##  z = z[indxMax]
##  indxMin =  z/float(auxDict["pscale"]) >= float(configs.G["minZ"]) 
##  numList = numList[indxMin]
##  z = z[indxMin]
##  sz = len(numList)
##  print numList
##  if sz > int(configs.G['mov1D']):
##    indxStep = np.ceil(sz/int(configs.G['mov1D']))
##    numList = numList[0:sz:indxStep]
##  return numList
##
##def MultiMovie1D(fileID):
##
##  plt.clf()
##  fileList = []
##  numList = GetNumListMovie1D(fileID)
##  for num in numList:
##    MultiPlot1D(fileID,num)
##    fName = str(fileID) + "_" + str(num) + '.png' 
##    plt.savefig(fName)
##    fileList.append(fName)
##  try:
##    print fileList
##    command = GetMovieCommand(fileList,fileID,settings)
##    os.spawnvp(os.P_WAIT,'mencoder',command)
##    print str(fileID) + ".avi generated." 
##  except:
#    print str(fileID) + ".avi NOT generated." 
#    return
#


