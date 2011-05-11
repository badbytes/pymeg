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

#import matplotlib.axes3d as p3   #legacy code
'3d plotting doesnt work in pylab v .98'

#danc changed units to mm from meters

class read:
    def __init__(self, hsfile):
        self.fid=open(hsfile, "r") 
        self.hdr_version = fread(self.fid, 1, 'i', 'i', 1);
        self.hdr_timestamp = fread(self.fid, 1, 'i', 'i', 1);
        self.hdr_checksum = fread(self.fid, 1, 'i', 'i', 1);
        self.hdr_npoints = fread(self.fid, 1, 'i', 'i', 1);
        self.index_lpa = fread(self.fid, 3, 'd', 'd', 1)*1000;
        self.index_rpa = fread(self.fid, 3, 'd', 'd', 1)*1000;
        self.index_nasion = fread(self.fid, 3, 'd', 'd', 1)*1000;
        self.index_cz = fread(self.fid, 3, 'd', 'd', 1)*1000;
        self.index_inion = fread(self.fid, 3, 'd', 'd', 1)*1000;
 
        hs_pointvec = fread(self.fid, self.hdr_npoints*3, 'd', 'd', 1)*1000;
        self.hs_point = reshape(hs_pointvec, [len(hs_pointvec)/3, 3])
        self.fid.close
