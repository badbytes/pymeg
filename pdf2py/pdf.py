#       pdf.py
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


'''Main pdf2py module. Point to pdf file and it returns object for pdfdata,hs,config,header from pdf.'''

from pdf2py import config, header, headshape, data
#from pdf2py.pdf_functions import compute
import os
from meg import py2pdf
from numpy import array

class read():#(compute):
    '''fn = filename/pathtofile
    p = pdf.read(fn)
    p.data.setchannels('meg')
    p.data.getdata(0,10) #returns to first 10 points for all meg signal channels as new object p.data.data_block
    #OR
    p.data.getdata(0,p.data.pnts_in_file) #returns all points in file'''
    def __init__(self, datapdf):
        if os.path.isfile(datapdf)==True:
            print('reading pdf', os.path.abspath(datapdf))
            self.data = data.read(datapdf)
            print('reading pdf header', os.path.abspath(datapdf))
            self.hdr=header.read(datapdf); #reading withing data module
            if os.path.isfile(os.path.dirname(datapdf)+'/config')==True:
                print('found config file in same dir. Reading config')
                self.cfg=config.read(os.path.dirname(datapdf)+'/config');
            if os.path.isfile(os.path.dirname(datapdf)+'/hs_file')==True:
                print('found headshape file in same dir. Reading headshape')
                self.hs=headshape.read(os.path.dirname(datapdf)+'/hs_file');
            self.results = self.__class__

        else: print('no file found')



class write:
     def __init__(self, datapdf, data2write, pdffilename):
        print('writing pdffilename')
        py2pdf.writeascdata(array([[1],[1]]), pdffilename, array(['A1']), '/tmp/tmppdf.asc', datapdf.data.filepath, datapdf, '1', '1.0')#write fake temp file
        datapdf.data.writepath = datapdf.data.filedir+pdffilename
        if os.path.isfile(datapdf.data.filepath)==True:
            print('writing pdf', os.path.abspath(datapdf.data.writepath))
            data.write(datapdf, data2write)
            print('writing pdf header', os.path.abspath(datapdf.data.writepath))
            header.write(datapdf); #writing header





