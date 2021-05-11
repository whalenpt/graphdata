
import json
from graphdata import np

def ReadJSONFile(file):
    with open(file) as f:
        data = json.load(f)
    return data

def ReadJSONMetadata(file):
    with open(file) as f:
        data = json.load(f)
    metadata = dict()
    for key,val in data.items():
        if not isinstance(val,list):
            metadata[key] = val
    return metadata

def ReadJSONFile1D(file):
    data = ReadJSONFile(file)
    try:
        xlabel = data['xlabel']
        ylabel = data['ylabel']
        x = np.array(data[xlabel])
        y = np.array(data[ylabel])
        del data[xlabel]
        del data[ylabel]
        return (x,y,data)
    except:
        pass
    try:
        x = np.array(data['x'])
        y = np.array(data['y'])
        del data['x']
        del data['y']
        return (x,y,data)
    except:
        raise Exception('Failed to parse JSON file data')
        

def ReadJSONFile2D(file):
    data = ReadJSONFile(file)
    try:
        xlabel = data['xlabel']
        ylabel = data['ylabel']
        zlabel = data['zlabel']
        x = np.array(data[xlabel])
        y = np.array(data[ylabel])
        z = np.array(data[zlabel])
        del data[xlabel]
        del data[ylabel]
        del data[zlabel]
        return (x,y,z,data)
    except:
        pass
    try:
        x = np.array(data['x'])
        y = np.array(data['y'])
        z = np.array(data['z'])
        del data['x']
        del data['y']
        del data['z']
        return (x,y,z,data)
    except:
        raise Exception('Failed to parse JSON file data')
        





