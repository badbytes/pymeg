'''Function to read data stream off the MAS storage device'''

# Copyright 2008 Dan Collins
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



try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
import time
import os
from numpy import append, reshape, zeros, shape, floor
from pdf2py import channel, trigdet
#from pdf2py.data import config  #commented out 090324 for fixing error
from pdf2py.data import read


class getdata:
    def __init__(self, datapdf):
        '''open data'''

        self.timelist=[]

        while os.path.isfile(datapdf)==False:
            try:
                check
            except NameError:
                check = 1; limit=5
            if check==1: print 'file not in existence... rechecking for ', limit, ' seconds'
            time.sleep(1)
            check=check+1
            if check==limit:
                    print 'file not found...giving up'
                    return
        else:
            self.timelist.append(time.time()) #check time
            print 'reading pdf', os.path.abspath(datapdf)
            self.fid=open(datapdf, 'r')

class chunk(getdata):
    def setparams(self, datatemplate, trig=None): #since header written at end, need to provide data template of same acquisiiton
        '''c=chunk(datapdf)
        c.setparams(datatemplate,trigchannel)
        ex. c.setparams(datafilename, 'TRIGGER')   or 'RESPONSE'
        '''
        self.trig=trig
        if self.trig==None:
            print 'no triggers will be detected, so no realtime averaging and such'
        else:
            print 'setting detection of channel',self.trig

        #for debugging using fidpos as positions to seek in file

        #090324 fix
        conf = read(datatemplate)
        #conf=config(datatemplate)

        self.step=conf.time_slice_size
        self.numch=conf.total_chans
        self.dataprecision=conf.dataprecision
        '''set data parameters'''
        print 'test'
        self.timelist.append(time.time())
        self.data_blockall=zeros((1,self.numch))
    def getchunk(self, channelinstance):#, fidpos):
        '''c.getchunk(channelinstance)'''
        print 'get chunk'
        marker=self.fid.tell(); print 'marker ', marker
        gotoend=self.fid.seek(0, os.SEEK_END)
        #gotoend=self.fid.seek(fidpos, os.SEEK_SET) #****************************FOR DEBUGGING *******************************************
        endpos=self.fid.tell(); print 'end pos ', endpos
        self.chunk=int(floor((endpos-marker)/self.step)); print 'chunk ',self.chunk
        self.timelist.append(time.time())

        #if no more chunks of ok size
        trys=0
        while endpos-marker<self.step:
            print endpos, self.fid.tell()
            print 'end of file. trying to read again'

            time.sleep(2) #pause 100ms
            trys=trys+1
            gotoend=self.fid.seek(0, os.SEEK_END)
            #gotoend=self.fid.seek(fidpos, os.SEEK_SET) #****************************FOR DEBUGGING *******************************************
            endpos=self.fid.tell(); print 'end pos ', endpos
            self.chunk=int(floor((endpos-marker)/self.step)); print 'chunk ',self.chunk
            if trys==10:
                print 'giving up';
                print 'reseting marker to start =',marker;
                self.fid.seek(marker, os.SEEK_SET)
                return

        self.fid.seek(marker, os.SEEK_SET)
        data_chunk = fread(self.fid, self.chunk*self.numch, self.dataprecision, self.dataprecision, 1);
        print 'data size ', shape(data_chunk)
        print 'new position ', self.fid.tell()

        #catch error chunks
        while shape(data_chunk)[0] != self.chunk*self.numch:
            print 'error detected, rereading file'
            gotoend=self.fid.seek(0, os.SEEK_END)
            #gotoend=self.fid.seek(fidpos, os.SEEK_SET) #****************************FOR DEBUGGING *******************************************

            endpos=self.fid.tell()
            self.fid.seek(marker, os.SEEK_SET); print 'reseting to ', self.fid.tell()
            self.chunk=int(floor((endpos-marker)/self.step)); print 'chunk ',self.chunk
            data_chunk = fread(self.fid, self.chunk*self.numch, self.dataprecision, self.dataprecision, 1);
            time.sleep(.1)

        data_block=data_chunk.reshape([shape(data_chunk)[0]/self.numch,self.numch])
        print shape(data_block)

        print 'detecting triggers'
        #print 'iiiii',self.trig
        if self.trig!=None:
            print 'finding indicies'
            print shape(data_block), channelinstance, self.trig
            #self.trigind=trigdet.get(data_block, channelinstance, 'RESPONSE')
            self.trigind=trigdet.get(data_block, channelinstance, self.trig)

        data_blocksorted = data_block[:,channelinstance.sortedindtype]
        self.data_blockall=data_blocksorted
        print 'shape of data',shape(self.data_blockall)








