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


'''get triggers onsets and returns indices for all zero to non-zero transitions.'''

#from scipy import *
import numpy as np
#from numpy import *


def vals(data):
    '''returns values,indices for all zero to non-zero transitions
    u,n,nz = trigger.vals(t.data_block)'''
    nzind = data.nonzero()[0]
    nz=data[data.nonzero()]
    uvals = np.unique(nz)
    return uvals,nzind,nz 
    
def ind(uvals, nzind, nz):
    ''' return indices of specific value code on channel.
    ind = trigger.ind(200,n,nz) #value 200'''
    tind = []
    for u in uvals:
        if type(u) == unicode:
            print 'decoding'
            t = nzind[nz == eval(u)[0]]
        else:
            t = nzind[nz == u]

        val = t[0];
        
        for i in t:
            if i - val == 0:
                tind.append(i)
            #if i - val == 1:
            #    pass
            if i-val > 1:
                tind.append(i)
            val = i
        
    return np.array(tind)
    
def external(data, sample_period, selectwin, slidingwin, thresh):
    '''use external channel with sliding window and threshold to create ind
    t = trigger.external(data, sample_period, 1.5, .05, .3)
    #returns the indices (t) 
    data = t.data.data_block[:,0]
    sample_period = t.hdr.header_data.sample_period
    window size 1.5 sec
    for a sliding window of 50 msec
    and a threshold of .3 V'''
    
    s = np.sqrt(np.square(data)) #make positive
    
    #win = np.where(eventtime < selectwin)[0][-1] #get ind for selction window
    win = int((1 / sample_period) * selectwin) #get ind for selction window
    #print win, win*sample_period
    
    #indslid = np.where(eventtime < slidingwin)[0][-1] #get ind for slidingwin
    indslid = int((1 / sample_period) * slidingwin) #get ind for slidingwin
    
    lastind = indslid*np.floor(len(data)/np.float(indslid))
    
    t = np.where(s>thresh+s.min())[0] #reduce computation by picking points that could qualify.
    tind = []
    a = 0
    val = t[0] #starting val
    #print 'starting index',val
    looping = True
    while looping == True:
        indx = val-indslid #step back from ind to start the peak-peak sliding window.
        #print indx
        stopindx = indx + win #create a stop point to keep the sliding window for going on forever
        while indx < stopindx:
            mini = min(s[indx:indx+indslid])
            maxi = max(s[indx:indx+indslid])
            if maxi - mini > thresh:
                tind.append(indx)
                indx = stopindx #stop this iteration, move on to next win
             
            indx = indx + 1 #slide to next index
        
        a = a + 1
        print 'event', a, 'detected'

        try:
            val = t[np.where(t > indx)[0][0]] #get ind for the next window
        except IndexError:
            looping == False
            return tind
            

