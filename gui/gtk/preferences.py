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
from pdf2py import readwrite

class prefs:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")

        try:
            self.prefs = readwrite.readdata(os.getenv('HOME')+'/.pymeg.pym')
            print 'reading pref file'
            for i in self.prefs.keys():
                try: self.builder.get_object(i).set_state(self.prefs[i])
                except: pass
                pass
                #i.set_state(self.prefs[i])
        except IOError:
            print 'no pref set.'
            self.prefs = {}

        dic = {
            "on_preference_toggled" : self.updateprefs,
            }

        self.builder.connect_signals(dic)

    def updateprefs(self,widget):
        self.prefs[gtk.Buildable.get_name(widget)] = widget.get_active()
        readwrite.writedata(self.prefs, os.getenv('HOME')+'/.pymeg')

if __name__ == "__main__":
    mainwindow = prefs()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
