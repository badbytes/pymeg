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
from numpy import char, reshape, array
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from pdf2py import user_block_data, channel_data
import shutil
import os, subprocess
import logging

logger1 = logging.getLogger('1')
logger1.addHandler(logging.FileHandler('/tmp/logger1',mode='w'))
logger2 = logging.getLogger('2')
logger2.addHandler(logging.FileHandler('/tmp/logger2',mode='w'))

class read:
    def __init__(self, configfile):
        fid=open(configfile, "r")
        dataype = 's'
        self.data_version = fread(fid, 1, 'H', 'H', 1);
        self.data_site_name = array(fread(fid, 32, 'c', 'c', 1))
        self.data_site_name_short = ''.join(list(self.data_site_name))
        #self.data_site_name = fid.read(32)
        self.data_dap_hostname = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        #self.data_dap_hostname = fid.read(16)

        self.data_sys_type = fread(fid, 1, 'H', 'H', 1);
        self.data_sys_options = fread(fid, 1, 'I', 'I', 1);
        self.data_supply_freq = fread(fid, 1, 'H', 'H', 1);
        self.data_total_chans = fread(fid, 1, 'H', 'H', 1);
        self.data_system_fixed_gain = fread(fid, 1, 'f', 'f', 1);
        self.data_volts_per_bit = fread(fid, 1, 'f', 'f', 1);
        self.data_total_sensors = fread(fid, 1, 'H', 'H', 1);
        self.data_total_user_blocks = fread(fid, 1, 'H', 'H', 1);
        self.data_next_derived_channel_number = fread(fid, 1, 'H', 'H', 1);
        fid.seek(2, 1)
        self.data_checksum = fread(fid, 1, 'i', 'i', 1);
        self.data_reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));

        Xfm = fread(fid, 4*4, 'd', 'd', 1);
        self.Xfm=Xfm.reshape([4, 4]);

        self.user_block_data = [user_block_data.read(fid) for i in range(0, self.data_total_user_blocks[0])] #read user blocks
        self.channel_data = [channel_data.read(fid) for i in range(0, self.data_total_chans[0])] #read channel data

        for i in range(0, self.data_total_user_blocks[0]):
            if self.user_block_data[i].user_block_data_hdr_type == 'B_COH_Points':
                self.coil_locations = self.user_block_data[i].coil_locations * .1


        fid.close

class write:
    def __init__(self, configfile, pyconfig): #pyconfig is the already read structure
        '''configfile = '/opt/msw/data/spartan_data0/1337/sef+eeg/03%31%09@11:17/1/config'
        hsfile = '/opt/msw/data/spartan_data0/1337/sef+eeg/03%31%09@11:17/1/hs_file'
        c = config.read(configfile)
        cw = config.write(configfile, c)
        #c2 = COHtransform.calc(configfile, hsfile)

        '''
        output = configfile+'T'
        os.chmod(output, 0660) 
        shutil.copyfile(configfile, output)
        
        fid = open(output, 'r+')
        dataype = 's'

        fwrite(fid, 1, pyconfig.data_version, 'H', 1);
        #fid.seek(32, 1)
        fwrite(fid, 32, array([pyconfig.data_site_name]), 'c', 1);
        fid.seek(16, 1)
        #fwrite(fid, 16, array([pyconfig.data_dap_hostname]), 'c', 1);
        fwrite(fid, 1, pyconfig.data_sys_type, 'H', 1);
        fwrite(fid, 1, pyconfig.data_sys_options, 'i', 1);
        fwrite(fid, 1, pyconfig.data_supply_freq, 'H', 1);
        fwrite(fid, 1, pyconfig.data_total_chans, 'H', 1);
        fwrite(fid, 1, pyconfig.data_system_fixed_gain, 'f', 1);
        fwrite(fid, 1, pyconfig.data_volts_per_bit, 'f', 1);
        fwrite(fid, 1, pyconfig.data_total_sensors, 'H', 1);
        fwrite(fid, 1, pyconfig.data_total_user_blocks, 'H', 1);
        fwrite(fid, 1, pyconfig.data_next_derived_channel_number,'H', 1);
        fid.seek(2, 1)
        fwrite(fid, 1, pyconfig.data_checksum, 'i', 1);
        fid.seek(32, 1)
        #fwrite(fid, 1, array([pyconfig.data_reserved]), 'c', 1);

        fwrite(fid, 16, pyconfig.Xfm, 'd', 1);
        print 'XFM',pyconfig.Xfm
        self.fid = fid

        for i in range(0, pyconfig.data_total_user_blocks[0]):
            user_block_data.write(fid, pyconfig.user_block_data[i])
            #return
        for i in range(0, pyconfig.data_total_chans[0]):
            channel_data.write(fid, pyconfig.channel_data[i])
            #if i == 2:
                #return

        fid.close()


if __name__ == "__main__":
    configfile = '/home/danc/programming/python/Colorado_Oct2011_Cal-Refs.config'
    hsfile = '/opt/msw/data/spartan_data0/1337/sef+eeg/03%31%09@11:17/1/hs_file'
    c = read(configfile)
    write(configfile,c)
    print dir(c), c.data_dap_hostname

