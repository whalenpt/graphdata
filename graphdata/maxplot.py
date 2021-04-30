
#from shared1D import AuxPlotLabel1D 
from .shared1D import ProcessData1D 
from .helper import GenFileList 
from .helper import GetData1D 
from .helper import GetDataFileInfo
from .helper import GenFileList
from .helper import ProcessAux
from .helper import GetSimNums
from .helper import GetRepFileList
from .helper import LoadData1D
from .helper import LoadParams
from matplotlib import ticker 
from mpl_toolkits.mplot3d.axes3d import Axes3D 
from matplotlib import cm 
from .plot1D import _PlotSize 
import os 
import sys 
import glob
from graphdata import plt
from graphdata import configs 
from graphdata import np 
from pprint import pprint

def Max(*args):
  """

  Plot max of 1D data. 

  Max(fileID,fileRange,plotLimits,options):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat 
    e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the
    fileID is simply 'T'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the
      fileID are used.  fileRange does not need to specify minFileNum or
      maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plotting range of the Evolve function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimits list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables.  plotLimits does
      not need to specify a minimum and maximum y value 
      e.g. Evolve('T',10,[0 1]) will plot data with an input value between 0
      and 1 

    
    e.g. Max1D('T',[10,0,60],[0,1,-10,10]) will produce a Max1D plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. Max1D('R') will produce a Max1D plot using all 'R' fileID data
    R_0.dat, R_1.dat, ..., R_MAX#.dat
  """
  
 # fileList = GenFileList(*args)
  fileList = GenFileList(*args)
  print(fileList)
  plotArgs = args[2:]
  xvec = []
  yvec = []
  auxDict = dict() 
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    x,y,auxDict = GetData1D(fileID,repNum,*plotArgs)
    x,y,auxDict = ProcessData1D(x,y,auxDict)
    if y.any():
      yval = np.amax(np.absolute(y))
      yvec.append(yval)
      if "pscale" in auxDict: 
        if(configs.G["scale"] == 'nonDim'):
          xvec.append(float(auxDict['pval'])/float(auxDict['pscale']))
        elif(configs.G["scale"] == 'dimscale'):
          xvec.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
        elif(configs.G["scale"] == 'noscale'):
          xvec.append(float(auxDict['pval']))
      else:
        xvec.append(repNum)
   
  configs.DefaultLS()
  plt.figure()
  plt.plot(xvec,yvec,configs.LS)
#  plt.plot(x,y,'b--',dashes = (4,2))
  plt.plot(xvec,yvec,'b--',dashes = (2,1))
  auxDict = ProcessAux(fileList[0])
  AuxMaxLabel(auxDict)
  if 'legend' in auxDict:
    plt.legend(['$'+str(auxDict["legend"])+'$'],loc='best')
  plt.ion()
  plt.show()
  return yvec 

