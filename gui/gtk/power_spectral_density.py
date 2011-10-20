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
from numpy import ceil, sqrt, arange, random

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

class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")
        #self.window.connect('destroy', gtk.main_quit)

        dic = {
            "on_button1_clicked" : self.test,
            "on_display_spectral_power_clicked" : self.display_power_density,
            }

        self.builder.connect_signals(dic)
        self.populate_combo()

    def test(self,widget):
        print 'test'

    def datahandler(self,ddict,callback=None):
        self.chlabels=ddict['labellist']
        self.populate_combo(self.chlabels)
        self.builder.get_object('entry2').set_text(str(ddict['srate']))
        self.data = ddict['data_block']
        self.window.show()

    def display_power_density(self,widget):
        #self.create_draw_frame(widget)
        #return
        print 'trying'
        from pylab import psd,show,figure,ion,title
        nfft = int(self.builder.get_object('entry1').get_text())
        srate = float(self.builder.get_object('entry2').get_text())
        chind = self.chlabels.index(self.chan_sel);print 'chind',chind
        data = self.data[:,chind]
        print 'NFFT',nfft,'SRATE',srate



        #figure()
        f = figure(figsize=(20,10), dpi=45)
        #title('Spectral Power of Channel: '+self.chan_sel)
        a = f.add_subplot(111)
        pow,freq=psd(data, NFFT=nfft, Fs=srate)
        f.show()

        #from meg import plot2dgtk
        #plot2dgtk.makewin(data,plottype='psd',NFFT=nfft, Fs=srate)



        #show()

    #def create_draw_frame(self,widget):
        #print 'creating frame'
        #from matplotlib.figure import Figure
        #from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

        #self.fig = Figure(figsize=[500,500], dpi=40)
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.show()
        #self.figure = self.canvas.figure
        #self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], axisbg='#FFFFCC')
        #self.axes.axis('off')
        ##self.vb = self.builder.get_object("vbox1")
        ##self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        ##self.vb.show()
        #self.sp = self.fig.add_subplot(111);
        #self.canvas.draw()



    def populate_combo(self, chlabels=None):
        print 'populating channel list'
        if chlabels == None:
            chlabels = arange(50)
        combobox = self.builder.get_object("combobox1")
        combobox.clear()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_wrap_width(int(ceil(sqrt(len(chlabels)))))

        for n in chlabels: #range(50):
            liststore.append([n])
        combobox.set_model(liststore)
        combobox.connect('changed', self.changed_cb)
        combobox.set_active(0)
        return

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            print model[index][0], 'selected','index',index
            self.chan_sel = str(model[index][0])
        return

if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    ddict = {'labellist':['A1','A2'],'data_block':random.randn(1000,2),'srate':1000}
    mainwindow.datahandler(ddict)
    print 'testing'
    gtk.main()
