    
    
from numpy import complex_, zeros, size, log10
from meg import spectral
from pylab import matplotlib, window_hanning
from pylab import figure,plot,show
from pdf2py import data, channel

def psd(datapdf):
    d = data.read(datapdf)
    nfft=256*2
    ch = channel.index(datapdf, 'meg')
    d.getdata(0, d.pnts_in_file, ch.channelindexhdr)
    data2anz = d.data_block
    #data2anz = result['attenddata']
    pow = zeros([(nfft/2)+1, size(data2anz,1)])
    comp = zeros([(nfft/2)+1, size(data2anz,1)], complex_)
    #fftreal = (zeros([(nfft/2)+1, size(attenddata,1)]))

    for eachch in range(0, size(data2anz,1)):
        p,f,i = spectral.psd(data2anz[:,eachch], NFFT=nfft, Fs=1/ d.hdr.header_data.sample_period)#, noverlap=200)#, detrend=matplotlib.pylab.detrend_mean)
        #p,f,i = spectral.psd(data[:,eachch], NFFT=nfft, Fs=1/ d.hdr.header_data.sample_period )
        pow[:,eachch] = p
        comp[:,eachch] = i
        #fftreal[:,eachch] = r
    logpow = 10*log10(pow)
    freq=f
    return logpow, freq


