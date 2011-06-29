#       fread_wrapper.py
#
#       Copyright 2011 dan collins <danc@badbytes.net>
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

'''Wrapper for the depreciated numpy.io fread and fwrite'''

from numpy import fromfile#, tofile

def fread(fid, numofelements, dtype, null=None, endianness=None):
    if endianness == 1:
        result = fromfile(fid, dtype, count=numofelements).byteswap()
    return result

#fwrite(fid, 1, pyconfig.data_sys_type, 'H', 1);

def fwrite(fid, numofelements, data, dtype, endianness=None):
    if endianness == 1:
        data.byteswap().tofile(fid)

    #z.byteswap().tofile('test')
