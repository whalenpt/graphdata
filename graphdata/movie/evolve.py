from graphdata import plt
from graphdata.evolve import Evolve
from graphdata.shared.shared import GenMovie

def EvolveMovie(*args,**kwargs):

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




