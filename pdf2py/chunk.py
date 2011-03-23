# Copyright 2008 Dan Collins
#

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

try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
import time
import os
from numpy import *
#import pylab as p

class go:
    def __init__(self, datapdf, sortedindtype):#, sortedindtype, plot, chanlocs):
        '''give channel index and plot='yes' or 'no' to indicate if you want to plot stream'''
        '''t=tap.go(datapdf, ch.sortedindtype)'''
        #open data and get initial *end of file* position
        #'/mnt/nfs/comeg2/0611/drawing3/01%01%01@01:01/5/c,rfDC'
        #check for file
        self.timelist=[]

        while os.path.isfile(datapdf)==False:
            print 'file not in existence... rechecking'
            try:
                check
            except NameError:
                check = 1; limit=30
                    
            while check < limit:
                time.sleep(1)
                check=check+1
                if check==limit:
                    print 'file not found...giving up'
                    return
        else:
            self.timelist.append(time.time()) #check time
            print 'reading pdf', os.path.abspath(datapdf)
            fid=open(datapdf, 'r')
            
        self.timelist.append(time.time())
        print fid
        step=1100  
        numch=275
        dataprecision='f'; 
        self.data_blockall=zeros((1,275))
        #x=1000; startpoint=x #number of reads
        #while x > 0:
            
        marker=fid.tell(); print 'marker ', marker
        gotoend=fid.seek(0, os.SEEK_END)
        endpos=fid.tell(); print 'end pos ', endpos
        chunk=int(floor((endpos-marker)/step)); print 'chunk ',chunk
        self.timelist.append(time.time())

        #if no more chunks of ok size
        trys=0
        while endpos-marker<step:
            print endpos, fid.tell()
            print 'end of file. trying to read again'
            time.sleep(.1)
            trys=trys+1
            gotoend=fid.seek(0, os.SEEK_END)
            endpos=fid.tell(); print 'end pos ', endpos
            chunk=int(floor((endpos-marker)/step)); print 'chunk ',chunk
            if trys==5:
                print 'giving up';
##                    p.plot(self.data_blockall[0:3000,0:50])
##                    p.show()                   
                return
            
        fid.seek(marker, os.SEEK_SET)
        data_chunk = fread(fid, chunk*numch, dataprecision, dataprecision, 1);
        print 'data size ', shape(data_chunk)
        print 'new position ', fid.tell()
        
        #catch error chunks
        while shape(data_chunk)[0] != chunk*numch:
            print 'error detected, rereading file'
            gotoend=fid.seek(0, os.SEEK_END)
            endpos=fid.tell()
            fid.seek(marker, os.SEEK_SET); print 'reseting to ', fid.tell()
            chunk=int(floor((endpos-marker)/step)); print 'chunk ',chunk
            data_chunk = fread(fid, chunk*numch, dataprecision, dataprecision, 1);
            time.sleep(.1)
            x=x+1
        
        data_block=data_chunk.reshape([shape(data_chunk)[0]/numch,numch])
        print shape(data_block)
        
        data_blocksorted = data_block[:,sortedindtype]

        #if x == startpoint:
            #self.data_blockall=data_block
        self.data_blockall=data_blocksorted
        #else:
            #self.data_blockall=append(data_block, self.data_blockall, axis=0)
            #self.data_blockall=append(data_blocksorted, self.data_blockall, axis=0)
        print shape(self.data_blockall)
        
        #x=x-1
            
            
##            if plot=='yes':
##                chan=0
##                contourplot()
        #p.plot(self.data_blockall[:,1])
        #p.draw()
        #p.ioff()
        #p.show()
        
        


