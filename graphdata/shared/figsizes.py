
from graphdata import configs 

def PlotSize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['PlotWidth']),float(configs._G['PlotHeight']))

def SemilogySize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['SemilogyWidth']),float(configs._G['SemilogyHeight']))

def LogLogSize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['LogLogWidth']),float(configs._G['LogLogHeight']))

def SurfaceSize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['SurfaceWidth']),float(configs._G['SurfaceHeight']))

def ContourfSize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['ContourfWidth']),float(configs._G['ContourfHeight']))


def WaterfallSize(figsize):
    if figsize is not None: 
        return figsize
    return (float(configs._G['WaterfallWidth']),float(configs._G['WaterfallHeight']))



