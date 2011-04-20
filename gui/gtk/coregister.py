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

try:
    import nifti
except ImportError:
    try:
        from nibabel import nifti1 as nifti
    except:
        print 'Error Loading python nifti libraries'


from numpy import random, array, round

class setup:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window1")
        self.statusbar = self.builder.get_object("statusbar1")
        self.statusbar_cid = self.statusbar.get_context_id("")

        dic = {
            "on_button1_clicked" : self.viewmri,
            "on_checkbutton_toggled" : self.setfiducials,
            "on_saveimagebutton_clicked" : self.savefiducials ,
            }

        self.builder.connect_signals(dic)

    def viewmri(self,widget):
        print('test')

        from mri import viewmri
        mrfile = self.builder.get_object('filechooserbutton1').get_uri()#.set_uri('file:///'+self.dipoledata.datafile[0]))
        print(mrfile[7:])
        try:
            self.mr = nifti.NiftiImage(mrfile[7:])
            self.mp = viewmri.display(self.mr) #return mouse tracker position as mp
            for i in self.builder.get_object("hbuttonbox2").get_children(): i.set_sensitive(True)
        except RuntimeError:
            print('error. your file is not the expected nifti file type or corrupted')
            self.statusbar.push(self.statusbar_cid, 'Error. Not a Nifti file.')

    def setfiducials(self, widget):
        print widget.get_label()
        ind = array([self.mp.ind3,self.mp.ind2, self.mp.ind1]*array(self.mr.voxdim[::-1])) #get fiducals in mm by multiplying mouse position by reverse of voxdim as expressed in the nifti header.

        if widget.get_label() == 'LPA': self.lpa = round(ind)
        if widget.get_label() == 'RPA': self.rpa = round(ind)
        if widget.get_label() == 'NAS': self.nas = round(ind)

        for i in self.builder.get_object("hbuttonbox2").get_children(): #query that three boxes are checked
            if i.get_active() == False:
                self.builder.get_object("saveimagebutton").set_sensitive(False)
                return
        self.builder.get_object("saveimagebutton").set_sensitive(True)

    def savefiducials(self, widget):
        ind = str([self.lpa,self.rpa,self.nas]).replace(' ','')
        print 'ind',ind
        self.mr.setDescription(ind)
        print('saving mr with coregistration')
        self.mr.save()
        self.statusbar.push(self.statusbar_cid, 'Save complete.')


    def datahandler(data=None):
        pass



if __name__ == "__main__":
    mainwindow = setup()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
