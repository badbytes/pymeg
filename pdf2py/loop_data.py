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

try:from scipy.io.numpyio import *
except ImportError: from extra.numpyio import *
from numpy import char, reshape
from pdf2py import align
import os

class read:
    def __init__(self, fid):
        align.check(fid);
        self.position = fread(fid, 3, 'd', 'd', 1)*1000; #convert to mm
        self.direction = fread(fid, 3, 'd', 'd', 1);
        self.radius = fread(fid, 1, 'd', 'd', 1);
        self.wire_radius = fread(fid, 1, 'd', 'd', 1);
        self.turns = fread(fid, 1, 'H', 'H', 1);
        fid.seek(2, os.SEEK_CUR);
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        self.reserved = fread(fid, 32, 'c', 'c', 1);
        
class write:
    def __init__(self, fid, loop_data):
        align.check(fid);
        
        fwrite(fid, 3, loop_data.position, 'd', 1)/1000; #convert to meters
        fwrite(fid, 3, loop_data.direction, 'd', 1);
        fwrite(fid, 1, loop_data.radius, 'd', 1);
        fwrite(fid, 1, loop_data.wire_radius, 'd', 1);
        fwrite(fid, 1, loop_data.turns, 'H', 1);
        fid.seek(2, os.SEEK_CUR);
        fwrite(fid, 1, loop_data.checksum, 'i', 1);
        #fwrite(fid, 32, loop_data.reserved, 'c', 1);
        fid.seek(32, os.SEEK_CUR);
