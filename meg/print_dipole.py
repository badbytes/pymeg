#!/usr/bin/python
#       print_dipole.py
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

from numpy import *
import sys
from pdf2py import lA2array,pdf
from scipy.io.numpyio import *



try:
    fn = sys.argv[1]
    fswitch = sys.argv[2]
    fileoutput = sys.argv[3]
except IndexError:
    print 'use: print_dipole.py "path to lA file" -f output_file_name'
    sys.exit(-1)


p = pdf.read(fn)
p.data.setchannels('derived')
p.data.getdata(0, p.data.pnts_in_file)
x=p.data.hdr.proc_data[0]
#z=x.proc_step[1].user_data.split('\x00')
#z = remove_empty(z)
#pid = p.data.pid
#session = z[0]
#run = z[1]
#filename = z[2]
#z = x.proc_step[3].user_data.split('\x00') #channel data
#z = remove_empty(z)
dfa_info = x.proc_step[7].user_data.split('\x00')[0]

pid = p.data.pid
scan = p.data.scan
session = p.data.session
run = p.data.run
datafilename = p.data.filename

f = open(fileoutput, 'w')
f.write('Patient:\t'+pid+'\n')
f.write('Scan:\t'+scan+'\n')
f.write('Session:\t'+session+'\n')
f.write('Run:\t'+run+'\n')
f.write('Localization File:\t'+datafilename+'\n')
f.write('Grid Size:\t'+dfa_info)
f.write('Latency\tX\tY\tZ\tQx\tQy\tQz\tRadius\t||\tQ\t||\tRms\tCorr\tGof\tIter\n')
f.write('(msec)\t(cm)\t(nAm)\t(cm)\t(nAm)\tfT\n')
f.write('EPOCH 1\n')

d = lA2array.calc(fn)
d.dips[:,0] = d.dips[:,0]*1000 #latency
d.dips[:,1:4] = d.dips[:,1:4]*100
d.dips[:,4:7] = d.dips[:,4:7]*1e+9
d.dips[:,7] = d.dips[:,7]*100
d.dips[:,8] = d.dips[:,8]*1e+9
d.dips[:,9] = d.dips[:,9]*1e+15
dips = d.dips[:,0:13]

#fwrite(f, dips.shape[], device_data.Xfm, 'd', 1);
for i in range(0,size(dips,0)):
    for j in range(0, size(dips,1)):
        f.write(str(round(dips[i,j],3))+'\t')
    f.write('\n')

f.close()


#def remove_empty(data):
    #ret = True
    #while ret == True: #remove empty fields
        #try:
            #z.remove('')
        #except ValueError:
            #ret = False
    #return data


#def write_to_file(filename):
    #f = open(filename, 'w')




