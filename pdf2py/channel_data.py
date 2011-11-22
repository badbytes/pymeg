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
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite
from pdf2py import align, device_data
import os, subprocess
from numpy import array
import logging

logger1 = logging.getLogger('1')
logger1.addHandler(logging.FileHandler('/tmp/logger1',mode='w'))
logger2 = logging.getLogger('2')
logger2.addHandler(logging.FileHandler('/tmp/logger2',mode='w'))
class read:
    def __init__(self, fid,log=None):
        align.check(fid);

        #logging.basicConfig(filename='/tmp/MSWconfigread.log',filemode='w',level=logging.DEBUG)
        self.name_array = array(fread(fid, 16, 'c', 'c', 1))
        self.name = ''.join(list(self.name_array));
        #print self.name,fid.tell()
        #self.name = fid.read(16)
        self.chan_no = fread(fid, 1, 'H', 'H', 1);
        self.type = fread(fid, 1, 'H', 'H', 1);
        self.sensor_no = fread(fid, 1, 'h', 'h', 1);
        fid.seek(2, os.SEEK_CUR);
        self.gain = fread(fid, 1, 'f', 'f', 1);
        self.units_per_bit = fread(fid, 1, 'f', 'f', 1);
        #self.yaxis_label = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        #self.yaxis_label = fid.read(16)
        self.yaxis_label = array(fread(fid, 16, 'c', 'c', 1))
        self.aar_val = fread(fid, 1, 'd', 'd', 1);
        self.checksum = fread(fid, 1, 'i', 'i', 1);
        #self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));

        #self.reserved = fid.read(32)
        self.reserved = array(fread(fid, 32, 'c', 'c', 1))
        fid.seek( 4, os.SEEK_CUR);
        #logger1.error((self.name_short,str(fid.tell())))

        if self.type in [1,3]: self.device_data = device_data.readmeg(fid); #meg/ref
        elif self.type in [2]: self.device_data = device_data.readeeg(fid); #eeg
        elif self.type in [4]: self.device_data = device_data.readexternal(fid); #external
        elif self.type in [5]: self.device_data = device_data.readtrigger(fid); #TRIGGER
        elif self.type in [6]: self.device_data = device_data.readutility(fid); #utility
        elif self.type in [7]: self.device_data = device_data.readderived(fid); #derived
        elif self.type in [8]: self.device_data = device_data.readshorted(fid); #shorted
        else:
            print 'device type unknown',self.type,self.name
            #sys.exit()


class write:
    def __init__(self, fid, channeldata, log=None):
        #logging.basicConfig(filename='/tmp/MSWconfigwrite.log',filemode='w',level=logging.DEBUG)

        align.check(fid);
        #logging.basicConfig(filename='/tmp/MSWconfigwrite.log',filemode='w',level=logging.DEBUG)
        #self.name = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        #fid.seek(16, os.SEEK_CUR);

        fwrite(fid, 1, array([channeldata.name_array]), 'c', 1); #16b
        #print channeldata.name,fid,fid.tell()
        fwrite(fid, 1, channeldata.chan_no, 'H', 1); #4b
        fwrite(fid, 1, channeldata.type, 'H', 1); #4b
        fwrite(fid, 1, channeldata.sensor_no, 'h', 1); #4b
        fid.seek(2, os.SEEK_CUR); #2b
        fwrite(fid, 1, channeldata.gain, 'f', 1); #4b
        fwrite(fid, 1, channeldata.units_per_bit, 'f', 1); #4b
        #self.yaxis_label = ''.join(list(fread(fid, 16, 'c', 'c', 1)));
        #fid.seek(16, os.SEEK_CUR);
        fwrite(fid, 1, array([channeldata.yaxis_label]), 'c', 1); #16
        fwrite(fid, 1, channeldata.aar_val, 'd', 1); #4
        fwrite(fid, 1, channeldata.checksum, 'i', 1); #4
        #self.reserved = ''.join(list(fread(fid, 32, 'c', 'c', 1)));
        #fid.seek(32, os.SEEK_CUR);
        fwrite(fid, 1, array([channeldata.reserved]), 'c', 1); #32
        fid.seek( 4, os.SEEK_CUR); #4b
        logger2.error((channeldata.name_short,str(fid.tell())))
        #fid.seek(77, os.SEEK_CUR);
        if channeldata.type in [1,3]: device_data.writemeg(fid,channeldata.device_data); #meg/ref
        elif channeldata.type in [2]: device_data.writeeeg(fid,channeldata.device_data); #eeg
        elif channeldata.type in [4]: device_data.writeexternal(fid,channeldata.device_data); #external
        elif channeldata.type in [5]: device_data.writetrigger(fid,channeldata.device_data); #TRIGGER
        elif channeldata.type in [6]: device_data.writeutility(fid,channeldata.device_data); #utility
        elif channeldata.type in [7]: device_data.writederived(fid,channeldata.device_data); #derived
        elif channeldata.type in [8]: device_data.writeshorted(fid,channeldata.device_data); #shorted
        else: print 'device type unknown'

