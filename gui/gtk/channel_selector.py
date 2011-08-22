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

'''channel_selector.setup(chanlocs=[2 X NumChan],chanlabels=[list of channel labels]'''

import sys,os
import numpy as np
from pylab import *

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk,gobject
    import gtk.glade
except:
    print("GTK Not Availible")
    sys.exit(1)

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as \
FigureCanvas
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class setup:
    def __init__(self,chanlocs=None,chanlabels=None,result_handler=None):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window")
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_cid = self.statusbar.get_context_id("")
        try: self.data = chanlocs; self.chanlabels = chanlabels; self.result_handler = result_handler
        except: pass

        dic = {
            #"on_auto_select_toggled" : self.test,
            "on_selection": self.selection_made,
            "showpopupmenu" : self.showpopupmenu,
            "on_select_toggled" : self.select_toggled,
            #"on_checked_toggled" : self.select_checked,
            "on_view_label_toggle" : self.view_label_toggled,
            "on_apply_clicked" : self.apply_selection,
            }

        self.builder.connect_signals(dic)

        self.create_draw_frame(None)
        self.channel_tree(None)

    def select_toggled(self,widget):
        print 'wid stat',widget.get_active()
        liststore,iter = self.View.get_selection().get_selected_rows()
        if widget.get_active() == True:
            for i in iter:
                print i
                liststore[i][2] = True
                x = liststore[i][0]
                self.axes.scatter(self.data[1,x],self.data[0,x],marker='o',color='r')

        else:
            for i in iter:
                print i
                liststore[i][2] = False
                x = liststore[i][0]
                self.axes.scatter(self.data[1,x],self.data[0,x],marker='o')
        self.canvas.draw()
        self.get_checked_channels()

    def get_checked_channels(self):
        liststore = self.View.get_model()
        self.chanchecked = [] #index to checked channels
        for i in liststore:
            if i[2] == True:
                self.chanchecked = append(self.chanchecked,i[0])

        self.statusbar.push(self.statusbar_cid, 'Number of channels checked: '+str(len(self.chanchecked)))


    def channel_tree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview1")
        self.dataList = gtk.ListStore(int,str,gobject.TYPE_BOOLEAN)
        self.AddListColumn('Number', 0, self.View)
        self.AddListColumn('Label', 1, self.View)
        self.AddBoolColumn('Select', 2, self.View)
        self.numchannels=np.size(self.data,1)#300

        for k in range(0,self.numchannels):
            iter = self.dataList.append([k,self.chanlabels[k],k])
            self.dataList[k][2] = False


        self.View.set_model(self.dataList)
        print 'adding channels'

    def AddBoolColumn(self, title, columnId, viewtype):
        self.render = gtk.CellRendererToggle()
        self.render.set_property('activatable', True)
        self.render.connect( 'toggled', self.checkit, self.dataList )
        column = gtk.TreeViewColumn(title,self.render)#,text=columnId)
        column.set_resizable(True)
        column.add_attribute( self.render, "active", 2)
        column.set_sort_column_id(columnId)
        viewtype.append_column(column)
        viewtype.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def checkit(self,cell,path,model):
        model[path][2] = not model[path][2]
        print "Toggle '%s' to: %s" % (model[path][1], model[path][2],)
        if model[path][2] == True:
            x = model[path][0]
            self.axes.scatter(self.data[1,x],self.data[0,x],marker='o',color='r')
        self.canvas.draw()
        self.get_checked_channels()

    def AddListColumn(self, title, columnId, viewtype):
        column = gtk.TreeViewColumn(title,gtk.CellRendererText(),text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        viewtype.append_column(column)
        viewtype.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def selection_made(self,widget):
        liststore,iter = self.View.get_selection().get_selected_rows()
        self.channels_selected = [];
        for i in iter:
            x = liststore[i][0]
            self.channels_selected.append(int(liststore[i][0])) #index to channels selected.
            if liststore[i][2] == False:
                scat = self.axes.scatter(self.data[1,x],self.data[0,x],marker='o',color='magenta')
        try:
            for j in self.previter:
                if liststore[(j,)][2] == False:
                    x = liststore[(j,)][0]
                    scat = self.axes.scatter(self.data[1,x],self.data[0,x],marker='o')
        except AttributeError:
            print 'first click skip'
            pass

        self.previter = copy(iter)
        #print 'prev',type(self.previter),self.previter
        self.canvas.draw()
        self.statusbar.push(self.statusbar_cid, 'Number of channels selected: '+str(len(self.channels_selected)))

    def view_label_toggled(self,widget):
        liststore = self.View.get_model()
        if widget.get_active() == True:
            for i in liststore:
                xy = i[0]
                label = i[1]
                self.axes.text(self.data[1,xy],self.data[0,xy],label,fontsize=7)

        else:
            pass
        self.canvas.draw()

    def create_draw_frame(self,widget):
        self.fig = Figure(figsize=[200,200], dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0, 0, 1, 1], axisbg='#FFFFCC')
        self.axes.axis('off')
        self.vb = self.builder.get_object("viewport1")
        self.vb.add(self.canvas)
        self.vb.show()
        self.axes.scatter(self.data[1],self.data[0],marker='o');#,facecolors='none');

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menufunctions")
            print(widget, event)
            m.show_all()
            m.popup(None,None,None,3,0)
        if event.button == 1:
            ap = self.axes.get_position()
            x,y = self.canvas.get_width_height()
            posx = (event.x/x-.5)*(1/(ap.x1-ap.x0))*-1
            posy = ((event.y/y-.5)*(1/(ap.y0-ap.y1)))
            #posx = ((event.x/x)-ap.x0)*(1/(ap.x1-ap.x0))
            #posy = ((event.y/y)-(1-ap.y0))*(1/(ap.y0-ap.y1))
            print posx,posy
            from meg import nearest
            nx=nearest.nearest(self.data[0],posy)[0]
            ny=nearest.nearest(self.data[1],posx)[0]
            print nx,ny

    def apply_selection(self, widget):
        print 'Number of channels applied:',size(self.chanchecked,0)
        self.result_handler(self.chanchecked)
        return self.chanchecked

if __name__ == "__main__":
    from pdf2py import readwrite
    chanlocs = readwrite.readdata('/home/danc/python/chlocs.pym')
    chanlabels = []
    for i in arange(size(chanlocs,1)):
        chanlabels = append(chanlabels, 'A'+str(i))
    mainwindow = setup(chanlocs,chanlabels)
    mainwindow.window.show()
    print 'testing'
    gtk.main()
