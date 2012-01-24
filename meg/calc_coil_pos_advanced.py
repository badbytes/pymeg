#!/usr/bin/env python2

'''calc coil pos advanced. auto calc bad channels and dont use for localizing and transform'''

import os, sys, commands
from meg import badchannels_v2
from pdf2py import pdf

STAGE = os.environ['STAGE']
DATA = os.environ['DATA0']

commandstr = ''
for i in sys.argv[1::]:
    print 'COIL ARG:',i
    commandstr = commandstr+' '+i

print 'COMM:',commandstr
dataconv = sys.argv[8].replace('/','%').replace(' ','@')
pdfpath = DATA+'/'+sys.argv[4]+'/'+sys.argv[6]+'/'+dataconv+'/'+sys.argv[10]+'/'+sys.argv[12]

p = pdf.read(pdfpath)
p.data.setchannels('meg')
p.data.getdata(0,p.data.pnts_in_file)

b = badchannels_v2.initialize(hz_range=[1,200])
b.builder(p,distance=25)
chanlabels = p.data.channels.labellist

badchanformatted = ''
for i in b.badchannelindex:
    badchanformatted = badchanformatted+chanlabels[i]+':'
post = commands.getoutput('calc_coil_pos_orig'+commandstr+' -I '+badchanformatted)


#COIL ARG /opt/msw_danc/map/bin/calc_coil_pos
#COIL ARG -C
#COIL ARG Colorado_June2010
#COIL ARG -P
#COIL ARG 1345
#COIL ARG -S
#COIL ARG test
#COIL ARG -s
#COIL ARG 11/23/11 11:12
#COIL ARG -r
#COIL ARG 1
#COIL ARG -p
#COIL ARG e,rfhp1.0Hz,COH
#COIL ARG -X
#COIL ARG 1


#def state():
   #coilorder=(var1.get() + "," + var2.get() +  "," + var3.get() +  "," + var4.get() +  "," + var5.get())
   #chan2del=(t.get)
   #fileposted=post
   #os.system("calc_coil_pos " + " -C " + conf + post + " -X " + trans + " -O " + coilorder + " -I " + chan2del() + " -f" )
   #print "calc_coil_pos " + " -C " + conf + post + " -X " + trans + " -O " + coilorder + " -I " + chan2del() + " -f"
   ##calc_coil_pos  -C Colorado_Jan2010 -P 0000 -S SAD-AUDSEF -s "04/12/10 10:38" -r 1 -p e,rfhp1.0Hz,COH -X 1 -O 1,2,3,4,5 -I A195:A117 -f
#root.title('Coil Editor with channel remove')

#f = Frame(root, width=350, height=210)
#xf = Frame(f, relief=GROOVE, borderwidth=5)
#Label(xf, text="Channel Delete").pack(pady=10)
#t = StringVar()
#ent = Entry(xf, textvariable=t).pack(side=LEFT, padx=5, pady=8)
#t.set('A195:A117')
#Button(xf, text="Close", command=root.quit).pack(side=RIGHT, padx=5, pady=8)
#xf.place(relx=0.01, rely=0.525, anchor=NW)
#Label(f, text='Delete MEG Channels from Transform').place(relx=.06, rely=0.525,anchor=W)
#Button(xf, command=state, text='Transform').pack(side=RIGHT, padx=5, pady=8)
#f.pack()

#root.mainloop()