def MaxH(*args):
  """

  Plot max of 1D data and keeps current figure for superimposing more data. 

  MaxH(fileID,fileRange,plotLimits,options):
  Args:
    fileID: ID for data files where files look like fileID_fileNum.dat 
    e.g. if data files for T data are T_0.dat,T_1.dat,T_2.dat,...  then the
    fileID is simply 'T'

    fileRange = [numFiles,minFileNum,maxFileNum]
    fileRange: Specifies the files from which to accept data.
      numFiles:     Number of 1D data files to plot
      minFileNum:   Start file number.  
      maxFileNum:   End file number.  
      If no fileRange is given, then all data files corresponding to the
      fileID are used.  fileRange does not need to specify minFileNum or
      maxFileNum e.g. Evolve('T',[10]) and Evolve('T',10) evolve 10 evenly
      spaced data files of fileID 'T' starting with the first available data
      file and ending with the last available data

    plotLimits = [minX,maxX,minY,maxY]
    plotLimits: Specifies the plotting range of the Evolve function data.
      minX:  Minimum x value limit
      maxX:  Maximum x value limit
      minY:  Minimum y value limit
      maxY:  Maximum y value limit
      If no plotLimits list is given, then all data is used in the plots and
      then minimum and maximum graph limits will depend on the minimum and
      maximum data limits of the input and output variables.  plotLimits does
      not need to specify a minimum and maximum y value 
      e.g. Evolve('T',10,[0 1]) will plot data with an input value between 0
      and 1 

    
    e.g. Max1D('T',[10,0,60],[0,1,-10,10]) will produce a Max1D plot using
    10 (input,output) data pairs starting with T_0.dat, then going to T_6.dat,
    then to ..., and lastly T_60.dat. The graph will truncate inputs to the
    range of 0 to 1 and plot output in the range of -10 to 10

    e.g. Max1D('R') will produce a Max1D plot using all 'R' fileID data
    R_0.dat, R_1.dat, ..., R_MAX#.dat
  """
  
  fileList = GenFileList(*args)
  plotArgs = args[2:]
  xvec = []
  yvec = []
  auxDict = dict() 
  for file in fileList: 
    fileID,repNum = GetDataFileInfo(file) 
    x,y,auxDict = GetData1D(fileID,repNum,*plotArgs)
    x,y,auxDict = ProcessData1D(x,y,auxDict)
    if y.any():
      yval = np.amax(np.absolute(y))
      yvec.append(yval)
      if "pscale" in auxDict: 
        if(configs.G["scale"] == 'nonDim'):
          xvec.append(float(auxDict['pval'])/float(auxDict['pscale']))
        elif(configs.G["scale"] == 'dimscale'):
          xvec.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
        elif(configs.G["scale"] == 'noscale'):
          xvec.append(float(auxDict['pval']))
      else:
        xvec.append(repNum)
 
  labs = plt.get_figlabels() 
  if "MaxH" not in labs:
    configs.DefaultLS()
    if 'legend' in auxDict:
      configs.SetLegend('$'+str(auxDict["legend"])+'$')
  else:
    configs.ToggleLS()
    if 'legend' in auxDict:
      configs.AddLegend('$'+str(auxDict["legend"])+'$')
  width,height = _PlotSize(*args)
  p = plt.figure("MaxH",figsize=(width,height))
  print(width,height)
  if len(args) < 4:
    plt.plot(xvec,yvec,configs.LS)
  else:
    plt.plot(xvec,yvec,str(args[3]))

  plt.hold(True) 

#  plt.plot(xvec,yvec,'k.')
#  plt.plot(xvec,yvec,'cd',markersize=1,fillconfigsyle='full',markerfacecolor='c',markeredgecolor='c')
#  plt.plot(xvec,yvec,'g-.',dashes = (7,4,3,4))
#  plt.plot(xvec,yvec,'b--',dashes = (2,1))
#  plt.plot(xvec,yvec,'r')
#  plt.plot(xvec,yvec,configs.LS)
  auxDict = ProcessAux(fileList[0])
  AuxMaxLabel(auxDict)
  if configs.LegendList:
    plt.legend(configs.LegendList,loc='best')
  plt.ion()
  plt.show()
  return p 

