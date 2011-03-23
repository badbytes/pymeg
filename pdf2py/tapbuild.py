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
from numpy import shape, average, array, append, any, zeros, arange
from pdf2py import tap, trigdet,contourbuild, powerspecbuild, pdf
from meg import offset
import pylab


class config:
    def __init__(self, datapdf, datatemplate):
        self.datapiece=tap.chunk(datapdf); print 'init datafile' #initialize datafile
        self.datapiece.setparams(datatemplate, trig='TRIGGER') ; print 'init parameters'#initialize parameters
        self.pdfobj=pdf.read(datatemplate)



class get(config):
    def avg(self, epochwidth, channelinstance, contour=None, butterfly=None, csd=None, sp=None):
        '''average data'''
        '''epochwidth is the number of samples/epoch'''

        def calldata(channelinstance):#, fidpos):
            self.datapiece.getchunk(channelinstance)#, fidpos);
            try:
                self.datapiece.data_blockall
            except AttributeError:
                return False  #no data opened
            else: #opened data
                print 'shape if incoming data', shape(self.datapiece.data_blockall)
                print 'fid-tell',self.datapiece.fid.tell()
                #print 'first trigger ',self.datapiece.trigind.trigstartind[0]
                return True
        def parsetrig():

            try:
                self.datapiece.trigind.trigstartind[0]
            except IndexError:
                return False  #no data opened
            except AttributeError:
                return False
            else:
                return True

        def checkbuffer():
            try: self.bufferdata
            except AttributeError:
                print 'nothing buffered'
                #self.bufferdata=self.datapiece.data_blockall
                return False
            else: #something buffered, prepend to incomming data
                return True

        def prepend():
            print 'prepending. New shape should be ',shape(self.datapiece.data_blockall), '+', shape(self.bufferdata)
            self.datapiece.data_blockall=append(self.bufferdata, self.datapiece.data_blockall, axis=0) #prepended data

            try:
                self.datapiece.trigind.trigstartind
            except AttributeError:
                pass
                #self.bufferedtrig=self.bufferedtrig
            else:
                if parsetrig()==False: #no trig
                    print 'no trigger instance'
                    print self.bufferedtrig
                    self.bufferedtrig=self.bufferedtrig-self.bufferedtrig[0]
                else:
                    #print 'trig instance',self.datapiece.trigind.trigstartind
                    #print 'buffered trigs',self.bufferedtrig
                    self.datapiece.trigind.trigstartind=self.datapiece.trigind.trigstartind+shape(self.bufferdata)[0] #change indexing to add space from buffer
                    self.bufferedtrig=array([self.bufferedtrig-self.bufferedtrig[0]])
                self.datapiece.trigind.trigstartind=append(self.bufferedtrig, self.datapiece.trigind.trigstartind)
                #print 'new indexing',self.datapiece.trigind.trigstartind

            #clear buffer
            #print 'actual shape ', shape(self.datapiece.data_blockall)
            #print 'new trigs',self.datapiece.trigind.trigstartind
            del self.bufferdata, self.bufferedtrig

        def avgdata():

            print self.datapiece.trigind.trigstartind
            for trig in self.datapiece.trigind.trigstartind: #do something for each trigger found
                if self.datapiece.chunk - trig >= epochwidth: #enough room for a single epoch
                    epochdata=(self.datapiece.data_blockall[trig:trig+epochwidth])
                    #print 'shape of avg data ',shape(epochdata)
                    try:
                        print 'checking for avg data'
                        self.data_avg
                    except AttributeError:
                        print 'starting first epoch'
                        self.data_avg = epochdata #create first epoch
                        #self.data_avg=data_avg
                        self.avgtimes=0
                        self.data3d=epochdata
                    self.data_avg=offset.correct((self.data_avg+epochdata))
                    #print 'shape of avg',self.data_avg
                    #print 'averaging', shape(self.data_avg)
                    self.avgtimes=self.avgtimes+1
                    #print 'avgtimes', self.avgtimes
                    self.lastepoch=offset.correct(epochdata)
                    #self.data3d=append(self.data3d,self.lastepoch)
                    print self.avgtimes,shape(epochdata)[0], shape(epochdata)[1]
                    #self.data3d=offset.correct(self.data3d.reshape(self.avgtimes+1, shape(epochdata)[0], shape(epochdata)[1]))
                else: #not enough room for an epoch
                    print 'not enough room for an epoch'
                    try:
                        self.bufferedtrig
                    except AttributeError:
                        self.bufferedtrig=array([trig])
                    else:
                        self.bufferedtrig=append(self.bufferedtrig, trig)

                    trig2end=shape(self.datapiece.data_blockall)[0] - trig #get size of from trigger ind to end of dataslice
                    #print trig2end, 'buffered'

                    try:
                        self.bufferdata #look for buffer var
                    except AttributeError:
                        #bufferdata = array([1,shape(self.datapiece.data_blockall)[1]]) #create empty buffer
                        self.bufferdata=self.datapiece.data_blockall[trig:trig+trig2end,:] #create first instance of buffer
                        #print 'shape of first buffer data ',shape(self.bufferdata)
                    else:

                    #print shape(self.datapiece.data_blockall)
                        self.bufferdata=append(self.bufferdata, self.datapiece.data_blockall[trig:trig+trig2end,:], axis=0) #keep appending until enough room
                        #print 'shape of buffer data ',shape(self.bufferdata)
        def clean():
            try:
                self.datapiece.data_blockall
            except AttributeError:
                pass
            else:
                print 'deleting'
                del self.datapiece.data_blockall
                del self.datapiece.trigind.trigstartind


        x=0;y=0
        numofloops=200
        #someval=200230
        #inc=arange(numofloops*someval)
        #fidpos=[2000000]
        #fidpos=[140617600]

        #fidpos=[1000230, 2000000, 4000000, 8000000, 10000000, 11000000, 20000000] #4 debugging
        pylab.ion()
        pylab.figure()

        while x < numofloops: #loops
            print x
            y=y+1
            if calldata(channelinstance):#, fidpos[0]*y)==True: #read chunk
                print 'data read'
