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
import sys,time,os

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

class template:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        #spin = self.builder.get_object("spinner1")
        #spin.start()
        #self.window = builder.add_objects_from_file("/home/danc/python/pymeg/gui/gtk/spinner.glade",['window2'])
        self.window = self.builder.get_object("window")
        #self.spin = self.builder.get_object("buttonbox1")

        dic = {
            "on_button1_clicked" : self.test,
            }

        self.builder.connect_signals(dic)


    def test(self,widget,null):
        print 'test'
        #self.builder.get_object("spinner1").stop()

    def datahandler(data=None):
        pass


if __name__ == "__main__":
    mainwindow = template()
    mainwindow.window.show()

    print 'started'

    print 'testing'
    gtk.main()
    print 'done'

    #time.sleep(5)
    #spin.stop()
