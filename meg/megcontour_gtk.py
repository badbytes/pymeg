#!/usr/bin/env python

#import pylab as p
from pylab import *
import sys
try:
    sys.path.index('/usr/lib/python2.6')
except ValueError:
    try:
        from scikits.delaunay import *
        delaunay = 'yes'
    except:
        delaunay = 'no'
else: #using python 2.6
    from matplotlib.mlab import griddata
    delaunay = 'no'


try:
    import numpy.core.ma as ma
except ImportError:
    import numpy.ma as ma


import time
import gtk

from matplotlib.figure import Figure
from numpy import arange, sin, pi, random
from pylab import get_current_fig_manager

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
from numpy import shape, mgrid, interp, isnan, ceil, sqrt,arange , size

class makewin():
    def __init__(self):

        self.win = gtk.Window()
        #win.connect("destroy", lambda x: gtk.main_quit())
        self.win.connect("delete-event", self.hideinsteadofdelete)
        self.win.set_default_size(400,300)
        self.win.set_title("Embedding in GTK")

        vbox = gtk.VBox()
        self.win.add(vbox)

        self.f = Figure(figsize=(5,4), dpi=100)
        sw = gtk.ScrolledWindow()
        vbox.pack_start(sw)
        #self.win.add (sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width (10)
        # policy: ALWAYS, AUTOMATIC, NEVER
        sw.set_policy (hscrollbar_policy=gtk.POLICY_AUTOMATIC,
                       vscrollbar_policy=gtk.POLICY_ALWAYS)

        self.canvas = FigureCanvas(self.f)  # a gtk.DrawingArea
        #vbox.pack_start(canvas)
        self.canvas.set_size_request(300,200)
        sw.add_with_viewport (self.canvas)

        manager = get_current_fig_manager()
        # you can also access the window or vbox attributes this way
        toolbar = manager.toolbar

        #vbox.pack_start(canvas)
        toolbar = NavigationToolbar(self.canvas, self.win)
        vbox.pack_start(toolbar, False, False)

        self.win.show_all()
        #gtk.main()

    def hideinsteadofdelete(self,widget,ev=None):
        print widget
        widget.hide()
        return True


    def plot_data(self,xi,yi,zi,intx,inty):
        """provide...
            xi=grid x data
            yi=grided y data
            zi=interpolated MEG data for contour
            intx and inty= sensor coords for channel plotting"""

        tstart = time.time()

        zim = ma.masked_where(isnan(zi),zi)

        self.p.pcolor(xi,yi,zim,shading='interp',cmap=cm.jet)

        self.p.contourf(xi,yi,zim,cmap=cm.jet)
        self.p.scatter(intx,inty, alpha=.75,s=3)

    def plot_data_loop(self,xi,yi,zi,intx,inty):
        pass

    def printlabels(self,chanlocs, labels):
            #if labels != None:
        count = 0
        for l in labels:
            p.text(chanlocs[1,count], chanlocs[0,count], l, alpha=1, fontsize=9)
            count = count + 1

    def titles(titletxt):
        print

    def display(self, data, chanlocs, data2=None, subplot='off', animate='off', quiver='off', title=None, labels=None, colorbar='off'):
        #self.p = f.add_subplot(111)

        if len(shape(chanlocs)) != 2:
            print 'Chanlocs shape error. Should be 2D array "(2,N)"'
            print 'transposing'
            chanlocs = chanlocs.T
            print chanlocs.shape

        #xi, yi = mgrid[-.5:.5:67j,-.5:.5:67j]
        xi, yi = mgrid[chanlocs[1,:].min():chanlocs[1,:].max():57j,chanlocs[0,:].min():chanlocs[0,:].max():57j]
        intx=chanlocs[1,:]
        inty=chanlocs[0,:]

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
                zi = griddata(intx,inty,z,xi,yi)


            if animate == 'on': #single plot with a loop to animate
                p.scatter(intx,inty, alpha=.5,s=.5)
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
                    p.contourf(xi,yi,zim,cmap=p.cm.jet, alpha=.8)
                    if labels != None:
                        printlabels(chanlocs, labels)
                    p.draw()
            if subplot == 'on':
                print 'suplotting'
                for i in range(0, shape(data)[0]):
                    spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
                    #self.p = f.add_subplot(spnum,spnum,i+1)
                    self.p = self.f.add_subplot(spnum,spnum,i+1);#axis('off')
                    dataslice=data[i,:];
                    self.p.scatter(intx,inty, alpha=.75,s=3)
                    z = dataslice
                    if delaunay == 'yes':
                        interp = tri.nn_interpolator(z)
                        zi = interp(xi,yi)
                    else:
                        zi = griddata(intx,inty,z,xi,yi)

                    zim = ma.masked_where(isnan(zi),zi)
                    self.p.contourf(xi,yi,zim,cmap=cm.jet, alpha=.8)
                    self.p.axis('off')
                    if labels != None:
                        printlabels(chanlocs, labels)
                    if title != None:
                        self.p.title(str(title[i]))
                    else:
                        pass
                        #self.p.title(str(i))
            if quiver == 'on':
                print 'suplotting quiver'
                for i in range(0, shape(data)[0]):
                    spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
                    fig.add_subplot(spnum,spnum,i+1);#axis('off')
                    dataslice=data[i,:];
                    p.scatter(intx,inty, alpha=.75,s=3)
                    z = dataslice
                    print 'size or z', size(z)
                    for xx in range(0,size(z)):
                        quiver(intx[xx],inty[xx], z[xx], data2[xx])

                    p.axis('off')
                    if labels != None:
                        printlabels(chanlocs, labels)
            if colorbar == 'on':
                p.colorbar()

        else:
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
            if labels != None:
                printlabels(chanlocs, labels)

            if colorbar == 'on':
                p.colorbar(cm)
        self.canvas.draw()

if __name__ == '__main__':
    data = random.randn(10)
    m = makewin()
    from pdf2py import pdf
    fn = '/home/danc/data/meg/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
    p = pdf.read(fn)
    p.data.setchannels('meg')
    p.data.getdata(0,p.data.pnts_in_file)
    m.display(p.data.data_block[2:30:5,:],p.data.channels.chanlocs, subplot='on')
    #import code; code.interact(local=locals())

    gtk.main()
