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
import sys
from gtk import gdk
from numpy import * #fromstring, arange, int16, float, log10
from matplotlib import rcParams

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

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

class template:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("draw.glade")
        self.window = self.builder.get_object("window")

        dic = {
            "on_toolbutton_refresh_clicked" : self.generate_testdata,
            "on_button1_clicked" : self.generate_testdata,
            "on_vboxMain_button_press_event" : self.button_press_event,
            "on_vboxMain_button_release_event" : self.button_release_event,
            "on_vboxMain_drag" : self.drag_begin,
            "on_vboxMain_motion_notify_event" : self.drag_begin,
            "on_toolbar_clear_clicked" : self.clear_selections,
            "on_toolbar_zoomin_clicked" : self.zoomin_time,
            "on_toolbar_zoomout_clicked" : self.zoomout_time,
            "on_go_back_clicked" : self.go_back,
            "on_go_forward_clicked" : self.go_forward,
            "on_toolbutton_preferences_clicked" : self.preferences_open,
            "on_button_pref_apply_activate" : self.pref_apply,
            "set_channel_groups" : self.set_channel_groups,
            
            }

        self.builder.connect_signals(dic)
        self.create_draw_frame('none')
        self.space = 0
        self.generate_testdata(None)

    def create_draw_frame(self,widget):
        self.fig = Figure(figsize=[100,100], dpi=72)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.connect("scroll_event", self.scroll_event)
        #self.canvas.connect('button_press_event', self.button_press_event)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], axisbg='#FFFFCC')
        
        self.vb = self.builder.get_object("vboxMain")
        self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        self.vb.show()
    
    def preferences_open(self,widget):
        self.win_prefs = self.builder.get_object("window_prefs")
        self.win_prefs.show()
        self.channel_tree(None)
        
    def scroll_event(self, widget, event):
        if event.direction == gdk.SCROLL_UP:
            direction = 1
            self.space = self.space + .1*self.scalefact
        else:
            direction = -1
            self.space = self.space - .1*self.scalefact
        if self.space < 0:
            self.space = 0
        print 'space', self.space
        print (arange(0,size(self.data2plot,1))*(self.space))
        self.space_data()
        self.redraw(None)
        curpos = self.axes.get_position()
        l1 = curpos.x0
        b1 = curpos.y0
        w1 = curpos.x1
        h1 = curpos.y1
        
    def space_data(self):
        self.data2plot = self.data[self.tstart:self.tstop,self.chanind] + \
        (arange(0,size(self.data[self.tstart:self.tstop,self.chanind],1)) * \
        (self.space))
        
    
        
    def get_cursor_position(self,event):
        ap = self.axes.get_position()
        x,y = self.canvas.get_width_height()
        posx = ((event.x/x)-ap.x0)*(1/(ap.x1-ap.x0))
        posy = ((event.y/y)-(1-ap.y0))*(1/(ap.y0-ap.y1))
        self.sx = (posx*(self.time[-1]-self.time[0]))+self.time[0]
        self.sy = (posy*(self.data2plot.max()-self.data2plot.min()))+self.data2plot.min()
        print self.sx, self.sy
        
    def button_press_event(self,widget,event):
        self.get_cursor_position(event)
        print 'button pushed',event.button,event.type
        if event.type == gtk.gdk.BUTTON_PRESS:
            print "single click"
            if event.button == 1:
                #clicked line
                #self.axes.axvline(x=self.sx)
                self.xstart = self.sx
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            print "double click"
            #highlight channel
            #self.axes.axhspan(self.sy-1, self.sy+1, xmin=0, xmax=1, color='yellow')

        elif event.type == gtk.gdk._3BUTTON_PRESS:
            print "triple click. ouch, you hurt your user."
            
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 2:
            print 'highlighting channel'
            self.axes.axhspan(self.sy-self.scalefact, \
            self.sy+self.scalefact, xmin=0, xmax=1, color='g')
        
        #refresh canvas
        self.canvas.draw()
        
    def button_release_event(self,widget,event):
        pass
        self.get_cursor_position(event)
        #print event#.button
        if event.type == gtk.gdk.BUTTON_RELEASE and event.button == 1:
            self.axes.axvspan(ymin=0, ymax=1, xmin=self.xstart, xmax=self.sx, color='b')
            try: self.selections = vstack((self.selections,[self.xstart,self.sx]))
            except AttributeError: self.selections = array([[self.xstart,self.sx]])
            print 'sels',self.selections
            self.canvas.draw()
            
    def clear_selections(self,widget):
        del self.selections
        self.redraw(None)
        
    def drag_begin(self,widget,event):
        pass
        #self.get_cursor_position(event)
        
    def redraw(self,widget):
        #print 'button press'
        print len(self.time),self.data2plot.shape
        self.color = 'black'
        self.axes.cla()
        self.axes = self.figure.axes[0]
        self.axes.plot(self.time, self.data2plot,color=self.color)
        self.axes.axis('tight')
        #self.axes.axis('off')
        try:
            print 'd',self.selections
            for i in self.selections:
                self.axes.axvspan(ymin=0, ymax=1, xmin=i[0], xmax=i[1], color='b')
        except:
            pass
        self.canvas.draw()
        
    def zoomin_time(self,widget):
        startind = self.tstart;
        stopind = self.tstop-((self.tstop-self.tstart)/2)
        self.check_scale(startind,stopind)
        
    def zoomout_time(self,widget):
        startind = self.tstart;
        stopind = self.tstop+((self.tstop-self.tstart)*2)
        self.check_scale(startind,stopind)

    def go_forward(self,widget):
        startind = ((self.tstop-self.tstart)/2)+self.tstart;
        stopind = ((self.tstop-self.tstart)/2)+self.tstop;
        self.check_scale(startind,stopind)
        
    def go_back(self,widget):
        startind = self.tstart-((self.tstop-self.tstart)/2);
        stopind = self.tstop-((self.tstop-self.tstart)/2);
        self.check_scale(startind,stopind)

        
    def check_scale(self,startind,stopind):
        print 'req',startind,stopind, self.tstart,self.tstop
        if startind < 0:
            startind = 0
            stopind = self.tstop
        if stopind > len(self.t):
            startind = self.tstart
            stopind = len(self.t)
        if stopind < 0:
            stopind = self.tstop
        print 'set',startind,stopind,self.tstart,self.tstop
            
        self.tstart = startind
        self.tstop = stopind
        self.time = self.t[self.tstart:self.tstop]
        self.data2plot = self.data[self.tstart:self.tstop,self.chanind]
        self.space_data()
        self.redraw(None)
        
    def page_down(self,widget):
        pass
        
    def channel_tree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview1")
        self.dataList = gtk.ListStore(str,str)
        self.AddListColumn('Number', 0)
        self.AddListColumn('Label', 1)
        
        for k in range(0,self.numchannels):
            iter = self.dataList.append([k,'label'+str(k)])
            
        self.View.set_model(self.dataList)
        print 'adding channels'
        
    def AddListColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.View.append_column(column)
        self.View.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        
    def pref_apply(self, widget):
        liststore,iter = self.View.get_selection().get_selected_rows()
        self.chanind = []
        for i in iter:
            print i, liststore[i][1]
            self.chanind.append(int(liststore[i][0]))
            #print self.dataList.get_value(iter,0)
        print self.chanind
        self.space_data()
        self.redraw(None)
        
    def set_channel_groups(self,widget):
        print widget.get_label(), widget
        #for i in self.builder.get_object('vbox2').get_children():
            #if i.get_active() == True:
                #print(i)
                #print i.get_label()
        if widget.get_label() == 'meg' and widget.get_active() == True:
            #self.View.get_selection().select_all()
            #self.View.get_selection().select_all()
            self.View.get_selection().select_range(0,2)
        if widget.get_label() == 'Clear':
            self.View.get_selection().unselect_all()
        if widget.get_label() == 'all' and widget.get_active() == True:
            self.View.get_selection().select_all()
            
            
            

        
    def generate_testdata(self,widget):
        numpts = 10
        self.numchannels = 10
        self.t = arange(0,numpts, .01)
        self.data = zeros((len(self.t),self.numchannels))
        self.scalefact = 1e-9
        for i in arange(0,self.numchannels):
            r = random.randn()
            self.data[:,i] = float32((sin(2*0.32*pi*self.t*r) * sin(2*2.44*pi*self.t*r)))#+ self.space
        self.data = self.data * self.scalefact
        self.tstart = 0; self.tstop = len(self.t)
        self.time = copy(self.t[self.tstart:self.tstop])
        print self.tstart,self.tstop
        self.chanind = arange(0,self.numchannels)
        self.data2plot = self.data
        self.space_data()
        #self.time_view()
        self.redraw(None)
        
        


    def datahandler(data=None):
        pass


if __name__ == "__main__":
    mainwindow = template()
    mainwindow.window.show()
    print 'testing'
    gtk.main()
