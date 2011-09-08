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


#try:from scipy.io.numpyio import *
#except ImportError: from extra.numpyio import *
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from numpy import reshape, shape, float32, array, arange, size, single, append, delete
from pdf2py import align, header, config, channel_new #channel
import os
from meg import functions

class initialize():
    def __init__(self, datapdf):
        '''d=data.read(datapdf)'''

        try:
            self.datapdf=datapdf
            self.hdr=header.read(datapdf)
            self.ext = 'pymdat'
            self.filepath = datapdf
            pathlist = self.filepath.split('/')
            self.filename = pathlist.pop()
            self.run = pathlist.pop()
            self.session = pathlist.pop()
            self.scan = pathlist.pop()
            self.pid = pathlist.pop()
            self.filedir = self.filepath.replace(self.filepath.split('/')[-1],'')
            self.total_chans=self.hdr.header_data.total_chans[0]
            self.format=self.hdr.header_data.data_format[0]
            self.fid=open(datapdf, "r")
            #print 'fidtell', self.fid.tell()
        except IndexError:
            print 'probably not a 4D MEG file'
            pass

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

class read(initialize):
    def getdata(self, start, end, chindex=None):#chanindex):
        from meg import functions
        '''d.getdata(0, d.pnts_in_file, chindex=[1,2])
        or
                chind=ch.channelindexhdr[ch.channelsortedlabels == 'A63']
                 d.getdata(0, d.pnts_in_file, chindex=chind)'''

        self.fid.seek(start*self.time_slice_size, os.SEEK_SET)
        self.fid_start_pos = self.fid.tell()
        data_block = fread(self.fid, self.total_chans*(end-start), self.dataprecision, self.dataprecision, 1);
        self.fid_end_pos = self.fid.tell()
        data_blockreshape=(data_block.reshape([ (end-start),self.total_chans]))

        if self.format == 1:
            print 'WARNING, bug in scalefactor order here. NEED TO FIX'
            print 'short format, multiplying units_per_bit from cfg'
            if os.path.isfile(os.path.dirname(self.datapdf)+'/config')==True:
                print 'found config file in same dir. Reading config'
                self.cfg=config.read(os.path.dirname(self.datapdf)+'/config');
                cfgchlist = []
                for t in range(0, self.cfg.data_total_chans):
                    cfgchlist.append(self.cfg.channel_data[t].chan_no)
                self.scalefact = []
                for c in range(0, self.hdr.header_data.total_chans):
                    scalefact = self.cfg.channel_data[cfgchlist.index(self.hdr.channel_ref_data[c].chan_no)].units_per_bit
                    self.scalefact = append(self.scalefact, scalefact)
                data_blockreshape = data_blockreshape*scalefact

            else:
                print "can't read config from same directory"

        if chindex!=None:
            self.data_block = data_blockreshape[:,chindex]
            self.scalefact = 1
        else:
            try:
                self.data_block = data_blockreshape[:,self.channels.indexlist]
            except AttributeError:
                print 'no channels specified'
                print "try something like... obj.setchannels('meg')"
                print "or something like... obj.data.getdata(0,p.data.pnts_in_file, chindex=obj.data.channels.channelsind)"
                return

        self.fid.close
        self.numofepochs = self.hdr.header_data.total_epochs[0] #self.pnts_in_file/self.time_slice_size
        #lasttimepnt = (self.pnts_in_file / self.numofepochs)/\
        #(1/self.hdr.header_data.sample_period)
        #self.wintime = arange(0,lasttimepnt,self.hdr.header_data.sample_period)[:-1]
        lasttimepnt = self.hdr.header_data.sample_period * self.pnts_in_file
        self.wintime = arange(0,lasttimepnt,self.hdr.header_data.sample_period)
        self.epoch_size = self.pnts_in_file / self.numofepochs
        self.eventtime = self.wintime[0:self.epoch_size] - self.hdr.event_data[0].start_lat
        self.numofchannels = size(self.data_block,1)
        self.srate = 1/self.hdr.header_data.sample_period[0]
        self.frames = self.data_block.shape[0] / self.numofepochs
        print 'DATA DEBUG', shape(self.data_block)
    def setchannels(self, chtype):
        '''chtype = = type of channel (meg | eeg | ref | trig | ext | derived | utility | shorted)'''
        self.setchanneltype(chtype)

    def setchanneltype(self, chtype):
        '''chtype = = type of channel (meg | eeg | ref | trig | ext | derived | utility | shorted)'''
        from pdf2py import update_data_header
        self.channels = channel_new.index(self.datapdf, chtype)
        update_data_header.cutchannels(self)
        try:
            self.channels.getposition()
        except:
            print('Error setting channel positions')

    def setchannellabels(self, chlabels):
        from pdf2py import update_data_header
        '''chlabel = ['A1','A2']'''
        self.channels = channel_new.index(self.datapdf, labels=chlabels)
        update_data_header.cutchannels(self)
        try:
            self.channels.getposition()
        except:
            print('Error setting channel positions')

    def analyze(self):
        from meg import analyze
        self.analyze = analyze

    def deletechannel(self,index):
        self.data_block = delete(self.data_block,index,axis=1)
        self.channel.deletechannel(index)
        self.numofchannels = self.numofchannels - len(index)


