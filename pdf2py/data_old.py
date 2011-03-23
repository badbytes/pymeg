#how to
#d=data.read(fullpathtofile)
#d.getdata(fullpathtofile, 0, 3000, ch.sortedindtype)

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
from numpy import reshape, shape, arange, size
from pdf2py import align, header, channel
import os

class config:
    #d=data.read(fullpathtofile)
    def __init__(self, datapdf):
        '''d=data.read(datapdf)'''
        self.datapdf=datapdf
        self.hdr=header.read(datapdf)
        self.ext = 'pymdat'
        self.filename = datapdf
        
        self.total_chans=self.hdr.header_data.total_chans[0]
        #self.pnts_in_file=self.hdr.epoch_data[0].pts_in_epoch[0]*self.hdr.header_data.input_epochs
        #print 'pnts in file ', self.pnts_in_file
        self.format=self.hdr.header_data.data_format[0]
        self.fid=open(datapdf, "r") 
        print 'fidtell', self.fid.tell()
        
        if self.format == 1: 
            self.dataprecision='h'; 
            self.time_slice_size = 2 * self.total_chans; 
        if self.format == 2: 
            self.dataprecision='i'; 
            self.time_slice_size = 4 * self.total_chans;
        if self.format == 3: 
            self.dataprecision='f'; 
            self.time_slice_size = 4 * self.total_chans;
        if self.format == 4: 
            self.dataprecision='d'; 
            self.time_slice_size = 8 * self.total_chans;
        
        print 'time_slice_size ',self.time_slice_size
        print 'precision ', self.dataprecision
        self.pnts_in_file = self.hdr.header_offset / self.time_slice_size

class read(config):
    #d=data.read(fullpathtofile)
    def getdata(self, start, end, chindex=None):#chanindex):
        '''d.getdata(0, d.pnts_in_file, chindex=[1,2])
        or
                chind=ch.channelindexhdr[ch.channelsortedlabels == 'A63']
                 d.getdata(0, d.pnts_in_file, chindex=chind)'''

        self.fid.seek(start*self.time_slice_size, os.SEEK_SET)
        print 'skipped fidtell', self.fid.tell()
        print self.total_chans, end-start
        data_block = fread(self.fid, self.total_chans*(end-start), self.dataprecision, self.dataprecision, 1);
        print shape(data_block)
        data_blockreshape=data_block.reshape([ (end-start),self.total_chans])
        #self.data_blockunsorted=data_blockreshape
        if chindex!=None:
            self.data_block= data_blockreshape[:,chindex]
            
        self.fid.close
        
        self.numofepochs = self.pnts_in_file/self.time_slice_size
        lasttimepnt = self.time_slice_size/(1/self.hdr.header_data.sample_period)
        self.wintime = arange(0,lasttimepnt,self.hdr.header_data.sample_period)
        self.eventtime = self.wintime - self.hdr.event_data[0].start_lat
        self.numofchannels = size(self.data_block,1)
