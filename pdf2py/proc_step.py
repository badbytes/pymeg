#       proc_step.py
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
from numpy import char, reshape, double
from pdf2py import align
import os
from pdf2py import chksum

class read:
    def __init__(self, fid):
        align.check(fid)
        self.nbytes_step = fread(fid, 1, 'I', 'I', 1);
        self.type = fid.read(20)
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        #Process Step Struct
        T = ''.join(self.type.split('\x00'))
        if T == 'b_filt_hp' or T == 'b_filt_lp' or T == 'b_filt_notch':
            self.frequency = fread(fid, 1, 'f', 'f', 1)
            self.reserved =  fid.read(32)

        elif T == 'b_filt_b_pass' or T == 'b_filt_b_reject':
            self.high_frequency = fread(fid, 1, 'f', 'f', 1)
            self.low_frequency = fread(fid, 1, 'f', 'f', 1)
            self.reserved =  fid.read(32)
            fid.seek(4, os.SEEK_CUR) #align

        else:
            self.user_space_size = fread(fid, 1, 'I', 'I', 1);
            self.reserved = fid.read(32)
            self.user_data = fid.read(self.user_space_size)
            #fid.seek(self.user_space_size%8)
            #align.check(fid)

class write:
    def __init__(self, fid, proc_step):
        align.check(fid)
        fwrite(fid, 1, proc_step.nbytes_step, 'I', 1);
        fid.write(proc_step.type)
        fwrite(fid, 1, chksum.__init__(proc_step), 'i', 1);

        #Process Step Struct
        T = ''.join(proc_step.type.split('\x00'))
        if T == 'b_filt_hp' or T == 'b_filt_lp' or T == 'b_filt_notch':
            fwrite(fid, 1, proc_step.frequency, 'f', 1)
            fid.write(proc_step.reserved)

        elif T == 'b_filt_b_pass' or T == 'b_filt_b_reject':
            fwrite(fid, 1, proc_step.high_frequency, 'f', 1)
            fwrite(fid, 1, proc_step.low_frequency, 'f', 1)
            fid.write(proc_step.reserved)
            fid.seek(4, os.SEEK_CUR) #align
        else:
            fwrite(fid, 1, proc_step.user_space_size, 'I', 1);
            fid.write(proc_step.reserved)
            fid.write(proc_step.user_data)
            #fid.seek(self.user_space_size%8)
            #align.check(fid)
