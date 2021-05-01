from graphdata import plt
from graphdata.evolve import Evolve
from graphdata.shared.shared import GenMovie

def EvolveR(*args,**kwargs):

# view = [elev,azim]
  numFiles = 6
  if len(args) > 2:
    numFiles = args[2]
  incr = 360/numFiles

  elev = 57
  if 'view' in kwargs:
    view = kwargs['view']
    elev = view[0]
    del kwargs['view']

  if 'elev' in kwargs:
    elev = kwargs['elev']

  kwargs['view'] = [elev,incr]
  ax = Evolve(*args,**kwargs)
  ax.axis('off')
  ax.view_init(elev,0)
  ax.set_title('view = (' + str(elev) + ',0)')
  plt.draw()
  plt.savefig('EvolveR_0.png')
  imageList = ['EvolveR_0.png']

  for angle in range(incr,360,incr):
    ax.view_init(elev,angle)
    ax.set_title('view = (' + str(elev) + ',' + str(angle) + ')')
    plt.draw()
    imageFile = 'EvolveR_' + str(angle) + '.png'
    plt.savefig(imageFile)
    imageList.append(imageFile)

  movLength = MovLength(**kwargs)
  GenMovie(imageList,'EvolveR',movLength)


def EvolveM(*args,**kwargs):
  fileList = GenFileList(*args)
  plotArgs = args[2:]
  fileLen = len(fileList)
  count = 0
  auxDict = dict() 
  x = []
  num = 0
  for file in fileList:
    auxDict = ProcessAux(file) 
    if "pscale" in auxDict: 
      if(configs._G["scale"] == 'nonDim'):
        x.append(float(auxDict['pval'])/float(auxDict['pscale']))
      elif(configs._G["scale"] == 'dimscale'):
        x.append(float(auxDict['pval'])/float(configs._G['pdimscale']))
      elif(configs._G["scale"] == 'noscale'):
        x.append(float(auxDict['pval']))
    else:
      x.append(num)
      num = num + 1

  fileID,repNum = GetDataFileInfo(fileList[0]) 
  y,z,auxDict = GetData1D(fileID,repNum)
  y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
  y,z = ProcessEvolvePoints(y,z,60)

  if len(args) > 3:
    view = args[3]  
    if len(view) > 0:
      auxDict['angle1'] = view[0]
    if len(view) > 1:
      auxDict['angle2'] = view[1]

  count = 0; 
  Z = np.zeros((len(x),len(y)))
  for file in fileList:
    fileID,repNum = GetDataFileInfo(file) 
    y,z,auxDict = GetData1D(fileID,repNum)
    y,z,auxDict = ProcessData1D(y,z,auxDict,**kwargs)
    y,z = ProcessEvolvePoints(y,z,60)
    Z[count,:] = z 
    count = count + 1

  X,Y = np.meshgrid(y,x)

  width = float(configs._G['EvolveWidth'])
  height = float(configs._G['EvolveHeight'])
  fig = plt.figure(figsize=(width,height))
  fig.clf()
  ax = fig.add_subplot(1,1,1,projection = '3d')
  wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1,color='black')
  plt.xlim([x[0],x[-1]])
  AuxSurfaceLabel(ax,auxDict)
  plt.ion()
  plt.show()
  return True


