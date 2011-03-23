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

'''Returns channel indexing for pdf file
ex.
fn = ['/path/E-0053/EPILEPSY2/09%21%09@11:41/1/c,rfhp0.1Hz,f3-70bp,o,o,d2']
p = pdf.read(fn[0])
p.data.setchannels('meg')
#OR
fn = '/path/to/file'
ch = channel.index(fn[0], 'meg') #return meg channels
'''

from pdf2py import config, header, headshape#, pdf
#from meg import sensors
import os
from numpy import zeros, array, unique, append, size, loadtxt
import re
import sys
#from scipy.io import write_array
#from scipy.io import read_array

def sorted(alist):
    '''sort channels'''
    indices = map(_generate_index, alist)
    decorated = zip(indices, alist)
    decorated.sort()
    return [ item for index, item in decorated ]

def _generate_index(str):
    """
    Splits a string into alpha and numeric elements, which
    is used as an index for sorting"
    """
    index = []
    def _append(fragment, alist=index):
        if fragment.isdigit(): fragment = int(fragment)
        alist.append(fragment)

    # initialize loop
    prev_isdigit = str[0].isdigit()
    current_fragment = ''
    # group a string into digit and non-digit parts
    for char in str:
        curr_isdigit = char.isdigit()
        if curr_isdigit == prev_isdigit:
            current_fragment += char
        else:
            _append(current_fragment)
            current_fragment = char
            prev_isdigit = curr_isdigit
    _append(current_fragment)
    return tuple(index)

