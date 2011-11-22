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
from numpy import char, reshape
from pdf2py import align, device_header, loop_data
import os, subprocess
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite

class readmeg:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.inductance = fread(fid, 1, 'f', 'f', 1);
        fid.seek(4, os.SEEK_CUR);
        self.Xfm = fread(fid, 4*4, 'd', 'd', 1);
        self.xform_flag = fread(fid, 1, 'H', 'H', 1);
        self.total_loops = fread(fid, 1, 'H', 'H', 1);
        self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));
        fid.seek(4, os.SEEK_CUR);

        self.loop_data = [loop_data.read(fid) for i in range(0, self.total_loops[0])] #read loop data

class readeeg:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.impedance = fread(fid, 1, 'f', 'f', 1);
        fid.seek(4, os.SEEK_CUR);
        self.Xfm = fread(fid, 4*4, 'd', 'd', 1);
        self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));

class readexternal:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.user_space_size = fread(fid, 1, 'I', 'I', 1);
        self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(4, os.SEEK_CUR);

class readtrigger:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.user_space_size = fread(fid, 1, 'I', 'I', 1);
        self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(4, os.SEEK_CUR);

class readutility:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.user_space_size = fread(fid, 1, 'I', 'I', 1);
        self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(4, os.SEEK_CUR);

class readderived:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.user_space_size = fread(fid, 1, 'I', 'I', 1);
        self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(4, os.SEEK_CUR);

class readshorted:
    def __init__(self, fid):
        align.check(fid);
        self.hdr = device_header.read(fid);
        self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1 )));
        #fid.seek(4, os.SEEK_CUR);

#-----------WRITE----------------

class writemeg:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.inductance, 'f', 1);
        fid.seek(4, os.SEEK_CUR);
        fwrite(fid, 4*4, device_data.Xfm, 'd', 1);
        fwrite(fid, 1, device_data.xform_flag, 'H', 1);
        fwrite(fid, 1, device_data.total_loops, 'H', 1);
        #self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));
        fid.seek(32, os.SEEK_CUR);
        fid.seek(4, os.SEEK_CUR);

        for i in range(0, device_data.total_loops[0]):
            loop_data.write(fid, device_data.loop_data[i])

        #self.loop_data = [loop_data.read(fid) for i in range(0, self.total_loops[0])] #read loop data

class writeeeg:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.impedance, 'f', 1);
        fid.seek(4, os.SEEK_CUR);
        fwrite(fid, 4*4, device_data.Xfm, 'd', 1);
        #self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        #fid.seek(4, os.SEEK_CUR);

class writeexternal:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.user_space_size, 'I', 1);
        #self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        fid.seek(4, os.SEEK_CUR);

class writetrigger:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.user_space_size, 'I', 1);
        #self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        fid.seek(4, os.SEEK_CUR);

class writeutility:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.user_space_size, 'I', 1);
        #self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        fid.seek(4, os.SEEK_CUR);

class writederived:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        fwrite(fid, 1, device_data.user_space_size, 'I', 1);
        #self.reserved = ''.join(list(fread(fid, 32,  'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        fid.seek(4, os.SEEK_CUR);

class writeshorted:
    def __init__(self, fid, device_data):
        align.check(fid);
        device_header.write(fid, device_data.hdr);
        #self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1 )));
        fid.seek(32, os.SEEK_CUR);
        #fid.seek(4, os.SEEK_CUR);
