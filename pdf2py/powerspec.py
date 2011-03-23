from pylab import *
from numpy import transpose, shape
from pdf2py import pdf


##p = pdf.read()
##dt = 1/pdf.sample_rate
###t = arange(0,pdf.n_slices,dt)
##t = arange(0,pdf.n_slices/pdf.sample_rate, dt)

def calc(data, pdfobj):#, data2, data3):
    dt = pdfobj.hdr.header_data.sample_period
    t = arange(0,shape(data)[0]/(1/pdfobj.hdr.header_data.sample_period), dt)
    NFFT=512
    print shape(t), dt
    #return
    f=figure()
    subplot(311)
    plot(data)
    print data.shape[1]
    for ch in range(data.shape[1]):
        #print ch
        subplot(312)
        psd(data[:,ch], NFFT, 1/dt)
        subplot(313)
        #specgram(data[:,ch], NFFT, 1/dt)
        #specgram(data[:,ch], NFFT, 1/dt, Fc=0, detrend=mlab.detrend_none,
        #     window = mlab.window_hanning, noverlap=128,
        #     cmap=None, xextent=None)
        
    #subplot(312)
    #legend((str(range(data.shape[0]))))
    show()
    
if __name__ == "__main__":
    #data= pdf.GetSliceRangeMEGChannels(0, pdf.n_slices)
    data= pdf.GetSliceRangeReferenceChannels(0, pdf.n_slices)
    #data=data[1,:]
    calc(data)
    