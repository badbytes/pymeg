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

from mri import img_nibabel as img
import nibabel
from mri import transform
from numpy import array, ndarray, float
from pdf2py import readwrite,pdf
from meg import grid
from gui.gtk import progressbar,viewmri
#from gui.gtk import progressbar

class gridwin():
    def __init__(self):
        #self.callback = callback
        MT = progressbar.MainThread()
        #
        self.datahandler()
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window1")
        n = self.builder.get_object('notebook1')
        self.statusbar = self.builder.get_object("statusbar1")
        self.statusbar_cid = self.statusbar.get_context_id("")
        #n.set_current_page(0)
        dic = {
            "on_button1_clicked" : self.mrigrid,
            "on_filechooserbutton1_file_set": self.coregistercheck,
            "on_filechooserbutton2_file_set": self.pdfcheck,
            #"on_button3_clicked" : self.coregister_handler,
            "on_radiobutton_clicked" : self.gridtypechanged,
            "on_button2_clicked" : self.manualgrid,

            }

        self.builder.connect_signals(dic)

        try:
            self.prevdata = readwrite.readdata(os.getenv('HOME')+'/.pymegdata.pym')
            print 'previous data', self.prevdata
            self.builder.get_object("filechooserbutton1").set_uri('file://'+self.prevdata['MRI'])
            #self.builder.get_object("filechooserbutton1").set_filename(self.prevdata['MRI'])
            #self.mr = img.loadimage(self.prevdata['brain.nii.gz'])
            filename = self.filename = self.prevdata['MRI']
            self.coregistercheck(None, filename)
            self.statusbar.push(self.statusbar_cid, 'Loading Previous MRI.')

            #try:
                #type(self.mr.lpa) == ndarray#type(eval(self.mr.description)[0]) == ndarray: #coregegistered mri
                #self.builder.get_object("button1").set_sensitive(True)
            #except:
                #self.builder.get_object("button1").set_sensitive(False)
        except (IOError, KeyError): #no last file
            print 'no prev data'
            self.prevdata = {}
        except TypeError:
            pass

    #def loadmr(self, filename):
        #self.mr = nibabel.load(filename)


    def datahandler(self,callback=None):
        self.callback = callback
        #if callback != None: self.callback = callback

    def coregister_handler(s195elf, widget):
        vm = viewmri.display()

    #def coregister_handler(self, widget):
        #self.cr = coregister.setup() #window
        #self.cr.window.show()
        #self.cr.builder.get_object('filechooserbutton1').set_uri(self.builder.get_object("filechooserbutton1").get_uri())

    def pdfcheck(self, widget):
        print 'pdfcheck'
        p = pdf.read(self.builder.get_object("filechooserbutton2").get_filename())
        print 'pdf to try and read', p
        self.headshape = p.hs
        print self.headshape,'headshape'

    def coregistercheck(self,widget,filename=None):
        print filename, 'fn'
        if self.builder.get_object("filechooserbutton1").get_filename() == None:
            pass
        else:
            filename = self.builder.get_object("filechooserbutton1").get_filename()

        print 'loading and checking coreg', filename
        try: self.mr = nibabel.load(filename)
        except RuntimeError: print 'unsupported MR file'; return

        self.prevdata['MRI'] = filename
        readwrite.writedata(self.prevdata, os.getenv('HOME')+'/.pymegdata')

        try:
            xfm = readwrite.readdata(os.path.splitext(filename)[0]+'.pym')
            print 'file previously coregistered', xfm
            self.builder.get_object("button1").set_sensitive(True)
        except:
            print 'cant find fiducal file', os.path.splitext(filename)[0]+'.pym';
            return

        self.lpa = xfm['lpa']
        self.rpa = xfm['rpa']
        self.nas = xfm['nas']


    #def coregistercheck(self,widget):
        #print 'filename ',self.builder.get_object("filechooserbutton1").get_filename()
        #try:
            ##self.mr = img.loadimage(self.builder.get_object("filechooserbutton1").get_filename())
            #self.mr = nibabel.load(self.builder.get_object("filechooserbutton1").get_filename())
            ##self.prevdata['brain.nii.gz'] = self.builder.get_object("filechooserbutton1").get_filename()
            #readwrite.writedata(self.prevdata, os.getenv('HOME')+'/.pymegdata')
        #except RuntimeError:
            #print('not a nifti image. exiting')
            #self.statusbar.push(self.statusbar_cid, 'Error. Not a Nifti file.')
            #self.builder.get_object("button1").set_sensitive(False)
            #self.builder.get_object("button3").set_sensitive(False)

        #try:
            #if type(eval(self.mr.description)[0]) == ndarray: #coregegistered mri
                #self.builder.get_object("button1").set_sensitive(True)
                #self.builder.get_object("button3").set_sensitive(True)
                #self.statusbar.push(self.statusbar_cid, 'File already coregistered.')
            #else:
                #self.builder.get_object("button1").set_sensitive(False)
                #self.statusbar.push(self.statusbar_cid, 'File description field does not contain fiducials.')
        #except TypeError:
            #pass
        #try:
            #mrfn = self.mr.file_map['header'].filename
            #readwrite.readdata(self.mr.file_map['header'].filename

    #def delay(self):
        #import time
        #if self.builder.get_object('radiobutton4').get_active() == True:
            #braintype = 'yes'
        #else:
            #braintype = 'no'

        #for i in range(1):
            #print i
            ##time.sleep(1)
        #from numpy import random
        #from pdf2py import pdf
        #from meg import leadfield
        #fn = '/home/danc/python/data/0611/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
        #p = pdf.read(fn);p.data.setchannels('meg')

        #lf = leadfield.calc(p.data.channels, grid=random.randn(3,10))
        #self.mr.decimate(int(self.builder.get_object('entry1').get_text()))
        #self.grid = (transform.scalesourcespace(self.headshape, self.mr.megxyz,
        #self.mr.lpa,self.mr.rpa,self.mr.nas,self.mr.pixdim,brain=braintype))
        #gtk.main_quit()

    def mrigrid(self,widget):
        print 'MRI source space computing'
        from numpy import shape
        self.mr = img.loadimage(self.filename)
        def gridthread():
            if self.builder.get_object('radiobutton4').get_active() == True:
                braintype = 'yes'
            else:
                braintype = 'no'
            self.mr.decimate(int(self.builder.get_object('entry1').get_text()))
            self.grid = (transform.scalesourcespace(self.headshape, self.mr.megxyz,
            self.mr.lpa,self.mr.rpa,self.mr.nas,self.mr.pixdim,brain=braintype))
            #except: print 'Error, aborting'; return
            print 'grid shape', shape(self.grid) #shape(self.workspace_data.results.grid)
            print self.callback
            self.gridcallback()

        MT = progressbar.MainThread()
        MT.main(gridthread)

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
            self.grid  = array(eval(self.builder.get_object("entry2").get_text()))
            print 'done point'
        elif manualtypeselected == 'Cube':
            self.grid = grid.cube(eval(self.builder.get_object("entry2").get_text()), \
            float(self.builder.get_object("entry3").get_text()), \
            float(self.builder.get_object("entry4").get_text()))
            print 'done cube'
        elif manualtypeselected == 'Sphere':
            self.grid = grid.sphere(eval(self.builder.get_object("entry2").get_text()), \
            float(self.builder.get_object("entry3").get_text()), \
            float(self.builder.get_object("entry4").get_text()))
            print 'done sphere'

        self.gridcallback()

    def gridcallback(self):
        if self.callback != None:
            self.callback(self.grid,mr=self.mr)
        else:
            return self.grid


if __name__ == "__main__":
    mainwindow = gridwin()
    mainwindow.window.show()
    gtk.main()
