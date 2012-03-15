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
        self.confirmoverwrite(None)

        dic = {
            "on_filechooserbutton1_file_set" : self.fileset,
            "on_filechooserbutton2_file_set" : self.fileset,
            "on_button1_clicked" : self.startdensity,
            "on_startdensity_clicked" : self.startdensity,
            #"on_radiobuttonfileopen_clicked" : self.loaddipolefiletoggle,
            #"on_radiobuttonselected_clicked" : self.selectedtoggle,
            "on_button1_clicked" : self.savemri,
            "on_button2_clicked" : self.cancel,
            "on_toggled" : self.item_select,
            "on_confirm-overwrite" : self.confirmoverwrite,
            "on_response" : self.response_test,

            }

        self.builder.connect_signals(dic)
        fcb1 = self.builder.get_object("fileopenitem")
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


    def item_select(self,widget):
        self.itemselected =  gtk.Buildable.get_name(widget).split('_')[1]
        for i in self.builder.get_object('vbuttonbox2').get_children():
            i.set_sensitive(False)
        self.paired_item = paired_item = self.builder.get_object(self.itemselected+'item')
        paired_item.set_sensitive(True)

        self.builder.get_object('startdensity').set_sensitive(True)
        self.builder.get_object('entry1').set_sensitive(True)
        self.builder.get_object('entry2').set_sensitive(True)

    def fileset(self,widget):
        fcb1 = self.builder.get_object("fileopenitem")
        fcb2 = self.builder.get_object("filechooserbutton2")
        if fcb1.get_uri() != None and fcb2.get_uri() != None:
            self.builder.get_object('entry1').set_sensitive(True)
            self.builder.get_object('entry2').set_sensitive(True)
            self.builder.get_object('startdensity').set_sensitive(True)

    #def loaddipolefiletoggle(self, widget):
        #self.builder.get_object("currentitem").set_sensitive(False)
        #self.builder.get_object("fileopenitem").set_sensitive(True)

    #def selectedtoggle(self, widget):
        #self.builder.get_object("currentitem").set_sensitive(True)
        #self.builder.get_object("fileopenitem").set_sensitive(False)

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
        from mri import img_nibabel as img
        from numpy import array, append, size, ones

        #import nifti
        gofscale = float(self.builder.get_object('entry1').get_text())
        sigma = int(self.builder.get_object('entry2').get_text())
        print self.builder.get_object("filechooserbutton2").get_filename()
        self.mrfilename = self.builder.get_object("filechooserbutton2").get_filename()
        #mr = nifti.NiftiImage(self.mrfilename)
        mr = img.loadimage(self.mrfilename)
        print 'loaded MRI',mr

        if self.itemselected == 'manual':
            points = array(eval(self.paired_item.get_text()))
            gof = ones(size(points,0))
        if self.itemselected == 'selected':
            points = self.data_selected
        if self.itemselected == 'fileopen':
            from pdf2py import lA2array, readwrite
            from meg import dipole

            datafile = self.builder.get_object("fileopenitem").get_filename()
            print 'datafile=',datafile

            try:
                lA = lA2array.calc(datafile)
            except AttributeError: #probably not an MEG 4D file, try parsereport
                lA = dipole.parsereport(datafile)
                lA.dips[:,1:4] = lA.dips[:,1:4]/100 #xyz in meters (this is the units in the 4D,lA file)

            points = lA.dips[:,1:4]*1000 # units in mm
            time = lA.dips[:,0]/1000 #in sec

            gof_ind = lA.labels.index('GoF')
            gof = lA.dips[:,gof_ind]

        from meg import dipole2densitynifti
        self.dipoledensityimage = dipole2densitynifti.handler(points,mr,gofscale,gof,sigma)

        self.fcd = self.builder.get_object("filechooserdialog1")

        self.fcd.set_current_name('*dd.nii.gz')
        self.fcd.set_do_overwrite_confirmation(True)
        filter = gtk.FileFilter()
        filter.set_name("Nifti files")
        filter.add_pattern("*nii.gz")
        filter.add_pattern("*nii")
        self.fcd.add_filter(filter)
        self.fcd.show()

        #uridefault = self.fcd.set_uri(self.fcd.get_current_folder_uri())
        newname = self.mrfilename.replace('nii.gz','dd.nii.gz')
        self.fcd.set_uri('file://'+self.mrfilename)
        print 'debug',self.mrfilename
        uridefault = self.fcd.get_current_folder_uri()
        print 'uri', uridefault
        #self.fcd.set_uri(uridefault)

    def savemri(self, widget):
        print 'debugsave',self.fcd.get_filename()
        if os.path.isfile(self.fcd.get_filename()):
            self.confirmoverwrite(None)

        else:
            self.fcd.hide()
            self.dipoledensityimage.to_filename(self.fcd.get_filename())

    def confirmoverwrite(self,widget):
        print 'confirming'
        self.x = self.builder.get_object("messagedialog1")
        self.x.show()

    def response_test(self,widget,null):
        pass
        print 'response',widget,'test',null
        #print self.x.response()
        print widget.get_events()
        widget.close()
        if null == -6:
            print 'quit'
        else:
            print 'overwriting'




if __name__ == "__main__":
    mainwindow = density()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
