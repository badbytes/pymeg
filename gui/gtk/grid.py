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

from mri import img, transform
from numpy import array, ndarray, float
from pdf2py import readwrite
from meg import grid
import os
from gui.gtk import coregister

class gridwin:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("grid.glade")
        self.window = self.builder.get_object("window1")
        n = self.builder.get_object('notebook1')
        self.statusbar = self.builder.get_object("statusbar1")
        self.statusbar_cid = self.statusbar.get_context_id("")
        #n.set_current_page(0)
        dic = {
            "on_button1_clicked" : self.mrigrid,
            "on_filechooserbutton1_file_set": self.coregistercheck,
            "on_button3_clicked" : self.coregister_handler,
            "on_radiobutton_clicked" : self.gridtypechanged,
            "on_button2_clicked" : self.manualgrid,

            }

        self.builder.connect_signals(dic)

        try:
            self.prevdata = readwrite.readdata(os.getenv('HOME')+'/.pymegdata.pym')
            print 'previous data', self.prevdata
            self.builder.get_object("filechooserbutton1").set_uri('file://'+self.prevdata['brain.nii.gz'])
            self.builder.get_object("filechooserbutton1").set_filename(self.prevdata['brain.nii.gz'])
            self.mr = img.read(self.prevdata['brain.nii.gz'])
            self.statusbar.push(self.statusbar_cid, 'Loading Previous MRI.')
            if type(eval(self.mr.description)[0]) == ndarray: #coregegistered mri
                self.builder.get_object("button1").set_sensitive(True)
            else:
                self.builder.get_object("button1").set_sensitive(False)
        except IOError: #no last file
            print 'no prev data'
            self.prevdata = {}
        except TypeError:
            pass

    def coregister_handler(self, widget):
        self.cr = coregister.setup() #window
        self.cr.window.show()
        self.cr.builder.get_object('filechooserbutton1').set_uri(self.builder.get_object("filechooserbutton1").get_uri())


    def coregistercheck(self,widget):
        print 'p',self.builder.get_object("filechooserbutton1").get_filename()
        try:
            self.mr = img.read(self.builder.get_object("filechooserbutton1").get_filename())
            self.prevdata['brain.nii.gz'] = self.builder.get_object("filechooserbutton1").get_filename()
            readwrite.writedata(self.prevdata, os.getenv('HOME')+'/.pymegdata')
        except RuntimeError:
            print('not a nifti image. exiting')
            self.statusbar.push(self.statusbar_cid, 'Error. Not a Nifti file.')
            self.builder.get_object("button1").set_sensitive(False)
            self.builder.get_object("button3").set_sensitive(False)

        try:
            if type(eval(self.mr.description)[0]) == ndarray: #coregegistered mri
                self.builder.get_object("button1").set_sensitive(True)
                self.builder.get_object("button3").set_sensitive(True)
                self.statusbar.push(self.statusbar_cid, 'File already coregistered.')
            else:
                self.builder.get_object("button1").set_sensitive(False)
                self.statusbar.push(self.statusbar_cid, 'File not coregistered.')
        except TypeError:
            pass


    def mriwin(self,workspace_data=None):
        self.workspace_data = workspace_data
        self.builder.get_object('window1').show()


    def mrigrid(self,widget):
        print 'MRI source space computing'
        from numpy import shape
        dec = img.decimate(self.mr, int(self.builder.get_object('entry1').get_text()))
        print 'dec', dec
        lpa=eval(dec.origimg.description)[0]
        rpa=eval(dec.origimg.description)[1]
        nas=eval(dec.origimg.description)[2]
        [t,r] = transform.meg2mri(lpa,rpa,nas)
        dec.megxyz = transform.mri2meg(t,r,dec.mrixyz)
        print 'fn', self.workspace_data.data.filepath

        if self.builder.get_object('radiobutton4').get_active() == True:
            braintype = 'yes'
        else:
            braintype = 'no'


        #self.workspace_data.results.grid = transform.scalesourcespace(self.workspace_data.data.filepath, dec, brain=braintype)/1000
        self.workspace_data.results.grid = (transform.scalesourcespace
        (self.workspace_data.data.filepath, dec.megxyz, lpa,rpa,nas,dec.origimg.voxdim,brain=braintype)/1000)
        #(datapdf, megxyz, lpa, rpa, nas, voxdim, brain='no')
        print 'grid shape', shape(self.workspace_data.results.grid)

    def gridtypechanged(self, widget):
        print gtk.Buildable.get_name(widget)
        if widget.get_label() == 'Point':
            self.builder.get_object("entry3").set_sensitive(False);self.builder.get_object("entry4").set_sensitive(False)
        else:
            self.builder.get_object("entry3").set_sensitive(True);self.builder.get_object("entry4").set_sensitive(True)


    def manualgrid(self,widget):
        for i in self.builder.get_object('hbuttonbox3').get_children():
            if i.get_active() == True: manualtypeselected = i.get_label()

        #manualtypeselected = h.get_focus_child().get_label()
        if manualtypeselected == 'Point':
            self.workspace_data.results.grid = array(eval(self.builder.get_object("entry2").get_text()))
            print 'grid',self.workspace_data.results.grid
        elif manualtypeselected == 'Cube':
            self.workspace_data.results.grid = grid.cube(eval(self.builder.get_object("entry2").get_text()), \
            float(self.builder.get_object("entry3").get_text()), \
            float(self.builder.get_object("entry4").get_text()))
            print 'done cube'
        elif manualtypeselected == 'Sphere':
            self.workspace_data.results.grid = grid.sphere(eval(self.builder.get_object("entry2").get_text()), \
            float(self.builder.get_object("entry3").get_text()), \
            float(self.builder.get_object("entry4").get_text()))
            print 'done sphere'






if __name__ == "__main__":
    mainwindow = gridwin()
    mainwindow.window.show()
    gtk.main()
