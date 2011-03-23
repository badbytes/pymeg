#from pdf2py import pdf
'''makesine.create(pnts, srate, freq):'''
from numpy import dot, ceil, log2, abs, array, sin, pi, arange, float

    #p=pdf.read('/home/danc/python/data/e,rfhp1.0Hz,COH')
    #srate = 1/p.hdr.header_data.sample_period

def __run__(pnts, srate, freq):
    s = create(pnts, srate, freq)
    return s

def nextpow2(n):
##    if size(n) > 1:
##        #n = cast(length(n),class(n));

    f = ceil(log2(abs(n)));
    p = f-1;
    return p

    #% Check for infinities and NaNs
    #k = ~isfinite(f);
    #p(k) = f(k);

def create(pnts, srate, freq):
    pnts = float(pnts)
    t = arange(0,(pnts/srate),(pnts/srate)/pnts)#; % time in seconds
    #t = t[1:-1];
    #%freq=10; %frequency
    somefreqhz = array([sin(dot(dot(2,pi),dot(freq,t)))/2]) #%make sine wave
    return somefreqhz.T
'''
    Fs=srate;
    T=1.0/Fs;
    L=size(t);
    p=nextpow2(L);
    NFFT = 2**p
    
    Y = fft(somefreqhz,n=NFFT)/L;
    f = Fs/dot(2,linspace(0,1,NFFT/2))
    
    
    #figure;plot(f,2*abs(Y(1:NFFT/2))) ;
    #keyboard


    #Y = fft(EEG.data(:,:,:),NFFT)/L;'''
    
if __name__ == '__main__':
    s = create(1000, 200, 10)
    print s
