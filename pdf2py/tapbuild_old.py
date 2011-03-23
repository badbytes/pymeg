'''Use tap function to build data in loop'''
'''f='/mnt/nfs/comeg2/0611/tap/01%01%01@01:01/1/c,rfDC'
ch=channel.index(f, 'ext')
t=tapbuild.get(f,f)
t.avg(700, ch)'''

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



import time
from numpy import shape, average, array, append, any, zeros
from pdf2py import tap, trigdet

class config:
    def __init__(self, datapdf, datatemplate):
        self.datapiece=tap.chunk(datapdf) #initialize datafile
        self.datapiece.setparams(datatemplate) #initialize parameters
        
class get(config):
    def avg(self, epochwidth, channelinstance):
        '''average data'''
        '''epochwidth is the number of samples/epoch'''
        #condition1 = no trigger and no buffer => do nothing, data is crap
        #condition2= trigger+data. average data with enough data and buffer the rest if necessary. 
        #     then prepend data and trigger of buffer to incomming next data slice
        
        x=0
        while x < 20: #loops
            print x
            self.datapiece.getchunk(channelinstance); #get data segment
            #tmp=self.datapiece
            try:
                self.datapiece.data_blockall
                #tmp.data_blockall
            except AttributeError:
                pass
                #cant find data
            else:
                #ok
                
                print 'shape if incoming data', shape(self.datapiece.data_blockall)
                print 'fid-tell',self.datapiece.fid.tell()
                try:
                    bufferdata #look for buffer var
                except NameError:
                    pass #nothing buffered
                else: #something buffered, prepend to incomming data
                    print 'prepending. New shape should be ',shape(self.datapiece.data_blockall), '+', shape(bufferdata)
                    self.datapiece.data_blockall=append(bufferdata, self.datapiece.data_blockall) #prepended data
                    
                    #for bt in bufferedtrig:
                    
                    try:
                        self.datapiece.trigind.trigstartind[0]
                    except IndexError:
                        pass
                        bufferedtrig=bufferedtrig
                    else:
                        bufferedtrig=bufferedtrig-shape(bufferdata)[0]-self.datapiece.trigind.trigstartind[0]
                        self.datapiece.trigind.trigstartind=append(bufferedtrig, self.datapiece.trigind.trigstartind)
                    #clear buffer
                    print 'actual shape ', shape(self.datapiece.data_blockall)
                    print self.datapiece.trigind.trigstartind
                    del bufferdata

                if shape(self.datapiece.trigind.trigstartind)[0]==0: #no trigger detected, keep looking
                    
                    pass #nothing to do
                    print 'no trig detected'
                else: #detected trigger, look for enough space after each trigger
                    print self.datapiece.trigind.trigstartind
                    for trig in self.datapiece.trigind.trigstartind: #do something for each trigger found
                        if self.datapiece.chunk - trig >= epochwidth: #enough room for a single epoch
                            epochdata=(self.datapiece.data_blockall[trig:trig+epochwidth])
                            print 'shape of avg data ',shape(epochdata)

                            try:
                                avgdata
                            except NameError:
                                #avgdata = self.bufferdata[trig:trig+epochwidth,:] #create first epoch
                                avgdata = epochdata #create first epoch
                                self.avgdata=avgdata
                                self.avgtimes=0
                                
                            self.avgdata=(self.avgdata+epochdata)/2
                            print 'averaging', shape(self.avgdata)
                            self.avgtimes=self.avgtimes+1
                            
                        else: #not enough room for an epoch
                            try:
                                bufferedtrig
                            except NameError:
                                bufferedtrig=trig
                            else:
                                bufferedtrig=append(bufferedtrig, trig)
                                
                            trig2end=self.datapiece.chunk - trig #get size of from trigger ind to end of dataslice
                            print trig2end, 'buffered'
                            
                            try:
                                bufferdata #look for buffer var
                            except NameError:
                                #bufferdata = array([1,shape(self.datapiece.data_blockall)[1]]) #create empty buffer
                                bufferdata=self.datapiece.data_blockall[trig:trig+trig2end,:] #create first instance of buffer
                                #self.bufferdata=bufferdata #make global
                                print 'shape of first buffer data ',shape(bufferdata)
                            else:
                                
                            #print shape(self.datapiece.data_blockall)
                                bufferdata=append(bufferdata, self.datapiece.data_blockall[trig:trig+trig2end,:], axis=0) #keep appending until enough room
                                print 'shape of buffer data ',shape(bufferdata)
                        
            x=x+1
            print x
            print 'fid-tell',self.datapiece.fid.tell()
            
            try:
                self.datapiece.data_blockall
                #tmp.data_blockall
            except AttributeError:
                pass
                #cant find data
            else:
                #ok
                del self.datapiece.data_blockall, self.datapiece.trigind.trigstartind




        #dataall=
    def cont(self):
        pass
        
        '''continious build"
        datapiece.chunk();dataall='''