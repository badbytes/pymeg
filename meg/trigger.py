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


'''get triggers onsets and returns indices for all zero to non-zero transitions.

u,n,nz = trigger.vals(p.data.data_block);
where u are unique values in data, n are nonzero indicies and nz is the value at n.

t = trigger.zero_to_nonzero_ind(p.data.data_block,u[1]);
returns t, the indices to value u where the transition is from zero to u.

'''

import numpy as np

def zero_to_nonzero_ind(data, val):
    if len(np.shape(data)) > 1: #assume channel is second dim
        f = np.roll(data,1,axis=0)
        z2nz = data-f
        out = np.argwhere(z2nz == val).T[0]
        return out

def vals(data):
    '''returns values,indices for all zero to non-zero transitions
    u,n,nz = trigger.vals(t.data_block)'''
    nzind = data.nonzero()[0] #non-zero indices
    nz=data[data.nonzero()] #non-zero values
    uvals = np.unique(nz) #unique non-zero values
    return uvals,nzind,nz

def ind(uvals, nzind, nz, includefirstpointhigh=True):
    ''' return indices of specific value code on channel.
    ind = trigger.ind(200,nzind,nz) #value 200'''
    tind = []
    for u in uvals:
        if type(u) == unicode:
            print 'decoding'
            t = nzind[nz == eval(u)[0]]
        else:
            t = nzind[nz == u]

        '''t equals indicies to a value. ex all the indices to value bit == 100'''

        val = t[0];

        for i in t: #for each indice in
            if includefirstpointhigh == True:
                if i - val == 0: #get first
                    tind.append(i)
            if i - val > 1:
                tind.append(i)
                #print i,val, i-val
            val = i

    return np.array(tind),t

def event_detection(data, sample_period, selectwin, slidingwin, thresh):
    '''use external channel with sliding window and threshold to create ind
    t = trigger.external(data, sample_period, 1.5, .05, .3)
    #returns the indices (t)
    data = t.data.data_block[:,0]
    sample_period = t.hdr.header_data.sample_period
    window size 1.5 sec
    for a sliding window of 50 msec
    and a threshold of .3 V'''

    s = np.sqrt(np.square(data)) #make positive
    win = int((1 / sample_period) * selectwin) #get ind for selction window
    indslid = int((1 / sample_period) * slidingwin) #get ind for slidingwin
    lastind = indslid*np.floor(len(data)/np.float(indslid))
    print 'params',s,win,indslid,lastind

    t = np.where(s>thresh+s.min())[0] #reduce computation by picking points that could qualify.
    print t.shape
    tind = []
    a = 0
    val = t[0] #starting val
    looping = True
    while looping == True:
        indx = val-indslid #step back from ind to start the peak-peak sliding window.
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


