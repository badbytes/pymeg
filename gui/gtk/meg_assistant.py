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
import sys,os
from pdf2py import pdf

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

class setup:
    def __init__(self, path=None,callback=None):
        self.callback=callback
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.assistant = self.builder.get_object("assistant1")

        dic = {
            "on_button1_clicked" : self.load_file,
            "on_checkbutton_toggled" : self.assistadvance,
            "on_assistant1_apply" : self.read_data,
            "on_assistant1_cancel" : self.hide_window,
            }

        self.builder.connect_signals(dic)
        self.builder.get_object("assistant1").show()
        self.load_file(path=path)

    def hide_window(self,widget):
        self.builder.get_object("assistant1").hide()


    def load_file(self,path=None):
        print 'loading file'
        self.assistant.set_page_complete(self.assistant.get_nth_page(0), True)
        self.pdfdata = pdf.read(path)
        self.ne = self.pdfdata.hdr.header_data.total_epochs[0]
        print 'ne',self.ne
        if self.ne > 1: #only load value in epochs
            self.builder.get_object("label32").set_text('First Epoch')
            self.builder.get_object("label33").set_text('Last Epoch')
            self.builder.get_object("entry29").set_text(str(0))
            self.builder.get_object("entry30").set_text(str(self.ne))
        else:
            self.builder.get_object("entry30").set_text(str(self.pdfdata.data.pnts_in_file[0]))
        self.path = path

    def read_data(self,path=None):

        chlabels = []
        for c in self.chanlist:
            self.pdfdata = pdf.read(self.path)
            print('c',c)
            self.pdfdata.data.setchannels(c)
            chlabels.extend(self.pdfdata.data.channels.labellist)
        print 'chlabels', chlabels
        self.pdfdata = pdf.read(self.path)
        startpnt = int(self.builder.get_object("entry29").get_text())
        if self.ne > 1: #only load value in epoch increments
            pntsinepoch = self.pdfdata.data.pnts_in_file/self.ne
            endepoch = int(self.builder.get_object("entry30").get_text())
            endpnt = pntsinepoch * endepoch

        else:
            endpnt = int(self.builder.get_object("entry30").get_text())
        self.pdfdata.data.setchannellabels(chlabels)
        self.pdfdata.data.getdata(startpnt,endpnt)
        self.pdfdata.data.wintime = self.pdfdata.data.wintime[startpnt:endpnt]
        self.builder.get_object("assistant1").hide()
        self.callback()
        return self.pdfdata
        sys.exit(0)

    def datahandler(data=None):
        pass

    def assistadvance(self,widget):
        self.chanlist = []
        print('something')
        for i in self.builder.get_object('table1'):
            if i.get_active() == True:
                self.chanlist.append(i.get_label())
        if len(self.chanlist) > 0:
            self.assistant.set_page_complete(self.assistant.get_nth_page(1), True)
            self.assistant.set_page_complete(self.assistant.get_nth_page(2), True)
        else:
            self.assistant.set_page_complete(self.assistant.get_nth_page(1), False)
        print(self.chanlist, 'selected')

if __name__ == "__main__":
    path = '/home/danc/python/data/0611/0611piez/e,rfhp1.0Hz,COH'
    #path = '/home/danc/python/data/0611/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
    #path = '/home/danc/data/0611/0611piez/e,rfhp1.0Hz,ra,f50lp,o'
    mainwindow = setup(path)
    mainwindow.assistant.show()
    gtk.main()

