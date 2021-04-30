#!/usr/bin/python
# Filename: converg.py

import shutil 
import glob
import os 
import string
import re
import sys 
import math
import fnmatch
import matplotlib.gridspec as gridspec
from operator import itemgetter
from graphdata import plt
from graphdata import np 
from graphdata import configs 
from numpy import linalg as LA
from .helper import LoadData1D
from .helper import LoadData2D
from .helper import LoadParams
from pprint import pprint
from matplotlib import ticker 
from .Settings.figsets import figsize_and_margins 

def ConvergeH(fileName,yexact,ctype='cstep'):
  """
  Converge plots

  ConvergeH(fileName,yexact,type):
  Args:
    fileName: Name of data files to compare 
    e.g. X_1.dat
    
    yexact: Exact solution. Often can be best numerical solution
    type: Specifies the convergence type to be plotted.

      cstep (default): Step size vs. relative error. For constant step methods 
      speed :  Speed vs relative error. 
      relerr : Relative error tolerance vs. relative error. For adaptive step methods.
      stages : Runge-kutta stage speed vs. relative error.
      coeff :  ETD coefficient cost vs. relative error.
      incrf :  ETD increment floor vs. speed. For adaptive ETD methods.
      decrf :  ETD decrement ceiling vs. speed. For adaptive ETD methods.

  """

  conv_opts = ['cstep','speed','relerr','coeff','coeff2',\
      'stages','stages2','incrf','decrf','modecutoff']

  if ctype not in conv_opts:
    print('Did not recognize ctype. Here is a list of the options ')
    print(conv_opts)
    sys.exit()
  x,y,auxDict = ConvergeData(fileName,yexact,ctype)
  width,height = ConvSize()
  fsize,margins = figsize_and_margins(plotsize=(width,height))
  labs = plt.get_figlabels() 

  if ctype == 'cstep':
    if "CSTEP" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("CSTEP",figsize=fsize)
    plt.xlabel('Relative time step')
    plt.ylabel('Relative error')
  elif ctype == 'speed':
    if "SPEED" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("SPEED",figsize=fsize)
    plt.xlabel('Computer time (s)')
    plt.ylabel('Relative error')
  elif ctype == 'relerr':
    if "RELERR" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("RELERR",figsize=fsize)
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('Relative error')
  elif ctype == 'coeff':
    if "COEFF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("COEFF",figsize=fsize)
    plt.xlabel('ETD coefficient cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'coeff2':
    if "COEFF2" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("COEFF2",figsize=fsize)
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('ETD coefficient cost (s)')
  elif ctype == 'stages':
    if "STAGES" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("STAGES",figsize=fsize)
    plt.xlabel('RK stage evaluation cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'stages2':
    if "STAGES2" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("STAGES2",figsize=fsize)
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('RK stage evaluation cost (s)')
  elif ctype == 'incrf':
    if "INCRF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("INCRF",figsize=fsize)
    plt.xlabel('Expansion floor')
    plt.ylabel('Computer time (s)')

  elif ctype == 'decrf':
    if "DECRF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("DECRF",figsize=fsize)
    plt.xlabel('Compression ceiling')
    plt.ylabel('Computer time (s)')
  elif ctype == 'modecutoff':
    if "MODECUTOFF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("MODECUTOFF",figsize=fsize)
    plt.xlabel('Contour evaluation cutoff mode')
    plt.ylabel('Relative error')

  if ctype != 'incrf' and ctype != 'decrf':
    plt.loglog(x,y,configs.LS,markersize=4)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.LogLocator(numticks=6))
    ax.yaxis.set_major_locator(ticker.LogLocator(numticks=6))
#    ax.xaxis.set_major_locator(ticker.LogLocator(numdecs=6))
#    ax.yaxis.set_major_locator(ticker.LogLocator(numdecs=6))
    ax.xaxis.grid(b =
        True,which='minor',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.xaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.yaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  elif ctype == 'incrf' or ctype == 'decrf':
    plt.plot(x,y,configs.LS,markersize=4)

  plt.hold(True) 
  plt.ion()
  plt.show()
#  configs.SetLS(LSkey)

def TableP(fileName,yexact,pName):
  """
  """
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,auxDict = LoadData1D(nm)
        paramFile = root + '/ParamBin*'
        auxFile = glob.glob(paramFile)
        if(len(auxFile) == 1):
          found = False;
          paramDict = LoadParams(auxFile[0])
          for item in paramDict: 
            if item.startswith(str(pName)):
              sortedList.append(
                  (root,float(paramDict[item]),LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) ))
              found = True;
          if not found:          
            print(str(pName) + " not found.")
            print("Here is the dictionary. ")
            pprint(paramDict)
        else:
          print("cannot open param file. ") 

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(1), reverse = True)

  errVec = []
  x = []
  name = []
  for item in sortedList:
    if not math.isnan(item[2]):
      name.append(item[0])
      x.append(item[1])
      errVec.append(item[2])
  x = np.array(x)
  errVec = np.array(errVec)
  if len(x) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)

  print("%s %s %s" % ("Directory",str(pName),"Error"))
  for c1,c2,c3 in zip(name,x,errVec):
    print("%1.10s %1.3e %1.3e" % (c1,c2,c3))

