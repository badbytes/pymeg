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
    '''
    fftd = fftmeg.calc(p.data.data_block,1/ p.hdr.header_data.sample_period, epochs=p.data.numofepochs)'''
    def __init__(self,data, srate, epochs=1):
        ts = time();
        pnts = size(data,0)/epochs
        print 'fft pnts per epoch',pnts
        print 'number of epochs = ',epochs
        t = linspace(0,pnts/srate,pnts ); # time in seconds

        #t = t[:-1]
        Fs=srate;
        T=1/Fs;

        L=len(t);
        NFFT = int(2**ceil(log2(abs(L))))
        f = Fs/2*linspace(0, 1,NFFT/2);

        if len(shape(data)) == 1: #its a 1D vector, make 2D
            data = array([data]).T

        pow = zeros([size(f),size(data,1)]); #create empty power array. Freq X Ch
        powc = zeros([size(f),size(data,1)]);
        comp = zeros([size(f),size(data,1)], complex_);
        ipow = zeros([size(f),size(data,1)]);#, complex_);

        if size(data) > 4000000:
            print 'lots of pnts. might crash you sys.'
            print 'going to take care of that for you'

        div = int(ceil(size(data)/4000000.0))

        print 'number of channel groups',div
        chgrp = (size(data,1)/div)
        print 'debug',div,pnts,chgrp,NFFT
        for g in range(0, div):
            print g,'of', div

            for e in range(0,epochs):
                Yi = fft(data[e*pnts:(e+1)*pnts,g*chgrp:(g+1)*chgrp],n=NFFT, axis=0)/L;
                pow[:,g*chgrp:(g+1)*chgrp] = pow[:,g*chgrp:(g+1)*chgrp] + abs(Yi[0:NFFT/2]*2)
                powc[:,g*chgrp:(g+1)*chgrp] = powc[:,g*chgrp:(g+1)*chgrp] +  conjugate(Yi[0:NFFT/2]*2) * (Yi[0:NFFT/2]*2)
                comp[:,g*chgrp:(g+1)*chgrp] = comp[:,g*chgrp:(g+1)*chgrp] + (Yi[0:NFFT/2]*2)
                ipow[:,g*chgrp:(g+1)*chgrp] = pow[:,g*chgrp:(g+1)*chgrp] + imag(Yi[0:NFFT/2]*2)


                if g == div-1: #last few channels
                    #print 'last group'
                    Yi = fft(data[e*pnts:(e+1)*pnts,g*chgrp:],n=NFFT, axis=0)/L;
                    pow[:,g*chgrp:] = pow[:,g*chgrp:] + abs(Yi[0:NFFT/2]*2)
                    powc[:,g*chgrp:(g+1)*chgrp] = powc[:,g*chgrp:] +  conjugate(Yi[0:NFFT/2]*2) * (Yi[0:NFFT/2]*2)
                    comp[:,g*chgrp:] = comp[:,g*chgrp:] + (Yi[0:NFFT/2]*2)

        print 'number of channels processed',size(data,1)
        te = time() - ts
        print 'time elapsed', te, 'sec'
        if epochs > 1: print 'calculating mean power across epochs'
        self.pow = pow/epochs
        self.freq = f
        self.comp = comp
        self.powc = powc
        self.ipow = ipow
        self.Yi = Yi

        #return pow,f
    def ch2keep(self, ch2keep):
        self.pow = self.pow[:,ch2keep]


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
