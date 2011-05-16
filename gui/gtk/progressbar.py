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
import sys,os,time,gobject
import threading

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

class MainThread:
    def __init__(self):
        gtk.gdk.threads_init()
        self.builder = gtk.Builder()
        self.builder.add_from_file("progressbar.glade")
        self.window = self.builder.get_object("window1")
        self.progressbar = self.builder.get_object("progressbar")

    def pulse(self):
        self.progressbar.pulse()
        if self.still_working == False:
            #gtk.main_quit()
            self.window.hide()
            print 'quiting'
        return self.still_working # 1 = repeat, 0 = stop

    def fraction(self):
        self.progressbar.set_fraction(10)

    def main(self, function_passed=None, progresstype='pulse'):
        self.window.show()
        self.progressbar.show()
        self.window.connect('destroy', gtk.main_quit)
        WT = WorkerThread(function_passed, self)
        WT.start()
        if progresstype == 'pulse':
            gobject.timeout_add(100, self.pulse)
        if progresstype == 'fraction':
            self.fraction()
        gtk.main()

class WorkerThread(threading.Thread):
    def __init__ (self, function, parent):
        threading.Thread.__init__(self)
        self.function = function
        self.parent = parent

    def run(self): # when does "run" get executed?
        self.parent.still_working = True
        self.function()
        self.parent.still_working = False


if __name__ == '__main__':
    MT = MainThread()
    def testfunction():
        for i in range(0,50):
                print i;
                time.sleep(.1)
        gtk.main_quit()
    MT.main(testfunction)

