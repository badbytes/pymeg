#!/usr/bin/env python

#new coil editor interface to give option to delete bad channels from transform
#written by dan collins 080115

from Tkinter import *
import commands
import os
root = Tk()
Label(root, text="COH Coil Selection").pack(pady=5)
post = commands.getoutput('get_PSsrp')
Label(root, text=post).pack(pady=30)
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
var5 = StringVar()
f1 = Frame(root, bd=2, relief=SUNKEN)
opt1 = OptionMenu(f1, var1, 1, 2, 3, 4, 5, 0)   
opt2 = OptionMenu(f1, var2, 1, 2, 3, 4, 5, 0)
opt3 = OptionMenu(f1, var3, 1, 2, 3, 4, 5, 0)
opt4 = OptionMenu(f1, var4, 1, 2, 3, 4, 5, 0)
opt5 = OptionMenu(f1, var5, 1, 2, 3, 4, 5, 0)
Label(f1, text='Coil Order').pack(side=LEFT, padx=5)
opt1.pack(side=LEFT, anchor=W)
opt2.pack(side=LEFT, anchor=W)
opt3.pack(side=LEFT, anchor=W)
opt4.pack(side=LEFT, anchor=W)
opt5.pack(side=LEFT, anchor=W)
var1.set(1)
var2.set(2)
var3.set(3)
var4.set(4)
var5.set(5)
f1.pack()

conf='Colorado_Jan2010 '
trans='1'

def state(): 
   coilorder=(var1.get() + "," + var2.get() +  "," + var3.get() +  "," + var4.get() +  "," + var5.get())
   chan2del=(t.get)
   fileposted=post
   os.system("calc_coil_pos " + " -C " + conf + post + " -X " + trans + " -O " + coilorder + " -I " + chan2del() + " -f" )
   print "calc_coil_pos " + " -C " + conf + post + " -X " + trans + " -O " + coilorder + " -I " + chan2del() + " -f" 
   #calc_coil_pos  -C Colorado_Jan2010 -P 0000 -S SAD-AUDSEF -s "04/12/10 10:38" -r 1 -p e,rfhp1.0Hz,COH -X 1 -O 1,2,3,4,5 -I A195:A117 -f
root.title('Coil Editor with channel remove')

f = Frame(root, width=350, height=210)
xf = Frame(f, relief=GROOVE, borderwidth=5)
Label(xf, text="Channel Delete").pack(pady=10)
t = StringVar()
ent = Entry(xf, textvariable=t).pack(side=LEFT, padx=5, pady=8)
t.set('A195:A117')
Button(xf, text="Close", command=root.quit).pack(side=RIGHT, padx=5, pady=8)
xf.place(relx=0.01, rely=0.525, anchor=NW)
Label(f, text='Delete MEG Channels from Transform').place(relx=.06, rely=0.525,anchor=W)
Button(xf, command=state, text='Transform').pack(side=RIGHT, padx=5, pady=8)
f.pack()

root.mainloop()


