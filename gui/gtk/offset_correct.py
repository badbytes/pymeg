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

class offsetwin:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("offset_correct.glade")
        self.window = self.builder.get_object("OffsetWindow")

        dic = {
            "on_button1_clicked" : self.runoffsetcorrect,
            }

        self.builder.connect_signals(dic)

    def setupoffsetwin(self, widget, workspace_data=None, data_selected=None):
        print 'filter stuff'
        self.workspace_data = workspace_data
        self.data_selected = data_selected
        self.hdr = workspace_data.data.hdr
        self.builder.get_object('OffsetWindow').show()
        try:
            self.builder.get_object('entry1').set_text(str(self.workspace_data.data.eventtime[0]))
            #self.builder.get_object('entry24').set_text(str(1/self.datadict[self.fn].data.hdr.header_data.sample_period[0]))
        except AttributeError:
            print 'no header loaded'

    def runoffsetcorrect(self,widget):
        from meg import offset
        print 'offset correcting data', str(self.data_selected)
        self.workspace_data.results.offset_correct = offset.correct(self.data_selected, start=int(self.builder.get_object('entry1').get_text()), end=int(self.builder.get_object('entry2').get_text()))


