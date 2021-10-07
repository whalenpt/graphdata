
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
    with open(file) as f:
        data = np.genfromtxt(f,skip_header=len(auxDict))
    rows,cols = data.shape
    if cols == 2:
        x = np.array(data[:,0]); y = np.array(data[:,1]);
        return (x,y,auxDict)
    elif cols == 3:
        x = np.array(data[:,0]); 
        yreal = np.array(data[:,1]);
        yimag = np.array(data[:,2]);
        ycmplx = np.array(yreal + 1j*yimag,dtype=np.complex128)
        return (x,ycmplx,auxDict)
    else:
        raise RuntimeError(\
                'Failed to read the data file {}: is not in a DAT file format'.format(file))


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

    rows,cols = z.shape
    if cols == nD2:
        return (x,y,z,auxDict)
    elif cols == 2*nD2:
        zcmplx = np.array(z[:,::2] + 1j*z[:,1::2],dtype=np.complex128)
        return (x,y,zcmplx,auxDict)
    else:
        raise RuntimeError(\
                'Failed to read the data file {}: is not in a DAT file format'.format(file))



