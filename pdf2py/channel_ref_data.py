#       channel_ref_data.py
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

#try:from scipy.io.numpyio import *
#except ImportError: from extra.numpyio import *
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from numpy import char, reshape
from pdf2py import align
import os
from pdf2py import chksum

class read:
    def __init__(self, fid):
        align.check(fid);

        #self.chan_label = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        self.chan_label = fid.read(16)
        self.chan_no = fread(fid, 1, 'H', 'H', 1);
        self.attributes = fread(fid, 1, 'H', 'H', 1);
        self.scale = fread(fid, 1, 'f', 'f', 1);
        #self.yaxis_label = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        self.yaxis_label = fid.read(16)
        self.valid_min_max = fread(fid, 1, 'H', 'H', 1);
        fid.seek(6, os.SEEK_CUR);
        self.ymin = fread(fid, 1, 'd', 'd', 1);
        self.ymax = fread(fid, 1, 'd', 'd', 1);
        self.index = fread(fid, 1, 'I', 'I', 1);
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        #%something new?
        #self.whatisit = ''.join(list(fread(fid, 4, 'c', 'c', 1)));
        self.whatisit = fid.read(4)
        #self.reserved = ''.join(list(fread(fid, 28, 'c', 'c', 1)));
        self.reserved = fid.read(28)
        #%reserved first 4 bytes are not 0?

class write:
    def __init__(self, fid, channel_ref_data):
        align.check(fid);

        fid.write(channel_ref_data.chan_label);
        fwrite(fid, 1, channel_ref_data.chan_no, 'H', 1);
        fwrite(fid, 1, channel_ref_data.attributes, 'H', 1);
        fwrite(fid, 1, channel_ref_data.scale, 'f', 1);
        fid.write(channel_ref_data.yaxis_label);
        fwrite(fid, 1, channel_ref_data.valid_min_max, 'H', 1);
        fid.seek(6, os.SEEK_CUR);
        fwrite(fid, 1, channel_ref_data.ymin, 'd', 1);
        fwrite(fid, 1, channel_ref_data.ymax, 'd', 1);
        fwrite(fid, 1, channel_ref_data.index, 'I', 1);
        #fwrite(fid, 1, channel_ref_data.checksum, 'i', 1);
        fwrite(fid, 1, chksum.__init__(channel_ref_data), 'i', 1);
        #%something new?
        fid.write(channel_ref_data.whatisit);
        fid.write(channel_ref_data.reserved);
        #%reserved first 4 bytes are not 0?

if __name__ == "__main__":
    pass

