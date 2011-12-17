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

#add-danc-writesupport

from numpy import char, reshape, arange, vstack
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from pdf2py import align
import os, subprocess

class read:
    def __init__(self, fid):
        align.check(fid);
        self.user_block_data_hdr_nbytes = fread(fid, 1, 'I', 'I', 1); #4 bytes
        self.user_block_data_hdr_type = ''.join(list(fread(fid, 20, 'c', 'c', 1))); #20b
        self.user_block_data_hdr_checksum = fread(fid, 1, 'i', 'i', 1);#4b
        self.user_block_data_user = fread(fid, 32, 'c', 'c', 1);#32b
        self.user_block_data_timestamp = fread(fid, 1, 'I', 'I', 1);#4b
        self.user_block_data_user_space_size = fread(fid, 1, 'I', 'I', 1);#4b
        self.user_block_data_reserved = fread(fid, 32, 'c', 'c', 1);#32
        fid.seek(4, os.SEEK_CUR);#4b

        if self.user_block_data_hdr_type == 'B_weights_used':
            st = fid.tell()

            print('WEIGHTS',(st,self.user_block_data_user_space_size))

        if self.user_block_data_hdr_type == 'b_eeg_elec_locs':
            st = fid.tell()
            coillabel1=''.join(list(fread(fid, 16, 'c', 'c', 1)));
            self.lpa = fread(fid,3,'d','d',1)
            fid.seek(16,1)
            self.rpa = fread(fid,3,'d','d',1)
            fid.seek(16,1)
            self.nas = fread(fid,3,'d','d',1)
            fid.seek(16,1)
            self.cz = fread(fid,3,'d','d',1)
            fid.seek(16,1)
            self.inion = fread(fid,3,'d','d',1)
            fid.seek(st,0)

        if self.user_block_data_hdr_type == 'B_COH_Points':
            self.coil_locations = []
            st = fid.tell()
            for i in arange(5):
                fid.seek(16,1)
                self.coil_locations.append(fread(fid,3,'d','d',1))

            self.coil_locations = vstack(self.coil_locations)
            fid.seek(st,0)

        #print self.user_block_data_hdr_type, fid.tell(), self.user_block_data_user_space_size
        fid.seek(self.user_block_data_user_space_size, os.SEEK_CUR) #skip user space




class write:
    def __init__(self, fid, user_block_data):

        align.check(fid);


        fwrite(fid, 1, user_block_data.user_block_data_hdr_nbytes, 'I', 1);

        #fid.seek(1, os.SEEK_CUR);
        #print 'cksum';fid.close()
        #subprocess.Popen('cksum /opt/msw/data/spartan_data0/1337/sef+eeg/03%31%09@11:17/1/configT', shell=True)
        #return

        #fwrite(fid, 20, pyconfig.user_block_data_hdr_type, 'c', 1);

        fid.seek(20, os.SEEK_CUR);

        #fwrite(fid, 1, user_block_data.user_block_data_hdr_checksum, 'i', 1);
        fid.seek(4, os.SEEK_CUR);

        #fwrite(fid, 32, pyconfig.user_block_data_user, 'c', 1);
        fid.seek(32, os.SEEK_CUR);

        #fwrite(fid, 1, user_block_data.user_block_data_timestamp, 'I', 1);
        fid.seek(4, os.SEEK_CUR);

        #fwrite(fid, 1, user_block_data.user_block_data_user_space_size, 'I', 1);
        fid.seek(4, os.SEEK_CUR);


        #fwrite(fid, 32, pyconfig.user_block_data_reserved, 'c', 1);
        fid.seek(32, os.SEEK_CUR);

        fid.seek(4, os.SEEK_CUR);

        fid.seek(user_block_data.user_block_data_user_space_size, os.SEEK_CUR) #skip user space