def TableS(fileName,yexact,pName):
  """
  """
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,auxDict = LoadData1D(nm)
        paramFile = root + '/solver_stat*'
        auxFile = glob.glob(paramFile)
        if(len(auxFile) == 1):
          paramDict = LoadParams(auxFile[0])
          if str(pName) in paramDict:
            err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
            timing = float(paramDict[str(pName)])
            if not math.isnan(err):
              sortedList.append( (timing,err))
          else:
            print("Could not find Computer Time. ") 
            print("Here is the dictionary. ")
            pprint(paramDict)
        else:
          print("cannot open param file. ") 

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(0), reverse = True)
  errVec = []
  x = []
  for item in sortedList:
    if not math.isnan(item[1]):
      x.append(item[0])
      errVec.append(item[1])
  x = np.array(x)
  errVec = np.array(errVec)
  if len(x) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)

  print("%s %s" % (str(pName),"Error"))
  for c1,c2 in zip(x,errVec):
    print("%-9e %e" % (c1,c2))

def TablePS(fileName,yexact,pName,sName):
  """
  """
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,auxDict = LoadData1D(nm)
        paramFile1 = root + '/ParamBin*'
        paramFile2 = root + '/solver_stat*'
        auxFile1 = glob.glob(paramFile1)
        auxFile2 = glob.glob(paramFile2)
        if(len(auxFile1) == 1 and len(auxFile2) == 1):
          found = False;
          paramDict1 = LoadParams(auxFile1[0])
          paramDict2 = LoadParams(auxFile2[0])
          timing = 0.0
          epsRel = 0.0
          for item in paramDict1: 
            if item.startswith(str(pName)):
              epsRel = float(paramDict1[item])
          if str(sName) in paramDict2:
            timing = float(paramDict2[str(sName)])
          sortedList.append((epsRel,timing))
        else:
          print("cannot open param file(s). ") 

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(0), reverse = True)
  errVec = []
  x = []
  for item in sortedList:
    if not math.isnan(item[1]):
      x.append(item[0])
      errVec.append(item[1])
  x = np.array(x)
  errVec = np.array(errVec)
  if len(x) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)

  print("%s %s" % (str(pName),str(sName)))
  for c1,c2 in zip(x,errVec):
    print("%-9e %e" % (c1,c2))


