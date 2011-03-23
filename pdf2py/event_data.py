
try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape
from pdf2py import align
import os



class read:
    def __init__(self, fid):
        align.check(fid);
        
        #self.name = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        self.name = fid.read(16)
        self.start_lat = fread(fid, 1, 'f', 'f', 1);
        self.end_lat = fread(fid, 1, 'f', 'f', 1);
        self.step_size = fread(fid, 1, 'f', 'f', 1);
        self.fixed_event = fread(fid, 1, 'H', 'H', 1);
        fid.seek(2, os.SEEK_CUR);
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        #self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));
        self.reserved = fid.read(32)
        fid.seek(4, os.SEEK_CUR);
        
        
class write:
    def __init__(self, fid, event_data):
        align.check(fid);
        
        fid.write(event_data.name);
        fwrite(fid, 1, event_data.start_lat, 'f', 1);
        fwrite(fid, 1, event_data.end_lat, 'f', 1);
        fwrite(fid, 1, event_data.step_size, 'f', 1);
        fwrite(fid, 1, event_data.fixed_event, 'H', 1);
        fid.seek(2, os.SEEK_CUR);
        fwrite(fid, 1, event_data.checksum, 'i', 1);
        fid.write(event_data.reserved);
        fid.seek(4, os.SEEK_CUR);
