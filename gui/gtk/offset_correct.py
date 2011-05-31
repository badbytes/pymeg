#!/usr/bin/python2
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
import os
from meg import offset,nearest
from numpy import array,vstack,copy

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")
    sys.exit(1)

class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("OffsetWindow")

        dic = {
            "on_dcoffset_clicked" : self.runoffsetcorrect,
            }

        self.builder.connect_signals(dic)

    def setupoffsetwin(self, widget, data, eventtime, frames, numofepochs, callback=None):
        print 'filter stuff'
        self.callback = callback
        self.data = data
        self.frames = frames
        self.numofepochs = numofepochs
        self.eventtime = eventtime
        try:
            self.builder.get_object('entry1').set_text(str(eventtime[0]))
            self.builder.get_object('entry2').set_text(str(eventtime[-1]))
            #self.builder.get_object('entry24').set_text(str(1/self.datadict[self.fn].data.hdr.header_data.sample_period[0]))
        except AttributeError:
            print 'no header loaded'

    def runoffsetcorrect(self,widget):#, callback=None):
        start = self.builder.get_object('entry1').get_text()
        end = self.builder.get_object('entry2').get_text()
        self.startind = nearest.nearest(self.eventtime,start)[0]
        self.endind = nearest.nearest(self.eventtime,end)[0]
        print 'offset correcting data', self.startind, self.endind
        for i in range(self.numofepochs):
            print 'epoch',i+1# i*self.frames, (i*self.frames)+self.frames, self.startind, self.endind
            epoch_data = self.data[i*self.frames:(i*self.frames)+self.frames,:]
            tmp = offset.correct(epoch_data, start=self.startind, end=self.endind)

            try: outdata = vstack((outdata,tmp))
            except UnboundLocalError: outdata = copy(tmp)

        try: self.callback(outdata)
        except (TypeError,NameError): pass

if __name__ == "__main__":
    mainwindow = setup_gui()
    from pdf2py import pdf
    fn = '/home/danc/python/data/0611/0611piez/e,rfhp1.0Hz,COH'
    #fn = '/home/danc/programming/python/data/0611/0611piez/e,rfhp1.0Hz,ra,f50lp,o'
    p = pdf.read(fn)
    p.data.setchannels('meg')
    p.data.getdata(0,p.data.pnts_in_file)
    mainwindow.setupoffsetwin(None,p.data.data_block, p.data.eventtime, p.data.frames, p.data.numofepochs)
    mainwindow.window.show()
    gtk.main()
