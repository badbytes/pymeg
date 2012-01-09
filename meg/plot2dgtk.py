#!/usr/bin/env python
#       plot2dgtk.py
#
#       Copyright 2011 dan collins <danc@badbytes.net>
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

'''
demonstrate adding a FigureCanvasGTK/GTKAgg widget to a gtk.ScrolledWindow
'''

import gtk

from matplotlib.figure import Figure
from numpy import arange, sin, pi, random
from pylab import get_current_fig_manager, psd
from matplotlib.patches import Ellipse

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

class makewin():
    def __init__(self,data=None,xaxis=None,plottype='lines',labels=None,size=[700,500],NFFT=None, Fs=None):

        self.win = gtk.Window()
        #win.connect("destroy", lambda x: gtk.main_quit())
        self.win.connect("delete-event", self.hideinsteadofdelete)
        self.win.set_default_size(size[0],size[1])
        self.win.set_title("PyMEG Simple Plot")

        vbox = gtk.VBox()
        self.win.add(vbox)

        f = Figure(figsize=(500,500), dpi=75)
        a = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        #a.plot(t,s)

        if plottype == 'lines':
            a.plot(xaxis,data)
        if plottype == 'psd':
            a.psd(data,NFFT=NFFT, Fs=Fs)
        if plottype == 'empty':
            pass
        if plottype == 'imshow':
            timevals=xaxis
            extent=(int(timevals[0]), int(timevals[-1]),int(0), int(1));
            a.imshow(data,aspect='auto',extent=extent)

            el = Ellipse((.2, .1), 0.2, 0.2)
            a.annotate('Event', xy=(2, .5),  xycoords='data',\
            xytext=(0, 40), textcoords='offset points',\
                size=10, va="center",\
                bbox=dict(boxstyle="round", fc=(.5, 0.2, 0.2), ec="none"),\
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",\
                fc=(.5, 0.2, 0.2), ec="none",\
                patchA=None,\
                patchB=el,\
                relpos=(0.4, 0.5),\
                )\
                )

        #a.axis('off')
        self.plotted = f

        sw = gtk.ScrolledWindow()
        vbox.pack_start(sw)
        #self.win.add (sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width (10)
        # policy: ALWAYS, AUTOMATIC, NEVER
        sw.set_policy (hscrollbar_policy=gtk.POLICY_AUTOMATIC,
                       vscrollbar_policy=gtk.POLICY_ALWAYS)

        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        #vbox.pack_start(canvas)
        canvas.set_size_request(300,200)
        sw.add_with_viewport (canvas)

        manager = get_current_fig_manager()
        # you can also access the window or vbox attributes this way
        toolbar = manager.toolbar

        #vbox.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, self.win)
        vbox.pack_start(toolbar, False, False)

        self.win.show_all()
        #gtk.main()

    def hideinsteadofdelete(self,widget,ev=None):
        #print widget
        widget.hide()
        return True

if __name__ == '__main__':
    data = random.randn(10,10)
    xaxis = arange(0,10)
    makewin(data,xaxis,plottype='imshow',labels=None)
    #makewin(data,plottype='psd',labels=None)

    #import code; code.interact(local=locals())
    gtk.main()
