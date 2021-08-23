
from graphdata import np

def ReadDatMetadata(file):
    metadata = dict()
    with open(file) as f:
        line = f.readline()
        while(line.startswith('#')):
            key,val = line.split(':')
            key = key[1:]
            # Remove whitespace and tabs
            key = ' '.join(key.split())
            val = ' '.join(val.split())
            metadata[key] = val
            line = f.readline()
    return metadata

def ReadDatFile1D(file):
    auxDict = ReadDatMetadata(file)
    with open(file,'rb') as f:
        data = np.genfromtxt(f,skip_header=len(auxDict))
    x = np.array(data[:,0]); y = np.array(data[:,1]);
    return (x,y,auxDict)

def ReadDatFile2D(file):
    auxDict = ReadDatMetadata(file)
    with open(file) as f:
        line = f.readline()
        while(line.startswith('#')):
            line = f.readline()
        nD1,nD2 = line.split()
        nD1,nD2 = int(nD1), int(nD2)
        x,y = [], []
        for i in range(nD1):
            x.append(float(f.readline()))
        for i in range(nD2):
            y.append(float(f.readline()))
        x,y = np.array(x), np.array(y)
        z = np.genfromtxt(f)

    try:
        shape = (nD1,nD2)
        z = z.reshape(shape)
    except:
        shape = (2*nD1,nD2)
        zfull = z.reshape(shape)
        z = np.array(zfull[:nD1,:] + 1j*zfull[nD1:],dtype=np.complex128)
    return (x,y,z,auxDict)



