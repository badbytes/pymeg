#       py2pdf.py
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

'''write py array as ascii file and import script'''

from numpy import size
import subprocess
import os
import stat
import time

def writeascdata(pydata, importfilename, ch, fileoutpath, pdfobjfilepath, pdfobj, samplerate, trigtime):
    '''py2pdf.writeascdata(x, importfilename, p.data.channels.channelsortedlabels,
     '/home/danc/testout', p.data.filepath, p)'''
    p = pdfobj
    numch = size(pydata,1)
    numpnts = size(pydata,0)
    fileout = open(fileoutpath,"w")
    fileout.write(str(numch)+'\n')
    fileout.write(str(numpnts)+'\n')
    for i in ch:
        fileout.write(i+'\t')
    fileout.write('\n')

    pydata.tofile(fileout, sep='\t', format="%s")

    #~ fileout.write(str(pydata))

    #~ for j in pydata:
        #~ fileout.write(str(j)+'\t')

    fileout.close()

    print fileoutpath+importfilename+'.importscript'
    scriptout = open(fileoutpath+'.importscript','w')
    #scriptout.write('clr_db_locks -P '+str(numch)+'\n')
    print pdfobjfilepath
    dataformated = pdfobjfilepath.split('/')[::-1][2].replace('%','/')
    dataformated = dataformated.replace('@',' ')
    scriptout.write('asc_to_pdf -P '+pdfobjfilepath.split('/')[::-1][4] + ' -S ' + \
    pdfobjfilepath.split('/')[::-1][3] + ' -s ' + '"'+dataformated+'"' + \
    ' -r '+pdfobjfilepath.split('/')[::-1][1] + ' -o '+ importfilename + \
    ' -f ' + fileoutpath + \
    ' -R ' + samplerate + ' -T ' + trigtime + '>/dev/null' + '\n')
    print scriptout
    scriptout.close()
    print fileoutpath+importfilename+'.importscript'

    os.chmod(fileoutpath+'.importscript', stat.S_IRWXU)

    #remove if exists
    subprocess.Popen('remover -P '+pdfobjfilepath.split('/')[::-1][4] + ' -S ' + \
    pdfobjfilepath.split('/')[::-1][3] + ' -s ' + '"'+dataformated+'"' + \
    ' -r '+pdfobjfilepath.split('/')[::-1][1] + ' -p '+ importfilename, shell=True, stdout=subprocess.PIPE)
    time.sleep(1)

    exescript = subprocess.Popen('/bin/sh '+fileoutpath+'.importscript', shell=True, stdout=subprocess.PIPE)
    print exescript.stdout.readlines()
    time.sleep(1)

    #os.remove(fileoutpath+'.importscript')
    #os.remove(fileoutpath)


#~ clr_db_locks -P "0868"
#~ remover -P "0868" -S "motcohsup1" -s "07/17/06 15:09" -r "1" -p "e,rfDC,n,bahe001-1Flexion,ica.3" > /dev/null
#~ asc_to_pdf -P "0868" -S "motcohsup1" -s "07/17/06 15:09" -r "1" -o "e,rfDC,n,bahe001-1Flexion,ica.3" -f 0868@motcohsup1@07-17-06_15.09@1@e,rfDC,n,bahe001-1Flexion,
#~ epochs.ica3 -R 508.629924 -T 1.500108 > /dev/null

#asc_to_pdf -P E-0051 -S MOTOR -s "08/17/09 16:00" -r 1 -o "x1avg" -f /home/danc/python/data/E0051/X1.outx2 -R 508.63 -T 1.376 > /dev/null
