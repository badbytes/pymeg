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
import numpy as np
from pylab import *

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
    
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as \
FigureCanvas
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")

        dic = {
            "on_auto_select_toggled" : self.test,
            "on_row-activated": self.test2,
            }

        self.builder.connect_signals(dic)
        
        self.create_draw_frame(None)
        self.channel_tree(None)

    def channel_tree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview1")
        self.dataList = gtk.ListStore(int,str)
        self.AddListColumn('Number', 0, self.View)
        self.AddListColumn('Label', 1, self.View)
        
        
        self.numchannels=np.size(self.data,1)#300
        self.chanlabels=np.arange(np.size(self.data,1))#300)
        
        for k in range(0,self.numchannels):
            iter = self.dataList.append([k,self.chanlabels[k]])

        self.View.set_model(self.dataList)
        print 'adding channels'

    def AddListColumn(self, title, columnId, viewtype):
        column = gtk.TreeViewColumn(title,gtk.CellRendererText(),text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        viewtype.append_column(column)
        viewtype.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    
    def test(self,widget):
        print 'test',widget
        toggled = widget #self.builder.get_object("togglebutton1")
        print toggled.get_active()#toggled()#state
        box_children = self.builder.get_object("buttonbox1").get_children()
        if toggled.get_active() == True:
            for i in box_children:
                i.set_sensitive(True)
        if toggled.get_active() == False:
            for i in box_children:
                i.set_sensitive(False)
        toggled.set_sensitive(True)
        
    def test2(self,widget):
        try: self.axes.clear()
        except: pass 
        self.axes.axis('off')
        self.axes.scatter(self.data[1],self.data[0],marker='o',facecolors='none');
        liststore,iter = self.View.get_selection().get_selected_rows()
        self.chanind = []
        for i in iter:
            print i,liststore[i][0]
            x = liststore[i][0]
            self.chanind.append(int(liststore[i][0]))
            self.axes.scatter(self.data[1,x],self.data[0,x],marker='o',color='r')
            
        self.canvas.draw()
        #self.canvas.show()
            
                
    def create_draw_frame(self,widget):
        #ion()
        self.fig = Figure(figsize=[200,200], dpi=100)
        self.canvas = FigureCanvas(self.fig)
        #self.canvas.connect("scroll_event", self.scroll_event)
        #self.canvas.connect('button_press_event', self.button_press_event)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], axisbg='#FFFFCC')
        self.axes.axis('off')
        self.vb = self.builder.get_object("viewport1")
        self.vb.add(self.canvas)
        #self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        self.vb.show()
        from pdf2py import readwrite
        self.data = readwrite.readdata('/home/danc/programming/python/chlocs.pym')
        #self.data = np.arange(300)#np.random.randn(300)
        self.axes.scatter(self.data[1],self.data[0],marker='o',facecolors='none');

if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
