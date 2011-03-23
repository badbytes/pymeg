'''exp reader'''

try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape, array
from pdf2py import header_data, epoch_data, channel_ref_data, event_data
import os
 
class readpid:
    def __init__(self, Exp):
        fid=open(datapdf, "r") 
        id = fread(fid, 10, 'c','c',1);
        fid.seek(1, os.SEEK_CUR);
        lname = fread(fid, 15, 'c','c',1);
        fid.seek(2, os.SEEK_CUR);
        fname = fread(fid, 15, 'c','c',1);
        fid.seek(1, os.SEEK_CUR);
        mname = fread(fid, 17, 'c','c',1);
        fid.seek(1, os.SEEK_CUR);
        #fid.tell = 59
        #cb1silfdFD
        fid.seek(60, os.SEEK_SET);x=fread(fid, 1, 'i','i',1);
        
        
        self.header_data = header_data.read(fid); #read first section of header
        self.epoch_data = [epoch_data.read(fid) for i in range(0, self.header_data.total_epochs[0])] #read epoch header info
        self.channel_ref_data = [channel_ref_data.read(fid) for j in range(0, self.header_data.total_chans[0])]
        self.event_data = [event_data.read(fid) for j in range(0, self.header_data.total_fixed_events[0])]
        self.header_offset=header_offset
        fid.close
