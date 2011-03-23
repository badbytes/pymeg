#       header_data.py
#
#       Copyright 2010 dan collins <danc@badbytes.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape, array
from pdf2py import align
import os
from pdf2py import chksum
#cb1silfdFD
class read:
    def __init__(self, fid):
        align.check(fid);
        self.version = fread(fid, 1, 'H', 'H', 1);
        #file_type = fread(fid, 5, 'c', 'c', 1);

        #self.file_type = ''.join(list(fread(fid, 5, 'c', 'c', 1)));
        self.file_type = fid.read(5);
        fid.seek(1, os.SEEK_CUR);#%alignment
        self.data_format = fread(fid, 1, 'h', 'h', 1);
        self.acq_mode = fread(fid, 1, 'H', 'H', 1);
        self.total_epochs = fread(fid, 1, 'I', 'I', 1);
        self.input_epochs = fread(fid, 1, 'I', 'I', 1);
        self.total_events = fread(fid, 1, 'I', 'I', 1);
        self.total_fixed_events = fread(fid, 1, 'I', 'I', 1);
        self.sample_period = fread(fid, 1, 'f', 'f', 1);
        #xaxis_label = fread(fid, 16, 'c', 'c', 1);
        #self.xaxis_label = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        self.xaxis_label = fid.read(16);
        self.total_processes = fread(fid, 1, 'I', 'I', 1);
        self.total_chans = fread(fid, 1, 'H', 'H', 1);
        fid.seek(2, os.SEEK_CUR);#%alignment
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        self.total_ed_classes = fread(fid, 1, 'I', 'I', 1);
        self.total_associated_files = fread(fid, 1, 'H', 'H', 1);
        self.last_file_index = fread(fid, 1, 'H', 'H', 1);
        self.timestamp = fread(fid, 1, 'I', 'I', 1);
        #self.reserved = ''.join(list(fread(fid, 20, 'c', 'c', 1)));
        self.reserved = fid.read(20);
        fid.seek(4, os.SEEK_CUR);#%alignment



class write:
    def __init__(self, fid, header_data):
        #import array
        align.check(fid);
        fwrite(fid, 1, header_data.version, 'H', 1);
        #file_type = fread(fid, 5, 'c', 'c', 1);
        #print fid.
        fid.write(header_data.file_type)
        #fwrite(fid, 5, header_data.file_type, 'c', 1);
        fid.seek(1, os.SEEK_CUR);#%alignment
        fwrite(fid, 1, header_data.data_format, 'h', 1);
        fwrite(fid, 1, header_data.acq_mode, 'H', 1);
        fwrite(fid, 1, header_data.total_epochs, 'I', 1);
        fwrite(fid, 1, header_data.input_epochs, 'I', 1);
        fwrite(fid, 1, header_data.total_events, 'I', 1);
        fwrite(fid, 1, header_data.total_fixed_events, 'I', 1);
        fwrite(fid, 1, header_data.sample_period, 'f', 1);
        #xaxis_label = fwrite(fid, 16, 'c', 'c', 1);
        fid.write(header_data.xaxis_label);
        fwrite(fid, 1, header_data.total_processes, 'I', 1);
        fwrite(fid, 1, header_data.total_chans, 'H', 1);
        fid.seek(2, os.SEEK_CUR);#%alignment
        #fwrite(fid, 1, header_data.checksum, 'i', 1);
        fwrite(fid, 1, chksum.__init__(header_data), 'i', 1);
        fwrite(fid, 1, header_data.total_ed_classes, 'I', 1);
        fwrite(fid, 1, header_data.total_associated_files, 'H', 1);
        fwrite(fid, 1, header_data.last_file_index, 'H', 1);
        fwrite(fid, 1, header_data.timestamp, 'I', 1);
        fid.write(header_data.reserved);
        fid.seek(4, os.SEEK_CUR);#%alignment
