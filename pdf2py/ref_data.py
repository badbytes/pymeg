try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape
from pdf2py import align
import os



class read:
    def __init__(self, fid):
        align.check(fid);
        
        self.chan_label = fread(fid, 16, 'c', 'c', 1);
##        self.chan_no = fread(fid, 1, 'H', 'H', 1);
##        self.attributes = fread(fid, 1, 'H', 'H', 1);
##        self.scale = fread(fid, 1, 'f', 'f', 1);
##        self.yaxis_label = fread(fid, 16, 'c', 'c', 1);
##        self.valid_min_max = fread(fid, 1, 'H', 'H', 1);
##        fid.fseek(6, os.SEEK_CUR);
##        self.ymin = fread(fid, 1, 'd', 'd', 1);
##        self.ymax = fread(fid, 1, 'd', 'd', 1);
##        self.index = fread(fid, 1, 'I', 'I', 1);
##        self.checksum = fread(fid, 1, 'i', 'i', 1);
##        #%something new?
##        self.whatisit = fread(fid, 4, 'c', 'c', 1);
##        self.reserved = fread(fid, 28, 'c', 'c', 1);
##        #%reserved first 4 bytes are not 0?
        
