"""baseline correction for each channel

slices=baseline.correct(slices)"""
from numpy import shape, mean



def correct(data):
    for ch in range(0,shape(data)[0]):
        dmean=mean(data[ch,:])
        data[ch,:]=data[ch,:]-dmean;
    return data
        
        
