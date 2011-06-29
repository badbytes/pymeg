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

#try:from scipy.io.numpyio import *
#except ImportError: from extra.numpyio import *
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from numpy import char, reshape, array
from pdf2py import header_data, epoch_data, channel_ref_data, event_data, proc_data, proc_step
import os

class read:
    def __init__(self, datapdf):
        fid=open(datapdf, "r")
        fid.seek(0, os.SEEK_END); ep = fid.tell()
        fid.seek(-8, os.SEEK_END);
        header_offset=fread(fid, 1, 'q', 'q', 1); #first byte of the header
        try:
            fid.seek(header_offset, os.SEEK_SET);
        except IOError:
            print 'I dont think you selected a pdf file'
            return
        try:
            self.header_data = header_data.read(fid); #read first section of header
            self.epoch_data = [epoch_data.read(fid) for i in range(0, self.header_data.total_epochs[0])] #read epoch header info
            self.channel_ref_data = [channel_ref_data.read(fid) for j in range(0, self.header_data.total_chans[0])]
            self.event_data = [event_data.read(fid) for j in range(0, self.header_data.total_fixed_events[0])]
            self.proc_data = [proc_data.read(fid) for j in range(0, self.header_data.total_processes[0])]
            self.header_offset=header_offset
            fid.seek(0, os.SEEK_END)
            fid.close
        except IndexError:
            print 'probably not a 4D MEG file'
            pass

class write:
    def __init__(self, datapdf):
        hdr = datapdf.data.hdr
        print 'ch', hdr.header_data.total_chans
        fid=open(datapdf.data.writepath, "r+")
        fid.seek(0, os.SEEK_END);
        header_offset = array([fid.tell()])
        header_data.write(fid, hdr.header_data); #read first section of header
        [epoch_data.write(fid, hdr.epoch_data[i]) for i in range(0, hdr.header_data.total_epochs[0])] #writes epoch header info
        [channel_ref_data.write(fid, hdr.channel_ref_data[j]) for j in range(0, hdr.header_data.total_chans[0])]
        [event_data.write(fid, hdr.event_data[j]) for j in range(0, hdr.header_data.total_fixed_events[0])]
        [proc_data.write(fid, hdr.proc_data[j]) for j in range(0, hdr.header_data.total_processes[0])]
        fwrite(fid, 1, header_offset, 'q', 1); #first last byte of the header
        fid.close