##                print self.datapiece.trigind.trigstartind
##                if shape(self.datapiece.trigind.trigstartind)[0]==0: #no trigger detected...
##                    print 'no new trig detected'
                if parsetrig()==True: #trigs found
                    print 'trigs found'
                else:
                    print 'no trigs found'
                    time.sleep(5)


                if checkbuffer()==True:
                    print 'something buffered'
                    prepend(); print 'prepending data'
                print 'averaging data'
                avgdata()
                #print 'exiting';return

                print 'plotting'

                pylab.subplot(331)
                pylab.cla()
                if contour != None:
                    contourbuild.display(self.data_avg[contour,:], channelinstance.chanlocs)
                #p.draw()
                #pylab.subplot(212)
                #butterfly=None, csd=None, sp=None
                if csd != None:
                    powerspecbuild.calc(self.data_avg, self.pdfobj)

                #pylab.show()


##                #buffer() #call buffer function to either prepend existing data to incoming, or create buffer out of new piece.
##                shape(self.bufferdata); print 'shape of buffer'

            else:
                print 'no data read'
            x=x+1
            print x
            #print 'fid-tell',self.datapiece.fid.tell()
            clean(); print 'cleaning'

        pylab.ioff()
        pylab.show()

        #dataall=
    def cont(self):
        pass

        '''continious build"
        datapiece.chunk();dataall=


from pdf2py import tap, channel, tapbuild

template='/opt/msw/data/sam_data0/00000/BuildAVG/03%24%09@15:39/1/e,rfDC'
acqfile='/opt/msw/data/sam_data0/00000/BuildAVG/03%24%09@15:39/2/e,rfDC'
tapped = tapbuild.get(acqfile,template)
epochwidth=20
ch=channel.index(template, 'meg')
tapped.avg(epochwidth, ch)



        '''