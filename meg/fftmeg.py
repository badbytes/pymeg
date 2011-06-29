# Copyright 2008-2009 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


'''#returns fft power by freq
pow,freq = fftmeg.calc(data,srate)
#or
fftd = fftmeg.calc(p.data.data_block,1/ p.hdr.header_data.sample_period, epochs=p.data.numofepochs)
'''

from numpy import linspace, shape, size, ceil, log2, zeros, mean, append, complex_, conjugate, imag
from numpy.fft import *
#from scipy import fft
from pylab import figure,plot,show, array
from time import time

class calc():
    '''fftd = fftmeg.calc(p.data.data_block,1/ p.hdr.header_data.sample_period, epochs=p.data.numofepochs)'''
    def __init__(self,data, srate, epochs, axis=0):
        ts = time();
        pnts = size(data,0)/epochs
        print 'fft pnts per epoch',pnts
        print 'number of epochs = ',epochs
        t = linspace(0,pnts/srate,pnts ); # time in seconds
        Fs=srate;
        T=1/Fs;
        L=len(t);
        NFFT = int(2**ceil(log2(abs(L))))
        f = Fs/2*linspace(0, 1,NFFT/2);
        print 'NFFT', NFFT

        if len(shape(data)) == 1: #its a 1D vector, make 2D
            data = array([data]).T

        self.Yi = Yi = fft(data,n=NFFT, axis=axis)/L;
        self.pow =  abs(Yi[0:NFFT/2]*2)
        self.powc = conjugate(Yi[0:NFFT/2]*2) * (Yi[0:NFFT/2]*2)
        self.comp = (Yi[0:NFFT/2]*2)
        self.ipow = imag(Yi[0:NFFT/2]*2)
        self.freq = f


def nearest(array, target):
    '''ind = fftmeg.nearest(freqlist, 40)'''
    ind = []

    for i in range(0,size(target)):
        if type(target) != list:
            target = [target]
        targetint = float(target[i])
        x=list(abs(array-targetint))
        ind = append(ind,x.index(abs(array-targetint).min()))
    ind = ind.tolist()
    return ind

#~ if __name__ == "__main__":
    #~ calc()
