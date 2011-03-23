#       update_data_header.py
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

'''update_data_header.py
updates the p.data.hdr header to prepare for rewrite of 4D format data.
accomidates when channels read are less that in orig file, or window changes, etc'''

from numpy import *

def cutchannels(data):
    data.hdr.header_data.total_chans = array([data.channels.indexlist.__len__()], dtype=data.hdr.header_data.total_chans.dtype)

    channel_ref_data = arange(data.channels.indexlist.__len__()).tolist()
    #channel_ref_data = []
    #for i in data.channels.indexlist:
    for i in range(0, data.channels.indexlist.__len__()):
        #print data.channels.reverseindex[i], channel_ref_data, data.hdr.channel_ref_data[data.channels.reverseindex[i]]
        try:
            channel_ref_data[i] = data.hdr.channel_ref_data[data.channels.indexlist[i]]
        #channel_ref_data.append(data.hdr.channel_ref_data[i])
        #data.hdr.channel_ref_data[i].index = array([channel_ref_data.__len__()], dtype=data.hdr.channel_ref_data[i].index.dtype)
            channel_ref_data[i].index = array([i], dtype=data.hdr.channel_ref_data[data.channels.indexlist[i]].index.dtype)
        except IndexError:
            print 'IndexError... NEED TO FIX'
        #print channel_ref_data[i].index
    data.hdr.channel_ref_data = channel_ref_data