def AuxMaxLabel(auxDict):
  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = ystr + '$' + auxDict['plabel'] + '$' + '[$' + auxDict["pscale_str"] + '$]' 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr = zstr + '$' + auxDict['ylabel'] + '$' + '[$' + auxDict["yscale_str"] + '$]' 
  elif(configs.G['scale'] == 'noscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = ystr + auxDict['plabel'] + '[$' + auxDict["punit_str"] + '$]' 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = zstr + auxDict['ylabel'] + '[$' + auxDict["yunit_str"] + '$]' 
  elif(configs.G['scale'] == 'dimscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + "[$" + configs.G['pdimscale_str'] + auxDict["punit_str"] + "$]" 
    elif 'plabel' in auxDict:
      ystr = auxDict['plabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = zstr + auxDict['ylabel'] + "[$" + configs.G['ydimscale_str'] + auxDict["yunit_str"] + "$]" 

  print(ystr)
  plt.xlabel(ystr)
  plt.ylabel(zstr)

def MaxEvolveS(*args):

  if(len(args) < 2):
    sys.exit("Not enough arguments to MaxEvolveS.")
  
  sortedList = []
  auxDict = dict()
  simNums = GetSimNums(args[0])
  fileSID = str(args[0]) + "_" + str(simNums[0])
  fileList = GenFileList(fileSID,args[1])

  num = 0
  y = []
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs.G["scale"] == 'nonDim'):
        y.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs.G["scale"] == 'dimscale'):
        y.append(float(auxDict['pval'])/float(configs.G['pdimscale']))
      elif(configs.G["scale"] == 'noscale'):
        y.append(float(auxDict['pval']))
    else:
      y.append(num)
      num = num + 1

  x = []

  for i in simNums:
    auxFile = 'ParamBin_' + str(i) + '.txt'
    paramDict = LoadParams(auxFile)
    for item in paramDict: 
      if item.startswith(str(args[2])):
        x.append(float(paramDict[item]))
        found = True;
    if not found:          
      print("Parameter " + str(args[2]) + " not found. ") 
      print("Here is the dictionary. ")
      pprint(paramDict)
      sys.exit("Could not find x-parameter.")

  print(x)
  print(y)
  X,Y = np.meshgrid(x,y)
  X = np.transpose(X)
  Y = np.transpose(Y)

  max_x = 0;
  max_y = 0;
  max_z = 0;
  xcnt = 0; 
  Z = np.zeros((len(x),len(y)))
  plotArgs = args[3:]
  for i in simNums:
    fileSID = str(args[0]) + "_" + str(i)
    fileList = GenFileList(fileSID,args[1])
    ycnt = 0; 
    for file in fileList: 
      fileID,repNum = GetDataFileInfo(file) 
      xgarb,z,auxDict = GetData1D(fileSID,repNum,*plotArgs)
      xgarb,z,auxDict = ProcessData1D(xgarb,z,auxDict)
      if z.any():
        zval = np.amax(np.absolute(z))
        if zval > max_z:
          max_x = x[xcnt]
          max_y = y[ycnt]
          max_z = zval
        Z[xcnt,ycnt] = zval
      ycnt = ycnt + 1;
    xcnt = xcnt + 1

  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs.G["cmap"]),linewidth=0,antialiased=True,shade=False) 
  plt.xlim([x[0],x[-1]])
  plt.ylim([y[0],y[-1]])

  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'pscale_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + auxDict["pscale_str"] + ')' 
    elif 'pscale_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel']  + '(' + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] 
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'dimscale'):
    if 'punit_str' in auxDict and 'plabel' in auxDict:
      ystr = auxDict['plabel'] + '(' + configs.G['pdimscale_str'] + auxDict["punit_str"] + ')' 
    elif 'punit_str' not in auxDict and 'plabel' in auxDict:
      ystr = ystr + auxDict['plabel'] + " [arb.]" 
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + '(' + configs.G['ydimscale_str'] + auxDict["yunit_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + " [arb.]" 

  if 'ymin' in auxDict and 'ymax' in auxDict:
    ax.set_zlim3d([auxDict['ymin'],auxDict['ymax']])

  ystr = '$' + ystr + '$'
  zstr = '$' + zstr + '$'
  ax.set_xlabel(r'$\phi_0$')
  ax.set_ylabel(ystr)
  ax.set_zlabel(zstr)

  if 'angle1' in auxDict and 'angle2' in auxDict:
    ax.view_init(auxDict['angle1'],auxDict['angle2'])

  ax.view_init(39,-52)
  numTicks = int(configs.G['NumberSurfaceTicks'])
  ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.zaxis.set_major_locator(ticker.LinearLocator(4))
  
  labelType = str(configs.G['SurfaceTickFormat'])
  ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))

  plt.ion()
  plt.show()
  plt.tight_layout()
  print(max_x) 
  print(max_y)
  print(max_z)
  return ax 

