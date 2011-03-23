#!/usr/bin/env python
# Time-stamp: <2000-08-09 18:02:58 miller>
"""dycom.py
Some python to access David A. Clunie's dicom3tools. 

Copyright (C) 2000 Michael A. Miller <mmiller@debian.org>
Time-stamp: <2000-08-09 17:55:38 miller>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA.
"""

import commands
import string

import Gnuplot
import Image
import Numeric

from Constants import *

def tags(line):
    result = None
    words = string.split(line)
    if len(words) >= 1:
        #print words, len(words[0])
        if len(words[0]) == 15:
            tags = string.split(words[0],',')
            #print tags
            tags[0] = tags[0][1:]
            tags[1] = tags[1][:-1]
            result = tags
    return result

class DICOM:
    def __init__(self,filename):
        self.filename = filename

    def andump(self):
        # ANDUMP(1)   DICOM PS3 - Describe ACR-NEMA file content  ANDUMP(1)
        # 
        # NAME
        #        andump  -  ACR/NEMA  DICOM  PS3 ... Describe ACR-NEMA file
        #        content
        # 
        # SYNOPSIS
        #        andump   [    -showoffset|-showoffset-hex    |-showoffset-
        #                  octal|-showoffset-oct         |-showoffset-deci-
        #                  mal|-showoffset-dec ]
        # 
        # DESCRIPTION
        #        andump reads the named acr-nema input file  and  describes
        #        the information contained, without attempting to interpret
        #        the structure of the message (cf. dcdump).
        # 
        #        The group and  element  number,  dictionary  and  explicit
        #        value representation, description of tag, value length and
        #        value of the element are  displayed,  optionally  with  an
        #        offset byte count from the start of the file.
        
        status, self.raw_andump = commands.getstatusoutput('andump ' + self.filename)
        #print 'andump status =', status
        self.andump_lines = string.split(self.raw_andump,'\n')
        self.andump_dict = {}
        #for l in self.andump_lines:
        #    print tags(l), l

    def dcdump(self):
        # DCDUMP(1)    DICOM PS3 - Describe DICOM file content    DCDUMP(1)
        # 
        # NAME
        #        dcdump - ACR/NEMA DICOM PS3 ... DICOM PS3 - Describe DICOM
        #        file content
        # 
        # SYNOPSIS
        #        dcdump [ -v|verbose ]
        # 
        # DESCRIPTION
        #        dcdump reads the named dicom or acr-nema  input  file  and
        #        describes  the information contained, attempting to inter-
        #        pret  the  structure  of  the  message,  including  nested
        #        sequences (cf. andump).
        # 
        #        The  group  and  element  number,  dictionary and explicit
        #        value representation, description of tag, value length and
        #        value  of  the  element  are displayed, optionally with an
        #        offset byte count from the start of the file.
        
        status, self.raw_dcdump = commands.getstatusoutput('dcdump ' + self.filename)
        #print 'dcdump status =', status
        self.dcdump_lines = string.split(self.raw_dcdump,'\n')
        self.dcdump_dict = {}
        #for l in self.dcdump_lines:
        #    print tags(l), l

    def dchist(self):
        # DCHIST(1)       DICOM PS3 - DICOM image statistics      DCHIST(1)
        # 
        # NAME
        #        dchist  -  ACR/NEMA  DICOM PS3 ... DICOM PS3 - DICOM image
        #        statistics
        # 
        # SYNOPSIS
        #        dchist [ -h|histogram ] [ -v|verbose ]
        # 
        # DESCRIPTION
        #        dchist reads the named dicom or acr-nema  input  file  and
        #        describes the statistics of the image pixel data. The pri-
        #        mary intent is to determine the zero order entropy of  the
        #        image.
        #              
        #        The description and verbose output go to standard error.
        
        status, self.raw_dchist = commands.getstatusoutput('dchist -h ' + self.filename)
        #print 'dchist status =', status
        self.dchist_lines = string.split(self.raw_dchist,'\n')
        pixels = []
        counts = []        
        for line in self.dchist_lines:
            #print line
            words = string.split(line)
            if len(words) ==  5:
                if words[0][0:3] == '[0x':
                    if words[0] != '[0x0]':
                        pixels.append(string.atoi(words[0][1:-1],0))
                        counts.append(string.atoi(words[1]))
        self.hist = Numeric.zeros(max(pixels)+1)
        for i in range(len(pixels)):
            #print i, pixels[i], counts[i]
            self.hist[pixels[i]] = counts[i]

    def plot_dchist(self):
        self.dchist()
        g1 = Gnuplot.Gnuplot()
        data = Gnuplot.Data(range(len(self.hist)), self.hist)
        g1('set data style lines')
        g1.plot(data)
        raw_input('Please press return to continue...\n')

    def dckey(self,key):
        # DCKEY(1)       DICOM PS3 - Extract attribute values      DCKEY(1)
        #
        # NAME
        #       dckey - ACR/NEMA DICOM PS3 ... Extract attribute values
        #
        # SYNOPSIS
        #       dckey [ -v|verbose ] [ -describe ] [ -key|k  attributename
        #                 ]
        #
        # DESCRIPTION
        #       dckey reads the named dicom input file  and  displays  the
        #       values of the selected attributes.
        #
        #       Binary  attributes  are written in hexadecimal with a pre-
        #       ceding "0x". Numeric string attributes are written in dec-
        #       imal.
        status, result = commands.getstatusoutput('dckey -key ' + key + ' ' + self.filename)
        return result

    def dcposn(self,x,y):
        #     DCPOSN(1)       DICOM PS3 - DICOM locate position       DCPOSN(1)
        # 
        # NAME
        #        dcposn  -  ACR/NEMA DICOM PS3 ... DICOM PS3 - DICOM locate
        #        position
        # 
        # SYNOPSIS
        #        dcposn [ -col|x n ] [ -row|y n ] [ -v|verbose ]
        # 
        # DESCRIPTION
        #        dcposn reads the named dicom input file  and  locates  the
        #        requested  image  pixel  position  in  3D  space using the
        #        attributes of  the  Image  Plane  module  (Image  Position
        #        Patient and Image Orientation Patient) if present.
        # 
        #        The  spatial position is described as patient (not gantry)
        #        relative x, y and z co-ordinates, where  x  is  +ve  left-
        #        wards, y is +ve anteriorly and z is +ve cranially.

        status, raw_posn = commands.getstatusoutput('dcposn -x %d -y %d %s' %
                                                    ( x, y, self.filename ) )
        #print 'dcposn status =', status
        lines = string.split(raw_posn,'\n')
        words = string.split(lines[-1])

        row = string.atoi(string.split(words[0],'=')[1])
        col = string.atoi(string.split(words[1],'=')[1])
        x = string.atof(string.split(words[2],'=')[1])
        y = string.atof(string.split(words[3],'=')[1])
        z = string.atof(string.split(words[4],'=')[1])
        
        result = ( row, col, x, y, z )
        return result

    def dctopgm8(self,pgmfile):
        status, text = commands.getstatusoutput('dctopgm8 %s %s' %
                                                    ( self.filename, pgmfile ) )
        #print 'dctopgm8 status =', status

    def dctoraw(self,rawfile):
        status, text = commands.getstatusoutput('dctoraw %s %s' %
                                                ( self.filename, rawfile ) )
        #print 'dctoraw status =', status
        #print text

    def dicomdir(self):
        # Uses dcdump to read a DICOMDIR file. 
        self.dcdump()

        # Each file entry will look something like this:
        #  ----:
        #    > (0x0004,0x1430) CS Directory Record Type 	 VR=<CS>   VL=<0x0006>  <IMAGE > 
        #    > (0x0004,0x1500) CS Referenced File ID 	 VR=<CS>   VL=<0x0018>  <S9267260\S197240\I10000 > 
        #    > (0x0008,0x0008) CS Image Type 	 VR=<CS>   VL=<0x001a>  <ORIGINAL\PRIMARY\AXIAL\CT > 
        #    > (0x0008,0x0016) UI SOP Class UID 	 VR=<UI>   VL=<0x001a>  <1.2.840.10008.5.1.4.1.1.2> 
        #    > (0x0008,0x0018) UI SOP Instance UID 	 VR=<UI>   VL=<0x003a>  <1.2.840.113704.6.8833521926726.20000125.19724.10000100032> 
        #    > (0x0008,0x0023) DA Content (formerly Image) Date 	 VR=<DA>   VL=<0x0008>  <20000125> 
        #    > (0x0008,0x0033) TM Content (formerly Image) Time 	 VR=<TM>   VL=<0x0006>  <072655> 
        #    > (0x0018,0x0010) LO Contrast/Bolus Agent 	 VR=<LO>   VL=<0x0000>  <> 
        #    > (0x0020,0x0013) IS Instance (formerly Image) Number 	 VR=<IS>   VL=<0x0004>  <1000> 
        #    > (0x0020,0x0052) UI Frame of Reference UID 	 VR=<UI>   VL=<0x0030>  <1.2.840.113704.6.8833521926726.19723.10000100512> 
        #    > (0x0020,0x1041) DS Slice Location 	 VR=<DS>   VL=<0x0006>  <871.9 > 
        #    > (0x0028,0x0002) US Samples per Pixel 	 VR=<US>   VL=<0x0002>  [0x0001] 
        #    > (0x0028,0x0004) CS Photometric Interpretation 	 VR=<CS>   VL=<0x000c>  <MONOCHROME2 > 
        #    > (0x0028,0x0010) US Rows 	 VR=<US>   VL=<0x0002>  [0x0200] 
        #    > (0x0028,0x0011) US Columns 	 VR=<US>   VL=<0x0002>  [0x0200] 
        #    > (0x0028,0x0100) US Bits Allocated 	 VR=<US>   VL=<0x0002>  [0x0010] 
        #    > (0x0088,0x0200) SQ Icon Image Sequence 	 VR=<SQ>   VL=<0xffffffff>  
        #  ----:
        #    > (0x0028,0x0002) US Samples per Pixel 	 VR=<US>   VL=<0x0002>  [0x0001] 
        #    > (0x0028,0x0004) CS Photometric Interpretation 	 VR=<CS>   VL=<0x000c>  <MONOCHROME2 > 
        #    > (0x0028,0x0010) US Rows 	 VR=<US>   VL=<0x0002>  [0x0040] 
        #    > (0x0028,0x0011) US Columns 	 VR=<US>   VL=<0x0002>  [0x0040] 
        #    > (0x0028,0x0034) IS Pixel Aspect Ratio 	 VR=<IS>   VL=<0x0004>  <1\1 > 
        #    > (0x0028,0x0100) US Bits Allocated 	 VR=<US>   VL=<0x0002>  [0x0008] 
        #    > (0x0028,0x0101) US Bits Stored 	 VR=<US>   VL=<0x0002>  [0x0008] 
        #    > (0x0028,0x0102) US High Bit 	 VR=<US>   VL=<0x0002>  [0x0007] 
        #    > (0x0028,0x0103) US Pixel Representation 	 VR=<US>   VL=<0x0002>  [0x0000] 
        #    > (0x7fe0,0x0010) OX Pixel Data 	 VR=<OB>   VL=<0x1000>  
        #
        #    > (0x00e1,0x0010) LO PrivateCreator 	 VR=<LO>   VL=<0x0008>  <ELSCINT1> 
        #    > (0x00e1,0x1040) SH Offset From CT MR Images 	 VR=<SH>   VL=<0x0000>  <> 
        #    > (0x07a1,0x0010) LO PrivateCreator 	 VR=<LO>   VL=<0x0008>  <ELSCINT1> 
        #    > (0x07a1,0x1013)  ? 	 VR=<UL>   VL=<0x0004>  [0x00081b2c] 
        #  ----:

        # There are some header and trailer records that are reported
        # with no leading spaces. 

        tmp_list = []
        new_item = True
        for line in self.dcdump_lines:
            if string.count(line, '----:') == 1:
                if new_item:
                    tmp_list.append([])
                    new_item = False
                else:
                    new_item = True
            elif len(line) > 0:
                if line[0] == ' ':
                    tmp_list[-1].append(line)

        self.dicom_dir_dict = {}
        for item in tmp_list:
            for record in item:
                if string.count(record,'Referenced File ID') == 1:
                    referenced_file_ID = string.split(record)[-2][1:]
            self.dicom_dir_dict[referenced_file_ID] = item
        #for key in self.dicom_dir_dict.keys():
        #    print '==========================='
        #    for record in self.dicom_dir_dict[key]:
        #        print record


    def slice_location_dir(self):
        # Sorts dicom_dir by slice location.
        self.slice_location_dict = {}
        for key in self.dicom_dir_dict.keys():
            for record in self.dicom_dir_dict[key]:
                if string.count(record, 'Slice Location') == 1:
                    location = string.atof(
                        string.replace(
                            string.split(record,'<')[-1], '>', '' ) )
                    self.slice_location_dict[location] = key
        #print self.slice_location_dict

