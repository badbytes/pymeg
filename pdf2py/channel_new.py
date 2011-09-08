#       channel_new.py
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



'''
i = channel_new.index(fn, type='all')
p = pdf.read(fn);p.data.getdata(0,p.data.pnts_in_file, chindex=i.indexlist)
'''

from pdf2py import config, header, headshape#, pdf
from numpy import zeros, array, unique, append, size, sort, loadtxt,delete
import re, sys, os
#try:from scipy.io.numpyio import *
#except ImportError: from extra.numpyio import *
from pdf2py import io_wrapper
fread = io_wrapper.fread
fwrite = io_wrapper.fwrite

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
    def __init__(self, datapdf, type=None, labels=None):

        '''Returns the channelindex for TYPE channels
        type = type of channel (meg | eeg | ref | trig | ext | derived | utility | shorted)'''
        '''sortedindtype----is the index to channels of type. use for extracting those meg channels

        ex.
        fn = '/path/to/file'
        ch = channel.index(fn, 'meg') #return meg channels
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

        if type != None:
            self.labellist, self.indexlist = self.getchindexfromtype(type)
        if labels != None:
            self.indexlist, self.labellist = self.getchindexfromlabelsinhdr(labels)
        if type == 'derived':
            self.indexlist, self.labellist = self.getchindexfromchannuminhdr('derived')

        try:
            self.chanlocs = self.locs2D(self.labellist)
        except:
            print 'something wrong with new chanloc method'

        try:
            if self.device_types.__contains__(1): #has meg channel data
                print 'Data contains MEG channels. Making 2D chanlocs map'
                self.chanlocs = self.locs2D(self.labellist)#, self.indexlist)
        except AttributeError:
            pass



        self.reverseindex = []; sortedindex = sort(self.indexlist)
        for i in sortedindex: #reverse index
            self.reverseindex.append(self.indexlist.index(i))


    def chtypes(self, chtype):
        dd=[]
        if type(chtype) == str:
            chtype = list([chtype])

        for i in chtype:
            '''EXTRACT CHANNELS'''
            if i == 'meg':
                device_data=[1]
            elif i == 'ref':
                device_data=[3]
            elif i == 'eeg':
                device_data=[2]
            elif i == 'ext':
                device_data=[4]
            elif i == 'trig':
                device_data=[5]
            elif i == 'util':
                device_data=[6]
            elif i == 'derived':
                device_data=[7]
            elif i == 'shorted':
                device_data=[8]
            elif i == 'all':
                ch_cfg = self.chbuilder_cfg('type', 'type')
                device_data=ch_cfg.keys()
            else:
                print 'unknown channel type', i
                device_data=[1000]
            dd.append(device_data)
        self.device_types = dd[0]
        return dd


    def chbuilder_hdr(self, key, term): #Header Channel label/term dictonary
        #ex. term = 'chan_no'
        '''z.__class__      z.__init__       z.attributes     z.chan_no        z.index          z.scale          z.whatisit       z.ymax
        z.__doc__        z.__module__     z.chan_label     z.checksum       z.reserved       z.valid_min_max  z.yaxis_label    z.ymin'''
        ch_hdr = {}
        for i in range(0, len(self.hdr.channel_ref_data)):
            if key == 'chan_label': ch_hdr[self.hdr.channel_ref_data[i].chan_label.strip('\x00')] = eval('self.hdr.channel_ref_data[i].'+term)
            else: ch_hdr[eval('self.hdr.channel_ref_data[i].'+key)[0]] = eval('self.hdr.channel_ref_data[i].'+term)
            #ch_hdr[eval('hdr.channel_ref_data[i].'+key+']') = eval('hdr.channel_ref_data[i].'+term+'[0]')
        return ch_hdr

    def chbuilder_cfg(self,key, term): #CFG Channel label/term dictonary
        '''x.__class__      x.__init__       x.aar_val        x.checksum       x.gain           x.reserved       x.type           x.yaxis_label
        x.__doc__        x.__module__     x.chan_no        x.device_data    x.name           x.sensor_no      x.units_per_bit '''
        ch_cfg = {}
        for i in range(0, len(self.cfg.channel_data)):
            if key == 'name': ch_cfg[self.cfg.channel_data[i].name.strip('\x00')] = eval('self.cfg.channel_data[i].'+term)
            else: ch_cfg[eval('self.cfg.channel_data[i].'+key)[0]] = eval('self.cfg.channel_data[i].'+term)
        return ch_cfg

    def getchindexfromchannuminhdr(self,type):
        ch_hdr = self.chbuilder_hdr('chan_no', 'index')
        indexlist = []; labellistnew = []
        for i in ch_hdr.keys():
            indexlist.append(ch_hdr[i][0])
            labellistnew.append(i)
        return indexlist, labellistnew

    def getchindexfromlabelsinhdr(self,labellist):
        '''channels should be in a list'''
        ch_hdr = self.chbuilder_hdr('chan_label', 'index')
        self.ch_hdr = ch_hdr;
        indexlist = []; labellistnew = []
        for i in labellist:
            try:
                indexlist.append(ch_hdr[i][0])
                labellistnew.append(i)
            except KeyError:
                print 'KeyError';pass
        return indexlist, labellistnew

    def getchindexfromtype(self,type):
        device_type = self.chtypes(type)[0]
        ch_cfg = self.chbuilder_cfg('name', 'type')
        typelist = []; #cfgindex = []
        for i in ch_cfg.keys():
            if len(device_type) == 1: #only one type
                if ch_cfg[i] == device_type:
                    typelist.append(i)
            else:
                for j in device_type:
                    if ch_cfg[i] == j:
                        typelist.append(i)


        sortedlabels = sorted(typelist)
        indexlist, labellist = self.getchindexfromlabelsinhdr(sortedlabels)
        return labellist, indexlist

    def getchindex2cfg(self, sortedlabels):
        ch_cfg = self.chbuilder_cfg('name', 'chan_no')
        index2cfg = [];

    def locs2D(self, labellist):
        chfound=[];chnotfound=[]
        cfglabels = []
        import readline
        #chaninfo = read_array(os.path.dirname(__file__)+'/configs/megchannels.cfg')
        chaninfo = loadtxt(os.path.dirname(__file__)+'/configs/megchannels.cfg')
        for l in chaninfo[0]:
            cfglabels.append('A'+str(int(l)))
        chanlocs248 = chaninfo[1:4]
        for ch in cfglabels:
            chfound.append(ch in labellist)
            if ch in labellist:
                pass
            else:
                chnotfound.append(ch)
        print 'Chanloc Maker:',len(chnotfound), 'MEG channels not found'
        chfound=array(chfound);
        return chanlocs248[:,chfound];

    def getchannellocations(self):
        '''returns sensor locations from an chanlabel list self.labellist
        sensors.locationsbyindex()'''

        self.chlpos = array([]);self.chupos=array([])
        self.chldir = array([]);self.chudir=array([])
        self.chname = array([])

        dd = self.chbuilder_cfg('name', 'device_data')

        for i in self.labellist:
            self.chupos = append(self.chupos,dd[i].loop_data[1].position)
            self.chlpos = append(self.chlpos,dd[i].loop_data[0].position)
            self.chudir = append(self.chudir,dd[i].loop_data[1].direction)
            self.chldir = append(self.chldir,dd[i].loop_data[0].direction)

        self.chupos=self.chupos.reshape(size(self.chupos)/3,3)
        self.chlpos=self.chlpos.reshape(size(self.chlpos)/3,3)
        self.chudir=self.chudir.reshape(size(self.chudir)/3,3)
        self.chldir=self.chldir.reshape(size(self.chldir)/3,3)

    def getposition(self):
        '''returns sensor locations from an self.labellist
        p.data.channels.getposition()
        returns
        p.data.channels.sensorpos'''
        self.getchannellocations()

    def deletechannel(self, index):
        self.chlpos = delete(self.chlpos,index,axis=0)
        self.chupos = delete(self.chupos,index)
        self.chldir = delete(self.chldir,index)
        self.chudir = delete(self.chudir,index)
        self.chanlocs = delete(self.chanlocs,index,axis=1)
        self.indexlist = delete(self.indexlist,index,axis=1)
        self.labellist = delete(self.labellist,index,axis=1)
        self.reverseindex = delete(self.reverseindex,index,axis=1)
        self.chanlocs = delete(self.chanlocs,index,axis=1)
        self.chanlocs = delete(self.chanlocs,index,axis=1)

