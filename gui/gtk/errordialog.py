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

class errorwin:
    def __init__(self, errormesg):
        self.builder = gtk.Builder()
        self.builder.add_from_file("errordialog.glade")
        self.dialog = self.builder.get_object("errordialog1")
        #print 'You did something wrong, you moron!'
        self.dialog.set_property('text',errormesg)

        resp = self.dialog.run()
        if resp == -7:
            self.dialog.destroy()



if __name__ == "__main__":
    mainwindow = errorwin('test')
    #mainwindow.dialog.show()
    #x = mainwindow.dialog.run()
    #print x
    #if x == -7:
        #gtk.destroy()
        #mainwindow.dialog.destroy()
    gtk.main()
