#       matlab_wrapper.py
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

import scipy.io
import inspect


def loadmat(filename):
    mat = scipy.io.loadmat(filename)
    mat = checktype(mat)
    return mat

def checktype(mat):
    #always read as dict. check each key and see if its structured or not
    for i in mat.keys():
        try:
            mat[i].dtype[0]
            d = {}
            print 'Crappy MATLAB structured format'
            c = mat[i]
            xx = inspect.getmembers(mat[i].dtype)
            for j in xx:
                if j[0] == 'names':
                    names = j[1]
            for k in names:
                d[k] = c[0,0][k]
            return d
        except AttributeError:
            pass
        except KeyError:
            pass
    return mat
