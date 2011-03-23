#       lA2array.py
#
#       Copyright 2010 dan collins <danc@badbytes.net>
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

'''lA dipole conversion to diparray'''


from pdf2py import channel,data
from numpy import nonzero, zeros, size, shape, tile

def getderivedlabels(datafile):
    ch = channel.index(datafile, 'derived')
    chdict = {}
    for i in ch.chnumber:
        chdict[ch.cfgchname[ch.cfgchannumber == i][0]] = i

    return ch, chdict

def getnonzerosind(datafile, chdict, ch):
    d = data.read(datafile)
    d.getdata(0, d.pnts_in_file, ch.chindex)

    gofdata = d.data_block[:,ch.chnumber == chdict['GoF']]; #use the GOF channel, as if it is zero there shouldn't be any dipole at this point
    ind = nonzero(gofdata[:,0])
    return ind, d

def formatdata(d, chdict, ind, ch):
    #for i in range(0, len(chdict)):
    diparray = zeros([size(ind),len(chdict)+1])
    #print shape(diparray), d.eventtime, ind
    labels = ['x pos','y pos','z pos','Qx','Qy','Qz','Radius','||Q||','Rms','Correlation','GoF','Iter']
    diparray[:,0] = tile(d.eventtime,d.numofepochs)[ind] #time

    for i in range(0, size(labels)):
        diparray[:,i+1] = d.data_block[ind, ch.chnumber == chdict[labels[i]]]

    labels.insert(0,'time')
    return diparray, labels



class calc:
    def __init__(self, datafile):
        [ch,chdict] = getderivedlabels(datafile)
        [ind, d] = getnonzerosind(datafile, chdict, ch)
        [self.dips,self.labels] = formatdata(d, chdict, ind, ch)
        self.d = d
        self.ch = ch
        self.chdict = chdict
        self.ind = ind
