#!/usr/bin/python2
#!/usr/bin/env python
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
'''
Requires the following...
srate,timeaxes,data,chanlabels,
'''
import sys,os
from gtk import gdk
from numpy import * #fromstring, arange, int16, float, log10
from matplotlib import rcParams
from meg import nearest
from pylab import xticks,ion

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as \
FigureCanvas
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

#from meg import megcontour_gtk
from pdf2py import pdf
from gui.gtk import contour as contour_gtk
from gui.gtk import meg_assistant,event_process#,offset_correct

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
            "on_go_back_clicked" : self.page_back,
            "on_go_forward_clicked" : self.page_forward,
            "on_toolbutton_setup_toggled" : self.preferences_open,
            "on_button_channel_apply_clicked" : self.channel_selection_apply,
            "set_channel_groups" : self.set_channel_groups,
            "showpopupmenu" : self.showpopupmenu,
            "on_toolbar_plot_clicked" : self.plot_contour,
            "on_plot_contour_activate" : self.plot_contour,
            "on_button_delete_selection_clicked" : self.event_selection_delete,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            "on_button_display_apply_clicked": self.display_apply,
            "on_go_up_clicked" : self.page_up,
            "on_go_down_clicked" : self.page_down,
            "on_toolbutton_load_clicked" : self.load_data,
            "on_menu_offset_correct_clicked" : self.offset_correct,
            "on_button_epoch_clicked" : self.add_selections_to_event_process,
            "on_store_event_clicked" : self.store_event,
            "on_menu_save_noise_activate" : self.store_noise,
            "on_menu_save_event_activate" : self.store_event,
            "on_key_press_event" : self.key_press_event,

            }

        self.builder.connect_signals(dic)
        self.create_draw_frame('none')
        self.create_spec_frame('none')
        self.create_csd_frame('none')
        self.space = 0
        #self.generate_testdata(None)
        #self.preferences_open(None)

    def printtest(self,widget):
        print 'something'

    def store_noise(self,widget):
        print widget,'wid',widget.get_parent().get_name()
        self.callback(widget)

    def store_event(self,widget):
        print widget,'wid',widget.get_parent().get_name()
        self.callback(widget)

    def create_draw_frame(self,widget):
        self.fig = Figure(figsize=[100,100], dpi=40)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.connect("scroll_event", self.scroll_event)
        self.canvas.connect("key-press-event", self.key_press_event)
        #self.canvas.connect('button_press_event', self.button_press_event)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], \
        axisbg='#FFFFCC')

        self.vb = self.builder.get_object("vbox3")
        self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        self.vb.show()

    def create_spec_frame(self,widget):
        self.specfig = Figure(figsize=[10,10], dpi=40)
        self.specfig.text(0.25,0.5,'Middle Click Channel for Specgram',\
        fontsize=20)
        self.speccanvas = FigureCanvas(self.specfig)
        self.speccanvas.show()
        self.specfigure = self.speccanvas.figure
        self.specaxes = self.specfig.add_axes([0.045, 0.05, 0.93, 0.925], \
        axisbg='#FFFFCC')
        #self.specaxes.axis('off')
        self.vb2 = self.builder.get_object("vbox8")
        self.vb2.pack_end(self.speccanvas, gtk.TRUE, gtk.TRUE)
        self.vb2.show()

    def create_csd_frame(self,widget):
        self.csdfig = Figure(figsize=[10,10], dpi=40)
        self.csdfig.text(0.25,0.5,'Middle Click Channel for CSD',fontsize=20)
        self.csdcanvas = FigureCanvas(self.csdfig)
        self.csdcanvas.show()
        self.csdfigure = self.csdcanvas.figure
        self.csdaxes = self.csdfig.add_axes([0.045, 0.05, 0.93, 0.925], \
        axisbg='#FFFFCC')
        #self.csdaxes.axis('off')
        self.vb3 = self.builder.get_object("vbox9")
        self.vb3.pack_end(self.csdcanvas, gtk.TRUE, gtk.TRUE)
        self.vb3.show()

    def data_loaded_setup(self):
        self.channel_tree(None)
        self.builder.get_object("spinbutton1").set_range(0,self.numchannels)
        self.builder.get_object("spinbutton1").set_value(self.numchannels)
        self.builder.get_object("spinbutton2").set_range(self.t[0],self.t[-1])
        self.builder.get_object("spinbutton2").set_value(self.t[0])
        self.builder.get_object("spinbutton3").set_range(self.t[0],self.t[-1])
        #if self.t[-1] - self.t[0] > 1: #alot of time, save time in plotting and set low
        if len(self.t) > 1000:
            self.builder.get_object("spinbutton3").set_value(self.t[1000])
            print '.....reducing time var'
        else:
            print '.....showing all time'
            self.builder.get_object("spinbutton3").set_value(self.t[-1])
        #self.builder.get_object("spinbutton3").set_value(self.t[-1])
        #self.builder.get_object("spinbutton5").set_value(self.scalefact)
        self.builder.get_object("entry1").set_text(str(self.space))
        self.builder.get_object("entry2").set_text(str(self.scalefact))

    def preferences_open(self,widget):
        self.win_prefs = self.builder.get_object("window_prefs")
        if self.builder.get_object('toolbutton12').get_active() == True:
            self.win_prefs.show()
        else:
            self.win_prefs.hide()
        self.selections_tree(None)

    def key_press_event(self, widget, event):
        print event.keyval

    def scroll_event(self, widget, event):
        if event.direction == gdk.SCROLL_UP:
            direction = 1
            self.space = self.space + .5*self.scalefact
            print 'sf',self.scalefact
        else:
            direction = -1
            self.space = self.space - .5*self.scalefact
            print 'sf',self.scalefact
        if self.space < 0:
            self.space = 0
        print 'space', self.space
        #print (arange(0,size(self.data2plot,1))*(self.space))
        self.space_data()
        self.redraw(None)

    def space_data(self,space=None):
        self.data2plot = self.data[self.tstart:self.tstop,self.chanind2plot]+\
        (arange(0,size(self.data[self.tstart:self.tstop,self.chanind2plot],1))*\
        (self.space))

    def get_cursor_position(self,event):
        ap = self.axes.get_position()
        x,y = self.canvas.get_width_height()
        posx = ((event.x/x)-ap.x0)*(1/(ap.x1-ap.x0))
        posy = ((event.y/y)-(1-ap.y0))*(1/(ap.y0-ap.y1))
        self.sx = (posx*(self.time[-1]-self.time[0]))+self.time[0]
        self.sy = (posy*(self.data2plot.max()-self.data2plot.min())) + \
        self.data2plot.min()
        #print self.sx, self.sy

    def button_press_event(self,widget,event):
        self.get_cursor_position(event)
        #print 'button pushed',event.button,event.type
        if event.type == gtk.gdk.BUTTON_PRESS:
            print "single click"
            if event.button == 1:
                self.xstart = self.sx
        #elif event.type == gtk.gdk._2BUTTON_PRESS:
            #print "double click"
        #elif event.type == gtk.gdk._3BUTTON_PRESS:
            #print "triple click. ouch, you hurt your user."

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 2:
            closest_data = nearest.nearest(self.data2plot[0,:],self.sy)
            print 'nearest',closest_data
            print 'highlighting channel'
            self.axes.axhspan(self.data2plot[:,closest_data].min(), \
            self.data2plot[:,closest_data].max(), xmin=0, xmax=1, color='g',\
            alpha=0.2)
            self.canvas.draw()
            self.specaxes.cla()
            NFFT = 1024
            Fs = self.srate #(1/self.srate)
            print NFFT,int(Fs),'d'

            self.specaxes.specgram(
            self.data2plot[:,closest_data[0]], NFFT=NFFT, Fs=Fs,noverlap=900)
            #self.specaxes.axis('off')
            self.speccanvas.draw()

            self.csdaxes.csd(self.time,
            self.data2plot[:,closest_data[0]], NFFT=NFFT, Fs=Fs)
            #, noverlap=Noverlap,
            #cmap=cm.jet)#, xextent=xextent)
            #self.csdaxes.axis('off')
            self.csdcanvas.draw()

    def button_release_event(self,widget,event):
        self.get_cursor_position(event)
        if event.type == gtk.gdk.BUTTON_RELEASE and event.button == 1:
            self.axes.axvspan(ymin=0, ymax=1, xmin=self.xstart, xmax=self.sx, \
            color='b',alpha=0.4)
            if self.xstart > self.sx: #selection going from later to earlier
                tmp = copy(self.sx)
                self.sx = copy(self.xstart)
                self.xstart = tmp

            try: self.selections = vstack((self.selections,\
            [self.xstart,self.sx]))
            except AttributeError: self.selections = \
            array([[self.xstart,self.sx]])
            print 'sels',self.selections
            self.canvas.draw()
            self.selections_tree(None)

    def clear_selections(self,widget):
        del self.selections
        self.redraw(None)

    def drag_begin(self,widget,event):
        pass

    def redraw(self,widget):
        print len(self.time),self.data2plot.shape
        #self.color = 'black'
        self.axes.cla()
        self.axes = self.figure.axes[0]
        self.axes.plot(self.time, self.data2plot,color=self.color)
        self.axes.axis('tight')
        try:
            print 'current selections',self.selections
            for i in self.selections:
                self.axes.axvspan(ymin=0,ymax=1,xmin=i[0],xmax=i[1],color='b',\
                alpha=.4)
        except:
            pass
        self.axes.yaxis.set_ticks((arange(0,size(self.data2plot,1)) * \
        (self.space)))
        self.axes.yaxis.set_ticklabels(self.chanlabels2plot, fontsize=17)
        self.canvas.draw()
        ion()

    def zoomin_time(self,widget):
        startind = self.tstart;
        stopind = self.tstop-((self.tstop-self.tstart)/2)
        self.check_scale(startind,stopind)
        self.redraw(None)

    def zoomout_time(self,widget):
        startind = self.tstart;
        stopind = self.tstop+((self.tstop-self.tstart)*2)
        self.check_scale(startind,stopind)
        self.redraw(None)

    def page_forward(self,widget):
        startind = ((self.tstop-self.tstart)/2)+self.tstart;
        stopind = ((self.tstop-self.tstart)/2)+self.tstop;
        self.check_scale(startind,stopind)
        self.redraw(None)

    def page_back(self,widget):
        startind = self.tstart-((self.tstop-self.tstart)/2);
        stopind = self.tstop-((self.tstop-self.tstart)/2);
        self.check_scale(startind,stopind)
        self.redraw(None)

    def page_up(self,widget):
        self.curchannel = self.curchannel+self.numofch
        if self.curchannel >= len(self.chanind):
            self.curchannel = len(self.chanind)-self.numofch

        self.chanind2plot = \
        self.chanind[self.curchannel:self.curchannel+self.numofch]
        self.chanlabels2plot = \
        self.chanlabels[self.curchannel:self.curchannel+self.numofch]
        self.check_scale(self.tstart,self.tstop)
        self.redraw(None)#self.display_apply(None)

    def page_down(self,widget):
        self.curchannel = self.curchannel-self.numofch
        if self.curchannel < 0:
            self.curchannel = 0

        self.chanind2plot = \
        self.chanind[self.curchannel:self.curchannel+self.numofch]
        self.chanlabels2plot = \
        self.chanlabels[self.curchannel:self.curchannel+self.numofch]
        self.check_scale(self.tstart,self.tstop)
        self.redraw(None)#self.display_apply(None)

    def display_apply(self,widget):
        self.numofch = int(self.builder.get_object("spinbutton1").get_value())
        self.chanind2plot = \
        self.chanind[self.curchannel:self.curchannel+self.numofch]
        self.chanlabels2plot = \
        self.chanlabels[self.curchannel:self.curchannel+self.numofch]
        color = self.builder.get_object('colorbutton1')
        r = color.get_color().red_float
        g = color.get_color().green_float
        b = color.get_color().blue_float
        self.color = (r,g,b)
        st = float(self.builder.get_object("spinbutton2").get_value())
        ed = float(self.builder.get_object("spinbutton3").get_value())
        self.space = float(self.builder.get_object("entry1").get_text())
        self.scalefact = float(self.builder.get_object("entry2").get_text())
        #print 'se',st,ed, self.t
        startind = nearest.nearest(self.t,st)[0]
        stopind = nearest.nearest(self.t,ed)[0]
        print 'se',startind,stopind
        self.check_scale(startind,stopind)
        self.space_data()
        self.redraw(None)

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
        self.data2plot = self.data[self.tstart:self.tstop,self.chanind2plot]
        self.space_data()
        #self.redraw(None)


    def channel_tree(self,widget):
        print('updating list')
        self.View = self.builder.get_object("treeview1")
        self.dataList = gtk.ListStore(int,str)
        self.AddListColumn('Number', 0, self.View)
        self.AddListColumn('Label', 1, self.View)

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


    def channel_selection_apply(self, widget):
        liststore,iter = self.View.get_selection().get_selected_rows()
        self.chanind = [];
        self.chanlabels = [];
        for i in iter:
            self.chanind.append(int(liststore[i][0]))
            self.chanlabels.append(liststore[i][1])
        print self.chanlabels

        self.chanind2plot = self.chanind
        self.chanlabels2plot = self.chanlabels
        self.space_data()
        self.redraw(None)

    def set_channel_groups(self,widget):
        l = self.View.get_model()
        i = l.get_iter_first()
        v = []
        while ( i != None ):
            v.append(l.get_value(i,1))
            i = l.iter_next(i)

        print widget.get_label(), widget
        if widget.get_label() == 'meg' and widget.get_active() == True:
            for i in range(0,len(v)):
                if v[i].startswith('A'):
                    self.View.get_selection().select_path(i)
        if widget.get_label() == 'De-Select All':
            self.View.get_selection().unselect_all()
        if widget.get_label() == 'Select All':
            self.View.get_selection().select_all()
        if widget.get_label() == 'reference' and widget.get_active() == True:
            for i in range(0,len(v)):
                if v[i].startswith('M') or v[i].startswith('G'):
                    self.View.get_selection().select_path(i)
        if widget.get_label() == 'trigger' and widget.get_active() == True:
            for i in range(0,len(self.chanlabels)):
                if v[i].startswith('TRIGG'):
                    self.View.get_selection().select_path(i)
        if widget.get_label() == 'response' and widget.get_active() == True:
            for i in range(0,len(v)):
                if v[i].startswith('RESP'):
                    self.View.get_selection().select_path(i)


    def selections_tree(self,widget):
        try:
            if self.win_prefs.get_property('visible') == True:
                print('updating selections')
                self.SelView = self.builder.get_object("treeview2")
                self.selectionList = gtk.ListStore(int,str)

                if self.SelView.get_columns() == []:
                    self.AddListColumn('Event Number', 0,self.SelView)
                    self.AddListColumn('Selection', 1,self.SelView)

                for k in range(0,len(self.selections)):
                    iter=self.selectionList.append([k,str(self.selections[k])])
                self.SelView.set_model(self.selectionList)
                print 'adding selections'

        except AttributeError:
            pass #window not initiated yet

    def event_selection_delete(self, widget):
        liststore,iter = self.SelView.get_selection().get_selected_rows()
        #self.selections = delete(self.selections,iter,axis=0)
        del_ind = []
        for i in iter:
            print 'deleting event:',liststore[i][0]
            del_ind.append(liststore[i][0])
        self.selections = delete(self.selections,del_ind,axis=0)
        self.selections_tree(None)
        self.redraw(None)

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menufunctions")
            print(widget, event)
            m.show_all()
            m.popup(None,None,None,3,0)

    def get_time_selection(self,widget,current=True):
        print 'name',widget.get_parent().get_name()
        sel_ind = []
        sel_onset_ind = []
        def selection_to_ind(sels,sele,inc):
            print 'getting sel'
            if sele == sels: #only one point selected
                sele = sels+inc

            nearest.nearest(self.t,arange(sels,sele,inc))
            sel_ind = nearest.nearest(self.t,arange(sels,sele,inc))
            return sel_ind
        if widget.get_parent().get_name() == 'GtkMenu' and current == True: #call from editor menu
            print 'call from right click menu'
            try:
                self.sel_ind = selection_to_ind(self.selections[-1][0],\
                self.selections[-1][1],self.t[1]-self.t[0])
            except AttributeError:
                print 'no selections yet'
                return -1

        else: #call from selector
            print 'call from selector window'
            liststore,iter = self.SelView.get_selection().get_selected_rows()
            for i in iter:
                j = int(liststore[i][0])
                sel_ind.extend(selection_to_ind(self.selections[j][0],\
                self.selections[j][1],self.t[1]-self.t[0]))
                sel_onset_ind.extend(selection_to_ind(self.selections[j][0],\
                self.selections[j][0],self.t[1]-self.t[0]))
            self.sel_ind = sel_ind
            self.sel_onset_ind = sel_onset_ind

    def plot_contour(self,widget):
        if size(self.data,1) < 4:
            self.builder.get_object("messagedialog1").format_secondary_text\
            ('Contour Plot Requires at least 4 Channels')
            self.builder.get_object("messagedialog1").show()
            return -1
        print widget.get_parent().get_name()
        if self.get_time_selection(widget) == -1: #no selections
            self.builder.get_object("messagedialog1").format_secondary_text\
            ('No Selection Made Yet')
            self.builder.get_object("messagedialog1").show()
            return -1
        try:
            print 'state',self.mc.window.get_property('visible')
            if self.mc.window.get_property('visible') == False:
                #someone closed the window
                self.mc.window.show()
            print 'done replotting'
        except AttributeError: #first call. setup
            print 'first plot'
            self.mc = contour_gtk.setup_gui()
            self.mc.window.show()

        self.mc.fig.clf()
        self.mc.display(self.data[self.sel_ind,:],self.channels, subplot='on', labels=self.chanlabels)

    def generate_testdata(self,widget):
        self.quick_load_pdf_script()
        #numpts = 100
        #self.numchannels = 10
        #self.t = arange(0,numpts, .01)
        #self.data = zeros((len(self.t),self.numchannels))
        #self.scalefact = 1e-9
        #for i in arange(0,self.numchannels):
            #r = random.randn()
            #self.data[:,i] = float32((sin(2*0.32*pi*self.t*r) * \
            #sin(2*2.44*pi*self.t*r)))#+ self.space
        #self.data[:,0] = random.randn((len(self.t)))
        #self.data = self.data * self.scalefact
        #self.tstart = 0; self.tstop = len(self.t)
        #self.time = copy(self.t[self.tstart:self.tstop])
        #print self.tstart,self.tstop
        #self.chanind = arange(0,self.numchannels)
        #self.chanlabels = arange(0,self.numchannels)
        self.data2plot = self.data
        self.display_apply(None)
        #self.space_data()
        #self.redraw(None)

    def quick_load_pdf_script(self):
        from pdf2py import pdf
        datapath = '/home/danc/programming/python/data/'
        p = pdf.read(datapath+'test/e,rfhp1.0Hz,ra')
        #p = pdf.read(datapath+'0611/0611piez/e,rfhp1.0Hz')
        #p = pdf.read(datapath+'data/0611/drawing3/01%01%01@01:01/2/c,rfDC')
        p.data.setchannels('meg')
        #p.data.setchannellabels(['A1','A69','A130'])#meg')
        #p.data.setchannellabels(['A178'])
        p.data.getdata(0,p.data.pnts_in_file)
        self.numchannels = size(p.data.data_block,1)
        self.t = p.data.wintime #eventtime
        self.data = p.data.data_block
        self.tstart = 0; self.tstop = len(self.t)
        self.time = copy(self.t[self.tstart:self.tstop])
        self.chanind = arange(self.numchannels)
        self.chanlabels = p.data.channels.labellist
        self.scalefact = (p.data.data_block.min()+p.data.data_block.max())/2
        self.channels = p.data.channels.chanlocs
        self.srate = p.hdr.header_data.sample_period
        self.data_loaded_setup()
        self.curchannel = 0

    def hideinsteadofdelete(self,widget, ev=None):
        widget.hide()
        return True

    def load_data(self,widget):
        from gui.gtk import filechooser
        fn = filechooser.open()
        try: #pdf load method
            self.data_assist = meg_assistant.setup(path = fn[0], \
            callback=self.load_data_callback)

        except:
            print 'something wrong with load'
            return -1

    def load_data_callback(self, widget):
        print 'DONE!'
        p = self.data_assist.pdfdata #4D MEG file format
        input_dict = {'data_block':p.data.data_block,'srate':p.data.srate,'wintime':p.data.wintime,'labellist':p.data.channels.labellist,'chanlocs':p.data.channels.chanlocs}
        self.data_handler(widget, input_dict)


    def data_handler(self, widget, input_dict, callback=None):
        '''
        datahandler(data,srate,wintime,chanlabels,chanlocs)
        -
        data = 2D array
        srate = type(float or int)
        wintime = type(list or array) of same length as first dimension of data
        chanlabels = type(list of strings) of same length as
            second dimension of data
        chanlocs = shape is 2Xnumber of channels, ie, (2,248) and contains page
            coordinates for each channel. Position of X and Y is between -.5
            and .5
        '''
        ####!!!!!!!
        '''should rerwite the following as well as the filechooser method to make simple and compatible with dictionary based load and read'''
        data = input_dict['data_block']
        srate = input_dict['srate']
        wintime = input_dict['wintime']
        chanlabels = input_dict['labellist']
        chanlocs = input_dict['chanlocs']

        print type(data),srate,type(wintime),type(chanlabels),type(chanlocs)
        print len(chanlabels),size(data,1),len(wintime),size(data,0),\
        size(chanlocs,1)
        if len(chanlabels) != size(data,1) or len(wintime) != size(data,0):
        #or size(chanlocs,1) != size(data,1):
            print 'error matching wintime or chlabels or chanlocs with data'
            self.builder.get_object("messagedialog1").format_secondary_text\
            ('error matching wintime or chlabels or chanlocs with data')
            self.builder.get_object("messagedialog1").show()
            raise RuntimeError

        self.data = data
        self.srate = srate
        self.chanlabels = chanlabels
        self.t = array(wintime)
        self.tstart = 0; self.tstop = len(self.t)
        self.time = copy(self.t[self.tstart:self.tstop])
        self.numchannels = size(data,1)
        self.chanind = arange(self.numchannels)
        self.scalefact = (data.min()+data.max())/2
        print 'scalefact', self.scalefact
        self.channels = chanlocs
        self.curchannel = 0
        self.tstart = 0; self.tstop = len(self.t)

        self.data_loaded_setup()
        self.data2plot = self.data
        self.display_apply(None)


        try: callback(widget); self.callback = callback
        except TypeError, NameError: print('no callback')


    def offset_correct(self,widget):
        print self.get_time_selection(widget)
        if self.get_time_selection(widget) == -1: #no selections
            ###self.builder.get_object("messagedialog1").format_secondary_text\
            ###('No Selection Made Yet')
            ###self.builder.get_object("messagedialog1").show()
            print('no selections detected')
            return -1
        self.data = self.data - average(self.data[self.sel_ind,:],axis=0)
        print 'Data offset corrected, now trying to replot'
        self.display_apply(None)
        print widget,'wid:',widget.get_label()
        self.callback(widget)

    def add_selections_to_event_process(self,widget):
        try:
            if self.ed.window.get_property('visible') == False:
                #self.ed = event_process.setup_gui()
                self.ed.window.show()
        except AttributeError: #first call. setup
                self.ed = event_process.setup_gui()
                self.ed.window.show()
        if self.get_time_selection(widget) == -1:
            print('no selections detected')
            return -1

        print('passing selection indices',self.sel_onset_ind)
        self.ed.set_selected_events_passed(None,self.data,self.sel_onset_ind,self.t)
        self.ed.builder.get_object("button1").set_sensitive(False)

if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    print 'testing'
    ion()
    gtk.main()
