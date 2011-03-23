#       event_logic.py
#
#       Copyright 2011 danc <danc@badbytes.net>
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

from numpy import *
from meg import trigger
from meg.nearest import nearest


def get_ind(triggervals, data):
    u,n,nz = trigger.vals(data)
    ind = {}
    for i in range(0,len(triggervals)):
        ind[i] = trigger.ind([triggervals[i]],n,nz)
    return ind

#ind_dict = {0:array([0,10,20,300,350]),1:array([2,11,22,290,345,370])}
#timediff = 100

def ind_logic(ind_dict, timediff, timeseries):
    result_ind = []
    ts = timeseries
    for i in range(0,len(ind_dict.keys())):
        if i == 0:
            result_ind = ind_dict[0]
        else:
            print('cur key num',i)
            prime_timeind = ts[ind_dict[0]] #first ind array
            second_timeind = ts[ind_dict[i]] #every ind array including first
            nind = nearest(prime_timeind,second_timeind)
            for j in nind:
                n1 = ts[prime_timeind[j]]
                try: n2 = ts[second_timeind[j]]
                except IndexError: print('Error, so bailing');return unique(result_ind)
                c = 0
                while n2 < n1: #look for second trigger to be equal or later than first
                    c = c + 1
                    n2 = ts[second_timeind[j+c]] #make sure n2 index is after n1 and not just the closest.

                    print 'looking at next ind'
                if (timeseries[n2] - timeseries[n1]) <= timediff:
                    #print 'adding', j
                    result_ind.append(j)

    return unique(result_ind)






