try: from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape
from pdf2py import align
import os
from pdf2py import chksum


class read:
    def __init__(self, fid):
        align.check(fid);
        #print 'fid position', fid.tell()
        self.pts_in_epoch = fread(fid, 1, 'I', 'I', 1);
        self.epoch_duration = fread(fid, 1, 'f', 'f', 1);
        self.expected_iti = fread(fid, 1, 'f', 'f', 1);
        self.actual_iti = fread(fid, 1, 'f', 'f', 1);
        self.total_var_events = fread(fid, 1, 'I', 'I', 1);
        #print self.total_var_events
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        self.epoch_timestamp = fread(fid, 1, 'i', 'i', 1);
        #self.reserved = ''.join(list(fread(fid, 28, 'c', 'c', 1)));
        self.reserved = fid.read(28)
        #%read dftk_event_data (var_events)
#for event = 1:epoch.total_var_events
    #epoch.var_event{event} = read_event_data(fid);
#end

class write:
    def __init__(self, fid, epoch_data):
        align.check(fid);
        fwrite(fid, 1, epoch_data.pts_in_epoch, 'I', 1);
        fwrite(fid, 1, epoch_data.epoch_duration, 'f', 1);
        fwrite(fid, 1, epoch_data.expected_iti, 'f', 1);
        fwrite(fid, 1, epoch_data.actual_iti, 'f', 1);
        fwrite(fid, 1, epoch_data.total_var_events, 'I', 1);
        #print self.total_var_events
        #fwrite(fid, 1, epoch_data.checksum, 'I', 1);
        fwrite(fid, 1, chksum.__init__(epoch_data), 'i', 1);
        fwrite(fid, 1, epoch_data.epoch_timestamp, 'i', 1);
        #fwrite(fid, 28, epoch_data.reserved, 'c', 1);
        fid.write(epoch_data.reserved)