def Converge(fileName,yexact,ctype='cstep'):

  LSkey = configs.G['LSvec']
  configs.SetLS('converge')
  x,y,auxDict = ConvergeData(fileName,yexact,ctype)
  width,height = ConvSize()
  fsize,margins = figsize_and_margins(plotsize=(width,height))
  p = plt.figure(figsize=fsize)
  configs.DefaultLS()
  if ctype == 'cstep':
    plt.xlabel('Relative time step')
    plt.ylabel('Relative error')
  elif ctype == 'speed':
    plt.xlabel('Computer time (s)')
    plt.ylabel('Relative error')
  elif ctype == 'relerr':
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('Relative error')
  elif ctype == 'coeff':
    plt.xlabel('ETD coefficient cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'coeff2':
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('ETD coefficient cost (s)')
  elif ctype == 'stages':
    plt.xlabel('RK stage evaluation cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'stages2':
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('RK stage evaluation cost (s)')
  elif ctype == 'incrf':
    plt.xlabel('Expansion floor')
    plt.ylabel('Computer time (s)')
  elif ctype == 'decrf':
    plt.xlabel('Compression ceiling')
    plt.ylabel('Computer time (s)')
  elif ctype == 'modecutoff':
    plt.xlabel('Contour evaluation cutoff mode')
    plt.ylabel('Relative error')

  if ctype != 'incrf' and ctype != 'decrf':
    plt.loglog(x,y,configs.LS,markersize=4)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.LogLocator(numticks=6))
    ax.yaxis.set_major_locator(ticker.LogLocator(numticks=6))
#    ax.xaxis.set_major_locator(ticker.LogLocator(numdecs=6))
#    ax.yaxis.set_major_locator(ticker.LogLocator(numdecs=6))
    ax.xaxis.grid(b =
        True,which='minor',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.xaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.yaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  elif ctype == 'incrf' or ctype == 'decrf':
    plt.plot(x,y,configs.LS,markersize=4)

  plt.ion()
  plt.show()
  configs.SetLS(LSkey)

def ConvergeD(fileName,yexact,ctype='cstep'):
  labs = plt.get_figlabels() 
  if "ConvergeH" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  x1,err1,auxDict1 = ConvergeData(fileName,yexact,'vrel')
  x2,err2,auxDict2 = ConvergeData(fileName,yexact,'speed')
  gs = gridspec.GridSpec(1,2,width_ratios=[1,1])
  ax1 = plt.subplot(gs[0])
  ax1 = plt.loglog(x1,err1,configs.LS,markersize=2)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  ax2 = plt.subplot(gs[1])
  ax2 = plt.loglog(x2,err2,configs.LS,markersize=2)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  plt.ion()
  plt.show()


def ConvergeHRS(fileName,yexact):
  h,err,auxDict = ConvergeData(fileName,yexact)
  plt.semilogy(h,err,configs.LS,markersize=4)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  plt.hold(True) 
  ConvPlotLabelH(auxDict,h,err)
  plt.ion()
  plt.show()
  configs.ToggleLS()

def ConvergeO(fileName,yexact,order,alpha=0.5):

  width,height = ConvSize()
  fsize,margins = figsize_and_margins(plotsize=(width,height))
  plt.figure("ConvergeO",figsize=fsize)
  h,err,auxDict = ConvergeData(fileName,yexact)
  sz = len(h)
  indx = np.floor(alpha*sz) 
  C = err[indx]/pow(h[indx],order)
  ordVec = []
  hord = []
  for val in h:
    ordVec.append(C*pow(val,order))
    hord.append(val)
  ordVec = ordVec[:-1]
  hord = hord[:-1]
  h = h[:-1]
  err = err[:-1]

  configs.DefaultLS()
  plt.loglog(h,err,'k-d',hord,ordVec,'g-*',markersize=6)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  ConvPlotLabel(auxDict,h,err)

  plt.xlim([0.95*h[-1],1.05*h[0]])
  plt.ylim([0.5*err[-1],2*err[0]])
  plt.legend(['Method Error','Order = '+ str(order)],loc='best')
  plt.ion()
  plt.show()


def ConvergeData(fileName,yexact,ctype='cstep'):
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,auxDict = LoadData1D(nm)
        if ctype == 'cstep':
          paramFile = root + '/ParamBin*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            for item in paramDict: 
              if item.startswith('StepSize'):
                sortedList.append(
                    (root,float(paramDict[item]),LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) ))
                found = True;
            if not found:          
              print("StepSize not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'speed':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Computer Time' in paramDict:
              err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
              timing = float(paramDict['Computer Time'])
              if not math.isnan(err):
                sortedList.append( (root,timing,err))
            else:
              print("Could not find Computer Time. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'relerr':
          paramFile = root + '/ParamBin*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            for item in paramDict: 
              if item.startswith('EpsRel'):
                err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
                sortedList.append((root,float(paramDict[item]),err ))
                found = True;
            if not found:          
              print("EpsRel not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'coeff':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Timer Coefficient' in paramDict:
              err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
              timing = float(paramDict['Timer Coefficient'])
              if not math.isnan(err):
                sortedList.append( (root,timing,err))
            else:
              print("Could not find SolverStepSize. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'coeff2':
          paramFile1 = root + '/ParamBin*'
          paramFile2 = root + '/solver_stat*'
          auxFile1 = glob.glob(paramFile1)
          auxFile2 = glob.glob(paramFile2)
          if(len(auxFile1) == 1 and len(auxFile2) == 1):
            found = False;
            paramDict1 = LoadParams(auxFile1[0])
            paramDict2 = LoadParams(auxFile2[0])
            timing = 0.0
            epsRel = 0.0
            for item in paramDict1: 
              if item.startswith('EpsRel'):
                epsRel = float(paramDict1[item])
            if 'Timer Coefficient' in paramDict2:
              timing = float(paramDict2['Timer Coefficient'])
            sortedList.append((root,epsRel,timing))
          else:
            print("cannot open param file(s). ") 
        elif ctype == 'stages':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Solver Stepping' in paramDict:
              err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
              timing = float(paramDict['Solver Stepping'])
              if not math.isnan(err):
                sortedList.append( (root,timing,err))
            else:
              print("Could not find Solver Computer Time. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'stages2':
          paramFile1 = root + '/ParamBin*'
          paramFile2 = root + '/solver_stat*'
          auxFile1 = glob.glob(paramFile1)
          auxFile2 = glob.glob(paramFile2)
          if(len(auxFile1) == 1 and len(auxFile2) == 1):
            found = False;
            paramDict1 = LoadParams(auxFile1[0])
            paramDict2 = LoadParams(auxFile2[0])
            timing = 0.0
            epsRel = 0.0
            for item in paramDict1: 
              if item.startswith('EpsRel'):
                epsRel = float(paramDict1[item])
            if 'Timer Coefficient' in paramDict2:
              timing = float(paramDict2['Solver Stepping'])
            sortedList.append((root,epsRel,timing))
          else:
            print("cannot open param file(s). ") 
        elif ctype == 'incrf' or ctype == 'decrf':
          val = 1.0
          speedVal = 1.0
          paramFile = root + '/ParamBin*'
          solverFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          auxFile2 = glob.glob(solverFile)
          if(len(auxFile) == 1 and len(auxFile2) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            if ctype == 'incrf':
              for item in paramDict: 
                if item.startswith('IncrFactor'):
                  val = float(paramDict[item])
                  found = True;
            else:
              for item in paramDict: 
                if item.startswith('DecrFactor'):
                  val = float(paramDict[item])
                  found = True;
            solverDict = LoadParams(auxFile2[0])
            found2 = False;
            if 'Computer Time' in solverDict:
              speedVal = float(solverDict['Computer Time'])
              found2 = True
            if not found: 
              print("Increment Factor not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
            if not found2:          
              print("Computer time not found. ") 
              print("Here is the dictionary. ")
              pprint(solverDict)
            if found and found2:
              sortedList.append( (root,val,speedVal))
        elif ctype == 'modecutoff':
          paramFile = root + '/ParamBin*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            for item in paramDict: 
              if item.startswith('ModeCutoff'):
                err = LA.norm((y-yexact),np.inf)/LA.norm(yexact,np.inf) 
                sortedList.append((root,float(paramDict[item]),err ))
                found = True;
            if not found:          
              print("ModeCutoff not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 

        else:
          sys.exit("ConvergeType not recognized.")

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(1), reverse = True)

  errVec = []
  x = []
  name = []
  for item in sortedList:
    if not math.isnan(item[2]):
      name.append(item[0])
      x.append(item[1])
      errVec.append(item[2])
  x = np.array(x)
  errVec = np.array(errVec)
  if len(x) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)

  if 'pval' in auxDict and ctype == 'cstep': 
    x = x/float(auxDict["pval"])

  print("%s %s %s" % ("Directory","xval","yval"))
  for c1,c2,c3 in zip(name,x,errVec):
    print("%1.10s %1.3e %1.3e" % (c1,c2,c3))

 
  return (x,errVec,auxDict)

def Speed(fileName,yexact):
  speed,err,auxDict = SpeedData(fileName,yexact)
  plt.figure()
  configs.DefaultLS()
  plt.loglog(speed,err,configs.LS,markersize=4)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  SpeedPlotLabel(auxDict,speed,err)
  plt.ion()
  plt.show()

def SpeedH(fileName,yexact):
  labs = plt.get_figlabels() 
  if "SpeedH" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  speed,err,auxDict = SpeedData(fileName,yexact)
  plt.figure("SpeedH")
  plt.loglog(speed,err,configs.LS,markersize=4)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  plt.hold(True) 
  SpeedPlotLabelH(auxDict,speed,err)
  plt.ion()
  plt.show()
  configs.ToggleLS()


def SpeedData(fileName,yexact):
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,auxDict = LoadData1D(nm)
        paramFile = root + '/solver_stat*'
        auxFile = glob.glob(paramFile)
        if(len(auxFile) == 1):
          paramDict = LoadParams(auxFile[0])
          if 'Solver Stepping' in paramDict:
            err = LA.norm((y-yexact)/yexact,np.inf)
            timing = float(paramDict['Solver Stepping'])
            if not math.isnan(err) and timing > 1.0:
              sortedLiconfigs.append( (timing,err))
          else:
            print("Could not find SolverStepSize. ") 
            print("Here is the dictionary. ")
            pprint(paramDict)
        else:
          print("cannot open param file. ") 

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(0), reverse = True)
  errVec = []
  speed = []
  for item in sortedList:
      speed.append(item[0])
      errVec.append(item[1])
  speed = np.array(speed)
  errVec = np.array(errVec)
  speed = speed[1:]
  errVec = errVec[1:]
  if len(speed) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)
  print(speed) 
  return (speed,errVec,auxDict)


def ConvPlotLabel(auxDict,h,err):
  xstr = ""
  ystr = ""
  xlab = ""
  ylab = ""
  xstr = 'Relative time step' 
  ystr = 'Relative error'
  if 'pval' in auxDict and 'plabel' in auxDict: 
    ystr = ystr + ' at ' + '$' + auxDict['plabel'] + ' = ' + auxDict['pval'] + '$'
  elif 'pval' in auxDict and 'plabel' not in auxDict:
    ystr = ystr + ' at ' + auxDict['pval']
  plt.xlim([0.7*h[-1],1.3*h[0]])
  plt.xlabel(xstr)
  plt.ylabel(ystr)

def SpeedPlotLabel(auxDict,speed,err):
  xstr = ""
  ystr = ""
  xlab = ""
  ylab = ""
  xstr = 'Computer time (s)' 
  ystr = 'Relative error'
  if 'pval' in auxDict and 'plabel' in auxDict: 
    ystr = ystr + ' at ' + '$' + auxDict['plabel'] + ' = ' + auxDict['pval'] + '$'
  elif 'pval' in auxDict and 'plabel' not in auxDict:
    ystr = ystr + ' at ' + auxDict['pval']

  plt.xlim([0.8*speed[-1],1.2*speed[0]])
  plt.xlabel(xstr)
  plt.ylabel(ystr)

def ConvPlotLabelH(auxDict,h,err):
  xstr = ""
  ystr = ""
  xlab = ""
  ylab = ""
  xstr = 'Relative time step' 
  ystr = 'Relative error'
  if 'pval' in auxDict and 'plabel' in auxDict: 
    ystr = ystr + ' at ' + '$' + auxDict['plabel'] + ' = ' + auxDict['pval'] + '$'
  elif 'pval' in auxDict and 'plabel' not in auxDict:
    ystr = ystr + ' at ' + auxDict['pval']
  plt.xlabel(xstr)
  plt.ylabel(ystr)

def SpeedPlotLabelH(auxDict,speed,err):
  xstr = ""
  ystr = ""
  xlab = ""
  ylab = ""
  xstr = 'Computer time (s)' 
  ystr = 'Relative error'
  if 'pval' in auxDict and 'plabel' in auxDict: 
    ystr = ystr + ' at ' + '$' + auxDict['plabel'] + ' = ' + auxDict['pval'] + '$'
  elif 'pval' in auxDict and 'plabel' not in auxDict:
    ystr = ystr + ' at ' + auxDict['pval']

  plt.xlabel(xstr)
  plt.ylabel(ystr)

def ConvSize():
  width = float(configs.G['ConvergeWidth'])
  height = float(configs.G['ConvergeHeight'])
  return (width,height) 

def Speed(fileName,yexact):
  speed,err,auxDict = SpeedData(fileName,yexact)
  plt.figure()
  configs.DefaultLS()
  plt.loglog(speed,err,configs.LS,markersize=4)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  SpeedPlotLabel(auxDict,speed,err)
  plt.ion()
  plt.show()

def SpeedH(fileName,yexact):
  labs = plt.get_figlabels() 
  if "SpeedH" not in labs:
    configs.DefaultLS()
  else:
    configs.ToggleLS()
  speed,err,auxDict = SpeedData(fileName,yexact)
  plt.figure("SpeedH")
  plt.loglog(speed,err,configs.LS,markersize=4)
  plt.grid(b = True,which='major',linestyle=':')
  plt.grid(b = True,which='minor',linestyle=':')
  plt.hold(True) 
  SpeedPlotLabelH(auxDict,speed,err)
  plt.ion()
  plt.show()
  configs.ToggleLS()


def ConvergeData2D(fileName,zexact,ctype='cstep'):
  sortedList = []
  auxDict = dict()
  for root,dirs,files in os.walk("."):
    for file in files:
      if file == fileName:
        nm = os.path.join(root,file)
        x,y,z,auxDict = LoadData2D(nm)
        if ctype == 'cstep':
          paramFile = root + '/ParamBin*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            for item in paramDict: 
              if item.startswith('StepSize'):
                sortedList.append(
                    (float(paramDict[item]),LA.norm((z-zexact),np.inf)/LA.norm(zexact,np.inf) ))
                found = True;
            if not found:          
              print("StepSize not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'speed':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Computer Time' in paramDict:
              err = LA.norm((z-zexact),np.inf)/LA.norm(zexact,np.inf) 
              timing = float(paramDict['Computer Time'])
              if not math.isnan(err):
                sortedList.append( (timing,err))
            else:
              print("Could not find Computer Time. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'relerr':
          paramFile = root + '/ParamBin*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            for item in paramDict: 
              if item.startswith('EpsRel'):
                err = LA.norm((z-zexact),np.inf)/LA.norm(zexact,np.inf) 
                sortedList.append((float(paramDict[item]),err ))
                found = True;
            if not found:          
              print("EpsRel not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'coeff':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Timer Coefficient' in paramDict:
              err = LA.norm((z-zexact),np.inf)/LA.norm(zexact,np.inf) 
              timing = float(paramDict['Timer Coefficient'])
              if not math.isnan(err):
                sortedList.append( (timing,err))
            else:
              print("Could not find SolverStepSize. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'stages':
          paramFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          if(len(auxFile) == 1):
            paramDict = LoadParams(auxFile[0])
            if 'Solver Stepping' in paramDict:
              err = LA.norm((z-zexact),np.inf)/LA.norm(zexact,np.inf) 
              timing = float(paramDict['Solver Stepping'])
              if not math.isnan(err):
                sortedList.append( (timing,err))
            else:
              print("Could not find Solver Stepping (time). ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
          else:
            print("cannot open param file. ") 
        elif ctype == 'incrf' or ctype == 'decrf':
          val = 1.0
          speedVal = 1.0
          paramFile = root + '/ParamBin*'
          solverFile = root + '/solver_stat*'
          auxFile = glob.glob(paramFile)
          auxFile2 = glob.glob(solverFile)
          if(len(auxFile) == 1 and len(auxFile2) == 1):
            found = False;
            paramDict = LoadParams(auxFile[0])
            if ctype == 'incrf':
              for item in paramDict: 
                if item.startswith('IncrFactor'):
                  val = float(paramDict[item])
                  found = True;
            else:
              for item in paramDict: 
                if item.startswith('DecrFactor'):
                  val = float(paramDict[item])
                  found = True;
            solverDict = LoadParams(auxFile2[0])
            found2 = False;
            if 'Computer Time' in solverDict:
              speedVal = float(solverDict['Computer Time'])
              found2 = True
            if not found: 
              print("Increment Factor not found. ") 
              print("Here is the dictionary. ")
              pprint(paramDict)
            if not found2:          
              print("Computer Time not found. ") 
              print("Here is the dictionary. ")
              pprint(solverDict)
            if found and found2:
              sortedList.append( (val,speedVal))
        else:
          sys.exit("ConvergeType not recognized.")

  if len(sortedList) == 0:
    errStr = "No data files matching " + fileName
    errStr += " were found in current directory or subdirectories. "
    sys.exit(errStr)
  sortedList = sorted(sortedList,key = itemgetter(0), reverse = True)
  errVec = []
  x = []
  for item in sortedList:
    if not math.isnan(item[1]):
      x.append(item[0])
      errVec.append(item[1])
  x = np.array(x)
  errVec = np.array(errVec)
  if len(x) < 1:
    errStr = "No good data. Quitting. " 
    sys.exit(errStr)

  if 'pval' in auxDict and ctype == 'cstep': 
    x = x/float(auxDict["pval"])
  print(errVec)
  return (x,errVec,auxDict)

def Converge2DH(fileName,yexact,ctype='cstep'):
  """
  Converge plots

  ConvergeH(fileName,yexact,type):
  Args:
    fileName: Name of data files to compare 
    e.g. X_1.dat
    
    yexact: Exact solution. Often can be best numerical solution
    type: Specifies the convergence type to be plotted.

      cstep (default): Step size vs. relative error. For constant step methods 
      speed :  Speed vs relative error. 
      relerr : Relative error tolerance vs. relative error. For adaptive step methods.
      stages : Runge-kutta stage speed vs. relative error.
      coeff :  ETD coefficient cost vs. relative error.
      incrf :  ETD increment floor vs. speed. For adaptive ETD methods.
      decrf :  ETD decrement ceiling vs. speed. For adaptive ETD methods.

  """

  x,y,auxDict = ConvergeData2D(fileName,yexact,ctype)
  width,height = ConvSize()
  fsize,margins = figsize_and_margins(plotsize=(width,height))
  labs = plt.get_figlabels() 
  if ctype == 'cstep':
    if "CSTEP" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("CSTEP",figsize=fsize)
    plt.xlabel('Relative time step')
    plt.ylabel('Relative error')
  elif ctype == 'speed':
    if "SPEED" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("SPEED",figsize=fsize)
    plt.xlabel('Computer time (s)')
    plt.ylabel('Relative error')
  elif ctype == 'relerr':
    if "RELERR" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("RELERR",figsize=fsize)
    plt.xlabel('Tolerance ($\epsilon_{rel}$)')
    plt.ylabel('Relative error')
  elif ctype == 'coeff':
    if "COEFF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("COEFF",figsize=fsize)
    plt.xlabel('ETD coefficient cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'stages':
    if "STAGES" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("STAGES",figsize=fsize)
    plt.xlabel('RK stage evaluation cost (s)')
    plt.ylabel('Relative error')
  elif ctype == 'incrf':
    if "INCRF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("INCRF",figsize=fsize)
    plt.xlabel('Expansion floor')
    plt.ylabel('Computer time (s)')

  elif ctype == 'decrf':
    if "DECRF" not in labs:
      configs.DefaultLS()
    else:
      configs.ToggleLS()
    plt.figure("DECRF",figsize=fsize)
    plt.xlabel('Compression ceiling')
    plt.ylabel('Computer time (s)')


  if ctype == 'cstep' or ctype == 'speed' or ctype == 'relerr' or ctype == 'coeff' or ctype == 'stages':
    plt.loglog(x,y,configs.LS,markersize=4)
    ax = plt.gca()
    #ax.xaxis.set_major_locator(ticker.LogLocator(numticks=6))
    #ax.yaxis.set_major_locator(ticker.LogLocator(numticks=6))
    ax.xaxis.set_major_locator(ticker.LogLocator(numdecs=6))
    ax.yaxis.set_major_locator(ticker.LogLocator(numdecs=6))
    ax.xaxis.grid(b =
        True,which='minor',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.xaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
    ax.yaxis.grid(b =
        True,which='major',linestyle=':',linewidth=0.1,dashes=(1,2))
  elif ctype == 'incrf' or ctype == 'decrf':
    plt.plot(x,y,configs.LS,markersize=4)

  plt.hold(True) 
  plt.ion()
  plt.show()





