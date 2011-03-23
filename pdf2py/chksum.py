#       chksum.py
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


import types, inspect
from numpy import uint8, ndarray, dtype, sum, array
from meg.typecast import typecast

def __init__(object):
    '''parse object with inspect module to calc the sum of bytes'''
    if type(object) != types.InstanceType:
        print 'object not instance. goodbye'
        return
    checksum = -1
    for i in inspect.getmembers(object):

        if i[0].startswith('__'): #is module...skip
            pass

        else:
            #print checksum
            if type(i[1]) == ndarray:
                x = typecast(i[1],uint8)
                #print 'ndarray', i, sum(x)
                x = sum(x)
            elif type(i[1]) == str:
                x = 0
                for c in i[1]:
                    x = x + ord(c)

            if i[0] == 'checksum':
                origchecksum = i[1]

            if i[0] == 'checksum' or i[0] == 'nbytes' or i[0] == 'user_data':
                checksum = checksum + x
            checksum = checksum - x

            #print type(i[1]), i[0], sum(x)

    if checksum != origchecksum[0]:
        #print 'error with checksum on', object, ': old', origchecksum[0],'new',checksum
        pass

    return array([checksum])