##------------------------------------------------------------------------------------------
class write:
    def __init__(self, datapdf, data2write):
        #import shutil
        #from numpy import int16
        self.fid = open(datapdf.data.filepath, 'w')
        self.fid.seek(0*datapdf.data.time_slice_size, os.SEEK_SET)

        if datapdf.data.format == 1:
            data = (data2write) * datapdf.data.scalefact
        if datapdf.data.format == 3:
            data = single(data2write)#*2
            print 'dataprecision is single'#, datapdf.data.dataprecision

        print 'writing',datapdf.data.numofchannels, 'channels'

        if len(data2write.shape) == 2:
            numofpnts2write = data2write.shape[0]*data2write.shape[1]
            reindexed_data = data.flatten()
        elif len(data2write.shape) == 1:
            numofpnts2write = data2write.shape[0]
            reindexed_data = data
        print numofpnts2write, reindexed_data.shape
        fwrite(self.fid, numofpnts2write, reindexed_data, datapdf.data.dataprecision, 1);

        self.fid.close()

class write_changes:
    def __init__(self, dataobj, data2write):
        '''
        ex.

        fn = '/home/danc/data/meg/0611piez/e,rfhp1.0Hz,ra.mod'
        p = pdf.read(fn)
        p.data.setchannellabels(['A1','A100'])
        p.data.setchannels('meg')
        p.data.getdata(0,p.data.pnts_in_file)
        p.data.data_block = p.data.data_block * 100
        pdf.write_changes(p.data, p.data.data_block)

        '''
        print data2write
        self.fid = open(dataobj.filepath, 'r+')
        self.fid.seek(0,os.SEEK_SET)

        if dataobj.format == 1:
            data = (data2write) * dataobj.scalefact
        if dataobj.format == 3:
            data = single(data2write)#*2
            print 'dataprecision is single'#, dataobj.dataprecision

        numofpnts2write = data2write.shape[0]*data2write.shape[1]
        print 'saving changes to file. ',dataobj.numofchannels, 'channels getting rewritten.'

        bitsperchan = dataobj.time_slice_size/dataobj.total_chans
        for c in arange(len(dataobj.channels.indexlist)): #for each channel
            #print 'ch',c
            seekpnt = bitsperchan * (dataobj.channels.indexlist[c])
            for s in arange(dataobj.pnts_in_file): #for each time point.
                self.fid.seek(seekpnt + (dataobj.time_slice_size * s), os.SEEK_SET)
                fwrite(self.fid, 1, data2write[s,c], dataobj.dataprecision, endianness=1)
        print 'saving changes to file complete.'

        self.fid.close()


