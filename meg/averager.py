#       averager.py
#       
#       Copyright 2009 dan collins <quaninux@gmail.com>
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

'''averages epochs, raw files, on specific indices.
a = averager.on_epochs(data, epochs, start, end)
...
a = averager.on_epochs(p.data.data_block, p.data.numofepochs, 0, 300)
averages the first 300 points after the onset of epoch
'''

from numpy import *
#from pdf2py import file

def raw(rawdata, epochs):
    'rawdata is 2D array, datapnts X channels'
    numch = size(rawdata,1)
    redata = rawdata.reshape([size(rawdata,0)/epochs, epochs, numch], order='F')
    adata = mean(redata,1)
    return adata
#fil=m[244,:]

def pdffilepath(pdffilename, hdrfilename):
    'datapdf is filename, hdr is MEG header name'
    

def pdffiles(data, hdr):
    'data is the 2D data to average, hdr is MEG header'
    numch = size(rawdata,1)

def on_epochs(data, epochs, start, end):
    'data is the 2D data to average, hdr is MEG header'
    numch = size(data,1)
    
    redata = data.reshape([size(data,0)/epochs, epochs, numch], order='F')
    print shape(redata)
    cutdata = redata[int(start):int(end),:]
    print shape(cutdata)
    adata = mean(cutdata,1)
    return adata

def on_trig(data, trigind):
    'data is the 2D data to average, hdr is MEG header'
    numch = size(data,1)
    epochs = len(trigind); print 'numepochs',epochs
    redata = data.reshape([size(data,0)/epochs, epochs, numch], order='F')
    print shape(redata)
    cutdata = redata[int(start):int(end),:]
    
    
def multiplepdfs():
    from gui import pysel
    return pysel
    
