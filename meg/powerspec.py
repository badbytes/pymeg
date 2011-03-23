#!/usr/bin/env python
# python

# Copyright 2008 Dan Collins

# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from pylab import *
from msiread import getposted
from numpy import transpose, shape

pdf = getposted.read()
dt = 1/pdf.sample_rate
#t = arange(0,pdf.n_slices,dt)
t = arange(0,pdf.n_slices/pdf.sample_rate, dt)

def calc(data):#, data2, data3):
    f=figure()
    subplot(311)
    plot(t,data.transpose())
    print data.shape[0]
    for ch in range(data.shape[0]):
        print ch
        subplot(312)
        psd(data[ch,:], 512, 1/dt)
        subplot(313)
        specgram(data[ch,:], 512, 1/dt)
        
    subplot(312)
    legend((str(range(data.shape[0]))))
    show()
    
if __name__ == "__main__":
    #data= pdf.GetSliceRangeMEGChannels(0, pdf.n_slices)
    data= pdf.GetSliceRangeReferenceChannels(0, pdf.n_slices)
    #data=data[1,:]
    calc(data)
    

    