def MaxMaxEvolveS(*args):

  if(len(args) < 2):
    sys.exit("Not enough arguments to MaxEvolveS.")
  
  sortedList = []
  auxDict = dict()
  simNums = GetSimNums(args[0])
  fileSID = str(args[0]) + "_" + str(simNums[0])
  fileList = GenFileList(fileSID,args[1])

  Nx = int(args[3]) 
  Ny = int(args[5])
  X = np.zeros(len(simNums))
  Y = np.zeros(len(simNums))
  cnt = 0
  for i in simNums:
    auxFile = 'ParamBin_' + str(i) + '.txt'
    paramDict = LoadParams(auxFile)
    xfound = False
    yfound = False
    for item in paramDict: 
      if item.startswith(str(args[2])):
        X[cnt] = float(paramDict[item])
        xfound = True;
      if item.startswith(str(args[4])):
        Y[cnt] = float(paramDict[item])
        yfound = True;
    if not xfound:          
      print("Parameter " + str(args[2]) + " not found. ") 
      print("Here is the dictionary. ")
      pprint(paramDict)
      sys.exit("Could not find x-parameter.")
    if not yfound:          
      print("Parameter " + str(args[4]) + " not found. ") 
      print("Here is the dictionary. ")
      pprint(paramDict)
      sys.exit("Could not find x-parameter.")
    cnt = cnt + 1

  X = X.reshape(Nx,Ny)
  Y = Y.reshape(Nx,Ny)
  max_x = 0.0;
  max_y = 0.0;
  max_z = 0.0;
  xcnt = 0; 
  Z = np.zeros((Nx,Ny))
  plotArgs = args[6:]
  for i in np.arange(Nx):
    for j in np.arange(Ny):
      simCnt = i*Nx + j
      fileSID = str(args[0]) + "_" + str(simCnt)
      fileList = GenFileList(fileSID,args[1])
      ycnt = 0
      xmaxsim = 0.0
      ymaxsim = 0.0
      zmaxsim = 0.0
      for file in fileList: 
        fileID,repNum = GetDataFileInfo(file) 
        xgarb,z,auxDict = GetData1D(fileSID,repNum,*plotArgs)
        xgarb,z,auxDict = ProcessData1D(xgarb,z,auxDict)
        if z.any():
          zval = np.amax(np.absolute(z))
          if zval > zmaxsim:
            xmaxsim = X[i,j] 
            ymaxsim = Y[i,j] 
            zmaxsim = zval
      if zmaxsim > max_z:
        max_x = xmaxsim
        max_y = ymaxsim
        max_z = zmaxsim 
      Z[i,j] = zmaxsim 

  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
  p = ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=str(configs.G["cmap"]),linewidth=0,antialiased=True,shade=False) 
#  plt.xlim([x[0],x[-1]])
#  plt.ylim([y[0],y[-1]])

  ystr = ""
  zstr = ""
  if(configs.G['scale'] == 'nonDim'):
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'noscale'):
    if 'yscale_str' in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] + '(' + auxDict["yscale_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr =  auxDict['ylabel'] 
  elif(configs.G['scale'] == 'dimscale'):
    if 'yunit_str' in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + '(' + configs.G['ydimscale_str'] + auxDict["yunit_str"] + ')' 
    elif 'yscale_str' not in auxDict and 'ylabel' in auxDict:
      zstr = auxDict['ylabel'] + " [arb.]" 

  if 'ymin' in auxDict and 'ymax' in auxDict:
    ax.set_zlim3d([auxDict['ymin'],auxDict['ymax']])

  zstr = '$' + zstr + '$'
  ax.set_xlabel(r'$\phi_0$')
  ax.set_ylabel(r'$\theta_0$')
  ax.set_zlabel(zstr)

  if 'angle1' in auxDict and 'angle2' in auxDict:
    ax.view_init(auxDict['angle1'],auxDict['angle2'])

  ax.view_init(39,-52)
  numTicks = int(configs.G['NumberSurfaceTicks'])
  ax.xaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.yaxis.set_major_locator(ticker.LinearLocator(numTicks))
  ax.zaxis.set_major_locator(ticker.LinearLocator(4))
  
  labelType = str(configs.G['SurfaceTickFormat'])
  ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))
  ax.zaxis.set_major_formatter(ticker.FormatStrFormatter(labelType))

  plt.ion()
  plt.show()
  plt.tight_layout()
  print(max_x) 
  print(max_y)
  print(max_z)
  return ax 


