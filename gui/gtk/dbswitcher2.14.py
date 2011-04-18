#!/usr/bin/python2
#       dbswitcher.py
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
#!/usr/bin/env python


import pygtk
pygtk.require('2.0')
import gtk, gtk.glade

from mswtools import vistadbscan
import subprocess, os


class cbtest:
    def __init__(self):
        self.scandbs = vistadbscan.run()
        print self.scandbs
        self.builder = gtk.Builder()



        self.builder.add_from_file("dbswitcher2.14.glade")
        self.window = self.builder.get_object("window1")
        self.window.show()
        self.box=self.builder.get_object("combobox1")
        cell = gtk.CellRendererText()
        self.box.pack_start(cell, True)
        self.box.add_attribute(cell, 'text', 0)
        store = gtk.ListStore(str)
        #self.builder.get_object("entry1").set_text('click test button')
        store.append(["Choose a Database"])
        dic = {
            "on_button1_clicked" : self.switchdbs,
            "on_combobox1_changed" : self.combobox1_changed,
            }
        self.builder.connect_signals(dic)

        for d in self.scandbs:
            store.append([d])   #note: append a list
        self.box.set_model(store)   #this replaces the model set by Glade
        self.box.set_active(0)
        self.box.show()

        curstage = os.environ['STAGE']
        self.builder.get_object("label2").set_label('Current DB: '+curstage)

    def combobox1_changed(self, box):
        self.model = box.get_model()
        self.index = box.get_active()
        if self.index:
            print  self.model[self.index][0], 'selected'
            self.dbselected = self.model[self.index][0]

    def on_window1_destroy(self,w):
        gtk.main_quit()



    def switchdbs(self, event): # wxGlade: MyDialog.<event_handler>

        subprocess.call(["killall", "psel"])

        print self.dbselected, 'selected'
        stage = os.environ['STAGE']
        try:
            os.remove(stage+'/map/database')
        except OSError:
            pass
        os.symlink(os.environ['HOME']+'/.mswhome/'+self.dbselected, stage+'/map/database')
        subprocess.Popen('psel', shell=True, stdout=subprocess.PIPE)
        self.builder.get_object("label2").set_label('Current DB: '+self.dbselected)

if __name__ == "__main__":
    cbtest()
    gtk.main()
