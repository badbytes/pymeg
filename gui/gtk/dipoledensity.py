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

class density:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("dipoledensitywindow")

        dic = {
            "on_filechooserbutton1_file_set" : self.fileset,
            "on_filechooserbutton2_file_set" : self.fileset,
            "on_button1_clicked" : self.startdensity,
            "on_startdensity_clicked" : self.startdensity,
            "on_radiobuttonfileopen_clicked" : self.loaddipolefiletoggle,
            "on_radiobuttonselected_clicked" : self.selectedtoggle,
            "on_button1_clicked" : self.savemri,
            "on_button2_clicked" : self.cancel,

            }

        self.builder.connect_signals(dic)
        fcb1 = self.builder.get_object("filechooserbutton1")
        filter = gtk.FileFilter()
        filter.set_name("Dipole Files")
        filter.add_pattern("*lA")
        filter.add_pattern("*.drf")
        fcb1.add_filter(filter)
        fcb2 = self.builder.get_object("filechooserbutton2")
        filter = gtk.FileFilter()
        filter.set_name("Nifti files")
        filter.add_pattern("*nii.gz")
        filter.add_pattern("*nii")
        fcb2.add_filter(filter)



    def fileset(self,widget):
        fcb1 = self.builder.get_object("filechooserbutton1")
        fcb2 = self.builder.get_object("filechooserbutton2")
        if fcb1.get_uri() != None and fcb2.get_uri() != None:
            self.builder.get_object('entry1').set_sensitive(True)
            self.builder.get_object('entry2').set_sensitive(True)
            self.builder.get_object('startdensity').set_sensitive(True)

    def loaddipolefiletoggle(self, widget):
        self.builder.get_object("currentitem").set_sensitive(False)
        self.builder.get_object("filechooserbutton1").set_sensitive(True)
    def selectedtoggle(self, widget):
        self.builder.get_object("currentitem").set_sensitive(True)
        self.builder.get_object("filechooserbutton1").set_sensitive(False)

    def cancel(self, widget):
        import sys
        self.fcd.hide()

    def on_radiobuttonselected_group_changed(self,widget):
        vbb = self.builder.get_object('vbuttonbox1')
        for i in vbb.get_children():
            if i.active == True:
                pass

    def datahandler(workspace_data=None, data_selected=None):
        self.workspace_data = workspace_data
        self.data_selected = data_selected
        self.builder.get_object("currentitem").set_text(str(self.treedata))

    def startdensity(self, widget):
        from meg import density
        import nifti
        gofscale = float(self.builder.get_object('entry1').get_text())
        sigma = int(self.builder.get_object('entry2').get_text())
        print self.builder.get_object("filechooserbutton2").get_filename()
        self.mrfilename = self.builder.get_object("filechooserbutton2").get_filename()
        mr = nifti.NiftiImage(self.mrfilename)

        try:
            points = self.data_selected
        except AttributeError:
            from pdf2py import lA2array, readwrite
            from numpy import array, append, size
            from meg import dipole

            datafile = self.builder.get_object("filechooserbutton1").get_filename()
            print 'datafile=',datafile
            #if datafile[-2:] == 'lA':

            try:
                lA = lA2array.calc(datafile)
            except AttributeError: #probably not an MEG 4D file, try parsereport
                lA = dipole.parsereport(datafile)
                #lA.points = array([])
                lA.dips[:,1:4] = lA.dips[:,1:4]/100 #xyz in meters (this is the units in the 4D,lA file)

            points = lA.dips[:,1:4]*1000 # units in mm

            gof_ind = lA.labels.index('GoF')
            gof = lA.dips[:,gof_ind]

            from meg import dipole2densitynifti
            self.dipoledensityimage = dipole2densitynifti.handler(points,mr,gofscale,gof,sigma)

            self.fcd = self.builder.get_object("filechooserdialog1")
            self.fcd.show()
            self.fcd.set_current_name('*dd.nii.gz')
            filter = gtk.FileFilter()
            filter.set_name("Nifti files")
            filter.add_pattern("*nii.gz")
            filter.add_pattern("*nii")
            self.fcd.add_filter(filter)

            #uridefault = self.fcd.set_uri(self.fcd.get_current_folder_uri())
            self.fcd.set_uri('file://'+self.mrfilename)

            uridefault = self.fcd.get_current_folder_uri()
            print 'uri', uridefault
            self.fcd.set_uri(uridefault)

    def savemri(self, widget):
        self.dipoledensityimage.save(self.fcd.get_filename())
        self.fcd.hide()


if __name__ == "__main__":
    mainwindow = density()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