def test():
    testfile = '/home/miller/data/cbir-images/S9267260/S197240/I00005'
    d = DICOM(testfile)
    #d.andump()
    #d.dcdump()
    #d.plot_dchist()
    print d.dckey('Rows'), d.dckey('Columns')
    print d.dcposn(0,0)

    d.dctopgm8('test.pgm8')
    im = Image.open('test.pgm8')
    #im.show()
    d.dctoraw('test.raw')

    print im.size
    width, height = im.size
    data = im.getdata()
    for i in range(width):
        for j in range(height):
            index = i * height + j
            i1, j1, x, y, z = d.dcposn(i,j)
            print x, y, z, data[index]

def test_dir():
    testfile = '/home/miller/data/cbir-images/S9267260/S197240/DIRFILE'
    #testfile = '/home/miller/data/cbir-images/S9267260/DIRFILE'
    d = DICOM(testfile)
    d.dicomdir()
            
def test_slice_location_dir():
    testfile = '/home/miller/data/cbir-images/S9267260/S197240/DIRFILE'
    #testfile = '/home/miller/data/cbir-images/S9267260/DIRFILE'
    d = DICOM(testfile)
    d.dicomdir()
    d.slice_location_dir()
            
if __name__ == '__main__':
    #test()
    #test_dir()
    test_slice_location_dir()

