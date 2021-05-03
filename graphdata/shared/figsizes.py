
from graphdata import configs 

def PlotSize(figsize=None):
    if figsize is not None: 
        return figsize
    return (float(configs._G['PlotWidth']),float(configs._G['PlotHeight']))

def SemilogySize(figsize=None):
    if figsize is not None: 
        return figsize
    return (float(configs._G['SemilogyWidth']),float(configs._G['SemilogyHeight']))

def LogLogSize(figsize=None):
    if figsize is not None: 
        return figsize
    return (float(configs._G['LogLogWidth']),float(configs._G['LogLogHeight']))




