#from pdf2py import pdf
'''makesine.create(pnts, srate, freq):'''
from numpy import dot, ceil, log2, abs, array, sin, pi, arange, float

def __run__(pnts, srate, freq):
    s = create(pnts, srate, freq)
    return s

def nextpow2(n):
    f = ceil(log2(abs(n)));
    p = f-1;
    return p


def create(pnts, srate, freq):
    pnts = float(pnts)
    t = arange(0,(pnts/srate),(pnts/srate)/pnts)#; % time in seconds
    somefreqhz = array([sin(dot(dot(2,pi),dot(freq,t)))/2]) #%make sine wave
    return somefreqhz.T

if __name__ == '__main__':
    s = create(1000, 200, 10)
    print s
