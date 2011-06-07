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

from pylab import *
import sys,os
try:
    sys.path.index('/usr/lib/python2.6')
except ValueError:
    try:
        from scikits.delaunay import *
        delaunay = 'yes'
    except ImportError:
        from matplotlib.mlab import griddata
        delaunay = 'no'
else: #using python 2.6
    from matplotlib.mlab import griddata
    delaunay = 'no'
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

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from numpy import shape, mgrid, interp, isnan, ceil, sqrt,arange , size
import time


class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window1")

        dic = {
            "on_subplot_clicked" : self.subplot_redraw,
            "on_animate_clicked" : self.animate_redraw,
            "on_quiver_clicked" : self.quiver_redraw,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            "on_menu_load_data_activate" : self.load_data,
            "on_menu_load_channels_activate" : self.load_channel_positions,
            "on_channellabels_toggled" : self.channel_labels_toggle,

            }

        self.builder.connect_signals(dic)
        self.create_draw_frame('none')

    def load_data(self,widget):
        pass

    def load_channel_positions(self,widget):
        pass

    def subplot_redraw(self,widget):
        self.fig.clf()
        self.display(self.data,self.chanlocs,subplot='on',labels=self.labels)

    def animate_redraw(self,widget):
        self.fig.clf()
        self.display(self.data,self.chanlocs,animate='on',labels=self.labels)

    def quiver_redraw(self,widget):
        self.fig.clf()
        self.display(self.data,self.chanlocs,data2=self.data[0],quiver='on',labels=self.labels)

    def channel_labels_toggle(self,widget):
        pass

    def hideinsteadofdelete(self,widget,ev=None):
        print 'hiding',widget
        widget.hide()
        return True

    def create_draw_frame(self,widget):
        self.fig = Figure(figsize=[500,500], dpi=40)
        self.canvas = FigureCanvas(self.fig)
        #self.canvas.connect("scroll_event", self.scroll_event)
        #self.canvas.connect('button_press_event', self.button_press_event)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], axisbg='#FFFFCC')
        self.axes.axis('off')
        self.vb = self.builder.get_object("vbox1")
        self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        self.vb.show()

    def plot_data(self,xi,yi,zi,intx,inty):
        """provide...
            xi=grid x data
            yi=grided y data
            zi=interpolated MEG data for contour
            intx and inty= sensor coords for channel plotting"""

        tstart = time.time()
        zim = ma.masked_where(isnan(zi),zi)
        self.sp.pcolor(xi,yi,zim,shading='interp',cmap=cm.jet)
        self.sp.contourf(xi,yi,zim,cmap=cm.jet)
        self.sp.scatter(intx,inty, alpha=.75,s=3)

    def plot_data_loop(self,xi,yi,zi,intx,inty):
        pass

    def clear_axes(self):
        pass

    def printlabels(self,chanlocs, labels):
            #if labels != None:
        count = 0
        for l in labels:
            self.sp.text(chanlocs[1,count], chanlocs[0,count], l, alpha=.6, fontsize=15)
            count = count + 1

    def titles(titletxt):
        print

    def display(self, data, chanlocs, labels, data2=None, subplot='off', animate='off', quiver='off', title=None, colorbar='off'):
        self.data = data
        self.chanlocs = chanlocs
        self.labels = labels
        if len(shape(chanlocs)) != 2:
            print 'Chanlocs shape error. Should be 2D array "(2,N)"'
            print 'transposing'
            chanlocs = chanlocs.T
            #print chanlocs.shape

        xi, yi = mgrid[chanlocs[1,:].min():chanlocs[1,:].max():57j,chanlocs[0,:].min():chanlocs[0,:].max():57j]
        intx=chanlocs[1,:]
        inty=chanlocs[0,:]

        labelstatus = self.builder.get_object('channellabels').get_active(); #print 'ls', labelstatus

        if shape(shape(data))[0]==2: #more than a single vector, need to animate or subplot
            print '2d array of data'
            z = data[0,:]
            if delaunay == 'yes':
                print 'delaunay is set'
                tri = Triangulation(intx,inty)
                interp = tri.nn_interpolator(z)
                zi = interp(xi,yi)
            else: #try griddata method
                print 'delaunay is off'
                try:
                    zi = griddata(intx,inty,z,xi,yi)
                except TypeError:
                    print('something wrong with data your trying to plot')
                    return -1

            if animate == 'on': #single plot with a loop to animate
                self.sp = self.fig.add_subplot(111);
                self.sp.scatter(intx,inty, alpha=.5,s=.5)
                print 'animating'
                for i in range(0, shape(data)[0]):
                    dataslice=data[i,:];
                    z = dataslice
                    if delaunay == 'yes':
                        interp = tri.nn_interpolator(z)
                        zi = interp(xi,yi)
                    else:
                        zi = griddata(intx,inty,z,xi,yi)

                    zim = ma.masked_where(isnan(zi),zi)
                    self.sp.contourf(xi,yi,zim,cmap=cm.jet)#, alpha=.8)
                    if labels != None and labelstatus == True:
                        self.printlabels(chanlocs, labels)
                    self.sp.axes.axis('off')
                    self.canvas.draw()

            if subplot == 'on':
                print 'suplotting'
                for i in range(0, shape(data)[0]):
                    spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
                    #self.p = f.add_subplot(spnum,spnum,i+1)
                    self.sp = self.fig.add_subplot(spnum,spnum,i+1);#axis('off')
                    dataslice=data[i,:];
                    self.sp.scatter(intx,inty, alpha=.75,s=3)
                    z = dataslice
                    if delaunay == 'yes':
                        interp = tri.nn_interpolator(z)
                        zi = interp(xi,yi)
                    else:
                        zi = griddata(intx,inty,z,xi,yi)

                    zim = ma.masked_where(isnan(zi),zi)
                    self.sp.contourf(xi,yi,zim,cmap=cm.jet, alpha=.8)
                    self.sp.axes.axis('off')
                    print 'plotting figure',i+1#len(labels), labelstatus
                    if labels != None and labelstatus == True:
                        self.printlabels(chanlocs, labels)
                    if title != None:
                        self.sp.title(str(title[i]))
                    else:
                        pass

            if quiver == 'on':
                print 'suplotting quiver'
                for i in range(0, shape(data)[0]):
                    spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
                    self.sp = self.fig.add_subplot(spnum,spnum,i+1);#axis('off')
                    dataslice=data[i,:];
                    self.sp.scatter(intx,inty, alpha=.75,s=3)
                    z = dataslice
                    print 'size or z', size(z)
                    for xx in range(0,size(z)):
                        self.sp.quiver(intx[xx],inty[xx], z[xx], data2[xx])

                    self.sp.axis('off')
                    if labels != None and labelstatus == True:
                        printlabels(chanlocs, labels)
                self.canvas.draw()

            if colorbar == 'on':
                self.sp.colorbar()

        else:
            self.sp = self.fig.add_subplot(111);
            z = data
            if delaunay == 'yes':
                print 'delaunay is set'
                tri = Triangulation(intx,inty)
                interp = tri.nn_interpolator(z)
                zi = interp(xi,yi)
            else:
                print 'delaunay is off'
                zi = griddata(intx,inty,z,xi,yi)

            zim = ma.masked_where(isnan(zi),zi)
            self.plot_data(xi,yi,zi,intx,inty)
            if labels != None and labelstatus == True:
                printlabels(chanlocs, labels)

            if colorbar == 'on':
                p.colorbar(cm)
            self.sp.axes.axis('off')
        self.canvas.draw()



if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    from pdf2py import pdf
    fn = '/home/danc/programming/python/data/0611/0611piez/e,rfhp1.0Hz,ra,f50lp,o'
    p = pdf.read(fn)
    p.data.setchannels('meg')
    p.data.getdata(0,p.data.pnts_in_file)
    mainwindow.display(p.data.data_block[2:20:5,:],p.data.channels.chanlocs, subplot='on',labels=p.data.channels.labellist)
    gtk.main()
