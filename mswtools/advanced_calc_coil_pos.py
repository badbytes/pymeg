#!/usr/bin/env python2

'''calc coil pos advanced. auto calc bad channels and dont use for localizing and transform'''

import os, sys, commands
from meg import badchannels_v2
from pdf2py import pdf

STAGE = os.environ['STAGE']
DATA = os.environ['DATA0']

dataconv = sys.argv[8].replace('/','%').replace(' ','@')
pdfpath = DATA+'/'+sys.argv[4]+'/'+sys.argv[6]+'/'+dataconv+'/'+sys.argv[10]+'/'+sys.argv[12]

p = pdf.read(pdfpath)
p.data.setchannels('meg')
p.data.getdata(0,p.data.pnts_in_file)

b = badchannels_v2.initialize(hz_range=[1,200])
b.builder(p,distance=25)
chanlabels = p.data.channels.labellist

commandstr = ''
sys.argv[8] = '"%s"' % sys.argv[8]
for i in sys.argv[1::]:
    print 'COIL ARG:',i
    commandstr = commandstr+' '+i

print 'COMM:',commandstr

badchanformatted = ''
for i in b.badchannelindex:
    badchanformatted = badchanformatted+chanlabels[i]+':'
    print 'BAD CHANNEL', chanlabels[i]
print 'DEBUG',commandstr+' -I '+badchanformatted
post = commands.getoutput('/opt/msw_danc/map/bin/calc_coil_pos.orig '+commandstr+' -I '+badchanformatted[:-1])

