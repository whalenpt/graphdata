
from graphdata import np 
from graphdata.shared.shared import ProcessAux, SortNumericStringList,fmtcols
import glob
import os 
import sys 

def LoadData3D(file):
  fileList = glob.glob(file)
  if len(fileList) == 0:
    print('No files detected: ') 
    print('Files in directory are: ')
    dirFiles = os.listdir('.')
    dirFiles = SortNumericStringList(dirFiles)
    print(fmtcols(dirFiles,1))
    sys.exit()

  auxDict = ProcessAux(file) 
  with open(file) as f:
    line = f.readline()
    while(line.startswith('#')):
      line = f.readline()
    nD1,nD2,nD3 = line.split()
    nD1 = int(nD1)
    nD2 = int(nD2)
    nD3 = int(nD3)
    x1 = []
    x2 = []
    x3 = []
    for i in range(nD1):
      x1.append(float(f.readline()))
    for i in range(nD2):
      x2.append(float(f.readline()))
    for i in range(nD3):
      x3.append(float(f.readline()))
    x1 = np.array(x1)
    x2 = np.array(x2)
    x3 = np.array(x3)
    z = np.genfromtxt(f)
    shape = (nD1,nD2,nD3)
    z = z.reshape(shape)
  return (x1,x2,x3,z,auxDict)



