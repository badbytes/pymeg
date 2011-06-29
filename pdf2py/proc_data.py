#       proc_data.py
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
from pdf2py import chksum, proc_step


class read:
    def __init__(self, fid):
        align.check(fid)
        self.nbytes = fread(fid, 1, 'I', 'I', 1);
        self.type = fid.read(20)
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        self.user = fid.read(32)
        self.timestamp = fread(fid, 1, 'I', 'I', 1);
        self.filename = fid.read(256)
        self.total_steps = fread(fid, 1, 'I', 'I', 1);
        self.reserved = fid.read(32)
        align.check(fid)

        try:
            #print 'proc_step', self.total_steps[0], fid.tell()
            self.proc_step = [proc_step.read(fid) for j in range(0, self.total_steps[0])]
        except MemoryError:
            print 'memory error at', fid.tell()


class write:
    def __init__(self, fid, proc_data):
        align.check(fid)
        fwrite(fid, 1, proc_data.nbytes, 'I', 1);
        fid.write(proc_data.type)
        fwrite(fid, 1, proc_data.checksum, 'i', 1);
        fid.write(proc_data.user)
        fwrite(fid, 1, proc_data.timestamp, 'I', 1);
        fid.write(proc_data.filename)
        fwrite(fid, 1, proc_data.total_steps, 'I', 1);
        fid.write(proc_data.reserved)
        align.check(fid)

        try:
            #print 'proc_step', proc_data.total_steps[0], fid.tell()
            self.proc_step = [proc_step.write(fid, proc_data.proc_step[j]) for j in range(0, proc_data.total_steps[0])]
        except AttributeError:
            pass #no processing step data. skip
