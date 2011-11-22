#       badchannels_v2.py
#
#       Copyright 2011 dan collins <danc@badbytes.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


'''initialize badchannel class
    p = pdf.read('/path2data/e,rfhp1.0Hz,COH')
    b = badchannels_v2.initialize(hz_range=[4,50])
get the fft correlation coefficients from each channel and a family of channels within 25mm of that channel
    b.builder(p,distance=25)
    #then take a look at b.correl'''

from meg import euclid
from numpy import median,corrcoef

class initialize():
    def __init__(self, method='fft',comparison='proximity',hz_range=[4,50]):
        '''method can be fft
        neighboring channel pickup can be based on 'proximity' or 'neighbors'
        eg
        b = badchannels_v2.initialize(method='fft',comparison='proximity')'''

        self.method = method
        self.comparison = comparison
        self.hz_range = hz_range
        print 'Using method of family channel comparison based on:',comparison, 'using', self.method, ',within freq range of', hz_range

    def fft_method(self, data, srate, epochs):
        from meg import fftmeg,nearest
        '''fftmeg.calc(p.data.data_block, p.data.srate,epochs=p.data.numofepochs)'''
        fftout = fftmeg.calc(data, srate,epochs=epochs)
        cut_low = nearest.nearest(fftout.freq,self.hz_range[0])[0]
        cut_high = nearest.nearest(fftout.freq,self.hz_range[1])[0]
        self.result = fftout.pow[cut_low:cut_high]

    def proximity(self, channel_pos, distance_in_mm, picktype='median'):
        proxind = euclid.get_proximity(channel_pos,channel_pos,distance_in_mm);
        return proxind

    def builder(self, pdfobj, distance=None, neighbors=None):
        '''initialize badchannel class
            b = badchannels_v2.initialize()
            #get the fft correlation coefficients from each channel and a family of channels within 25mm of that channel
            b.builder(p,distance=25)'''

        if distance == None and neighbors == None:
            print 'Error. You need to specify either distance=mm or number of neighbors (int)'
            raise NameError('You need to specify either distance or neighbors. ex distance=20 or neighbors=5 for 20mm or 5 neighbor channels used')

        if self.method == 'fft':# and self.comparison == 'proximity':
            print 'Using method fft'
            self.fft_method(pdfobj.data.data_block,pdfobj.data.srate, epochs=pdfobj.data.numofepochs)

        if self.method == 'cross_correl':
            self.result = pdfobj.data.data_block

        if self.comparison == 'proximity':
            self.proxind = self.proximity(pdfobj.data.channels.chlpos,distance)
            cc = {}; self.correlation_coef = []
            for i in self.proxind.keys():
                m = median(self.result[:,self.proxind[i]],axis=1)
                cc[i] = corrcoef(self.result[:,i],m)[0,1]
                self.correlation_coef.append(cc[i])

if __name__=='__main__':
    pass