class index:
    def __init__(self, datapdf, type):

        '''Returns the channelindex for TYPE channels
        type = type of channel (meg | eeg | ref | trig | ext | derived | utility | shorted)'''
        '''sortedindtype----is the index to channels of type. use for extracting those meg channels

        ex.
        fn = '/path/to/file'
        ch = channel.index(fn[0], 'meg') #return meg channels
        '''
        self.datapdf = datapdf
        self.type = type


        if os.path.isfile(datapdf)==True:
            self.hdr=header.read(datapdf);
            if os.path.isfile(os.path.dirname(datapdf)+'/config')==True:
                self.cfg=config.read(os.path.dirname(datapdf)+'/config');
            if os.path.isfile(os.path.dirname(datapdf)+'/hs_file')==True:
                headshape.read
                self.hs=headshape.read(os.path.dirname(datapdf)+'/hs_file');
            else:
                print 'no headshape file'

        cind=[];
        chlabellist=[]#=empty
        chnumber=zeros([len(self.hdr.channel_ref_data)], dtype=int) #channel label, number and index array
        chindex=zeros([len(self.hdr.channel_ref_data)], dtype=int) #channel label, number and index array
        cfgchname=[]
        cfgchtype=zeros([len(self.cfg.channel_data)], dtype=int) #channel label, number and index array
        cfgchannumber=zeros([len(self.cfg.channel_data)], dtype=int) #channel label, number and index array

        for i in range(0, len(self.hdr.channel_ref_data)):
            cind.append(self.hdr.channel_ref_data[i].chan_label)
            chlabellist.append(self.hdr.channel_ref_data[i].chan_label)
            chnumber[i]=(self.hdr.channel_ref_data[i].chan_no)
            chindex[i]=(self.hdr.channel_ref_data[i].index)
        chlabel=array(chlabellist)

        self.chlabel=chlabel
        self.chnumber=chnumber
        self.chindex=chindex

        for i in range(0, len(self.cfg.channel_data)):
            cfgchname.append(self.cfg.channel_data[i].name)
            cfgchtype[i]=(self.cfg.channel_data[i].type)
            cfgchannumber[i]=(self.cfg.channel_data[i].chan_no)
        cfgchname=array(cfgchname)
        self.cfgchname=cfgchname
        self.cfgchtype=cfgchtype
        self.cfgchannumber=cfgchannumber

        def indexsorted(sortedch, chlisttoindex):
            chlist=list(chlisttoindex)

            sortind=[];
            for i in sortedch:
                sortind.append(chlist.index(i))
            return sortind

        '''sort channels and return indexing array'''
        self.unsortedch=chlabel;
        if type == 'derived':
            print 'cant sort derived channels'
            return

        self.sortedch=array(sorted(self.unsortedch))
        self.sortedind=array(indexsorted(self.sortedch, self.chlabel))
        self.sortedcharray=array(chlabel[self.sortedind])

        '''EXTRACT CHANNELS'''
        if type == 'meg':
            device_data=[1]
        elif type == 'ref':
            device_data=[3]
        elif type == 'eeg':
            device_data=[2]
        elif type == 'ext':
            device_data=[4]
        elif type == 'trig':
            device_data=[5]
        elif type == 'util':
            device_data=[6]
        elif type == 'derived':
            device_data=[7]
        elif type == 'shorted':
            device_data=[8]
        elif type == 'all':
            device_data=unique(cfgchtype)
        else:
            print 'unknown channel type', type
            device_data=[1000]


        dd = device_data

        self.chanbool=cfgchtype[chnumber-1]==dd #cfgchtype[chnumber-1] returns boolean to unsorted channel of type
        self.unsortedlabeltype=self.unsortedch[self.cfgchtype[self.chnumber-1]==dd] #unsorted of only device type
        self.sortedlabeltype=array(sorted(self.unsortedlabeltype)) #sorted labels
        self.sortedindtype=array(indexsorted(self.sortedlabeltype, self.chlabel)) #sorted index of certain type
        self.channelsind=self.chindex[self.chanbool]
        self.channelsname=self.chlabel[self.chanbool]
        self.allfromconfig=cfgchname[cfgchtype[cfgchannumber<1000-1]==dd] #get all channels from config less than number value=1000 (excludes weird types)

        '''return index to config'''
        try:
            self.ind2cfg=array(indexsorted(self.sortedlabeltype, self.cfgchname))
        except ValueError:
            print 'names in config don\'t match header. no sort'
            return

        #--20090928--danc--fixing bug from previous channel locs method which picked up unsorted channel labels and used that to index sorted coordinates, which produced wrong results.

        chfound=[] #empty array
        cfglabels = []
        import readline
        if type == 'meg': #build meg channel 2d locations
            #chaninfo = read_array(os.path.dirname(__file__)+'/configs/megchannels.cfg')
            chaninfo = loadtxt(os.path.dirname(__file__)+'/configs/megchannels.cfg')
            for l in chaninfo[0]:
                #print l
                cfglabels.append('A'+str(int(l)))
            chanlocs248 = chaninfo[1:4]

            for ch in cfglabels:
                chfound.append(ch in self.sortedlabeltype)
                if ch in self.sortedlabeltype:
                    pass
                else:
                    print 'Chanloc Maker Warning:',ch, 'not found'
            self.chfound=array(chfound);

            self.chanlocs=chanlocs248[:,self.chfound];

        self.channelindexhdr=self.sortedindtype
        self.channelindexcfg=self.ind2cfg
        self.channelsortedlabels=self.sortedlabeltype
        self.channeltype = type
        del self.channelsind,self.chanbool,self.unsortedlabeltype,self.unsortedch
        del self.cfgchannumber,self.cfgchname,self.cfgchtype,self.cfg,self.allfromconfig
        del self.channelsname,self.chindex,self.chlabel,self.chnumber
        del self.hdr,self.sortedcharray,self.sortedlabeltype,self.ind2cfg

    class locationsbyindex:
        def __init__(self, datapdf, index):
            '''returns sensor locations from an index provided
            sensors.locationsbyindex(datapdf, ch.channelindexcfg)'''
            #--20090707--danc--read config directly to keep from infinite looping
            #pdfinstance=pdf.read(datapdf)
            if os.path.isfile(os.path.dirname(datapdf)+'/config')==True:
                #print 'found config file in same dir. Reading config'
                cfg=config.read(os.path.dirname(datapdf)+'/config');

            self.chlpos = array([]);self.chupos=array([])
            self.chldir = array([]);self.chudir=array([])
            self.chname = array([])
            #--20090817--danc--flipped lower and upper position and direction, as I had it wrong before now.
            for i in index:
                self.chupos = append(self.chupos,cfg.channel_data[i].device_data.loop_data[1].position)
                self.chlpos = append(self.chlpos,cfg.channel_data[i].device_data.loop_data[0].position)
                self.chudir = append(self.chudir,cfg.channel_data[i].device_data.loop_data[1].direction)
                self.chldir = append(self.chldir,cfg.channel_data[i].device_data.loop_data[0].direction)
                self.chname = append(self.chname,cfg.channel_data[i].name)


            self.chupos=self.chupos.reshape(size(self.chupos)/3,3)
            self.chlpos=self.chlpos.reshape(size(self.chlpos)/3,3)
            self.chudir=self.chudir.reshape(size(self.chudir)/3,3)
            self.chldir=self.chldir.reshape(size(self.chldir)/3,3)


    def getposition(self):
        '''returns sensor locations from an index provided
        p.data.channels.getposition()
        returns
        p.data.channels.sensorpos'''
        #print self.datapdf
        j = index(self.datapdf, self.type)
        self.sensorpos = j.locationsbyindex(self.datapdf, self.channelindexcfg)

