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
from numpy import *
import sys,nibabel,os,inspect,time
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
from matplotlib.patches import Circle

from pdf2py import readwrite


class setup_gui:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.splitext(__file__)[0]+".glade")
        self.window = self.builder.get_object("window1")

        dic = {
            "on_lpa_toggled" : self.set_lpa,
            "on_rpa_toggled" : self.set_rpa,
            "on_nas_toggled" : self.set_nas,
            "gtk_widget_hide" : self.hideinsteadofdelete,
            "on_menu_load_data_activate" : self.load_data,
            "on_menu_load_channels_activate" : self.load_channel_positions,
            "on_menuAbout_activate": self.show_aboutdialog,
            "on_menu_coregister_toggled" : self.coregister_toggle,
            "on_buttonsavecoreg_activate" : self.save_coregister_info,
            }

        self.builder.connect_signals(dic)
        self.create_draw_frame('none')

    def coregister_toggle(self,widget):
        if widget.get_active() == True:
            self.builder.get_object("hbuttonbox2").show()
        else:
            self.builder.get_object("hbuttonbox2").hide()

    def show_aboutdialog(self,widget):
        self.builder.get_object("aboutdialog1").show()

    def load_data(self,widget):
        pass
    def load_channel_positions(self,widget):
        pass

    def set_lpa(self,widget):
        if widget.get_active() == True:
            print 'adding circle', self.ind1, self.ind2, self.ind3
            circle = Circle((self.ind3,self.ind2),radius=5,color='b',alpha=.75)#self.ind2,self.ind3), 5)
            self.lpapatch = self.ax1.add_patch(circle)
            self.lpa = copy(self.coordinates)
        if widget.get_active() == False:
            self.lpapatch.remove()
        self.update()

    def set_rpa(self,widget):
        if widget.get_active() == True:
            print 'adding circle', self.ind1, self.ind2, self.ind3
            circle = Circle((self.ind3,self.ind2),radius=5,color='r',alpha=.75)#self.ind2,self.ind3), 5)
            self.rpapatch = self.ax1.add_patch(circle)
            self.rpa = copy(self.coordinates)
        if widget.get_active() == False:
            self.rpapatch.remove()
        self.update()

    def set_nas(self,widget):
        if widget.get_active() == True:
            print 'adding circle', self.ind1, self.ind2, self.ind3
            circle = Circle((self.ind3,self.ind2),radius=5,color='g',alpha=.75)#self.ind2,self.ind3), 5)
            self.naspatch = self.ax1.add_patch(circle)
            self.nas = copy(self.coordinates)
        if widget.get_active() == False:
            self.naspatch.remove()
        self.update()

    def save_coregister_info(self,widget):
        print 'current aux field in header',self.hdr['aux_file']
        filepath = os.path.splitext(self.img.file_map['header'].filename)[0]
        coreg_dict = {'lpa': self.lpa,'rpa': self.rpa, 'nas':self.nas}
        readwrite.writedata(coreg_dict, filepath)

    def load_coregister_info(self, widget):
        if os.path.isfile(filepath+'.pym') == True:
            print('loading index points found in file',filepath+'.pym')
            self.fiddata = readwrite.readdata(filepath+'.pym')
            self.getfiducals(h)


    #def test2(self,widget):

        #self.fig.clf()
        #self.display(self.data,self.chanlocs,animate='on')
    #def test3(self,widget):

        #self.fig.clf()
        #self.display(self.data,self.chanlocs,data2=self.data[0],quiver='on')

    def hideinsteadofdelete(self,widget,ev=None):
        print 'hiding',widget
        widget.hide()
        return True

    def create_draw_frame(self,widget):
        self.fig = Figure(figsize=[500,500], dpi=40)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.show()
        self.figure = self.canvas.figure
        self.axes = self.fig.add_axes([0.045, 0.05, 0.93, 0.925], axisbg='#FFFFCC')
        self.axes.axis('off')
        self.vb = self.builder.get_object("vbox1")
        self.vb.pack_start(self.canvas, gtk.TRUE, gtk.TRUE)
        self.vb.show()

    #def plot_data(self,data):
        #"""provide...
            #xi=grid x data
            #yi=grided y data
            #zi=interpolated MEG data for contour
            #intx and inty= sensor coords for channel plotting"""

        #self.sp.imshow(data[100])#,shading='interp',cmap=cm.jet)

    def IndexTracker(self, data, ax1, ax2, ax3, colormap, pixdim, overlay, translation):#, coord):

        try: colormap = self.color_sel
        except: pass
        self.overlay = overlay
        self.ax1 = ax1
        ax1.set_title('Axial')
        self.ax2 = ax2
        ax2.set_title('Coronal')
        self.ax3 = ax3
        ax3.set_title('Sagital')
        #coord.set_title('\n\n\n\ncoord')

        self.data = (data)
        self.slices1,self.slices2,self.slices3 = data.shape

        print self.slices3,self.slices2,self.slices1, translation, data.shape
        self.translation = translation
        #coord1 = (-1000,100,-100,1000)
        #coord1 = (translation[1]+self.slices2,translation[1],translation[0]+self.slices3,translation[0])
        #coord2 = (translation[0]+self.slices3,translation[0],translation[2]-self.slices1,self.slices1-translation[2])
        #coord3 = (translation[1]+self.slices2,translation[1],translation[2]-self.slices1,self.slices1-translation[2])

        self.ind1 = self.slices3/2
        self.ind2 = self.slices2/2
        self.ind3 = self.slices1/2


        self.im1 = ax1.imshow(self.data[:,:,self.ind1].T, aspect = 'auto',cmap=colormap); ax1.set_ylim(ax1.get_ylim()[::-1]);
        self.im2 = ax2.imshow(self.data[:,self.ind2,:].T, aspect = 'auto',cmap=colormap); ax2.set_ylim(ax2.get_ylim()[::-1]);
        self.im3 = ax3.imshow(self.data[self.ind3,:,:].T, aspect = 'auto',cmap=colormap); ax3.set_ylim(ax3.get_ylim()[::-1]);

        #self.coord = coord

        for im in gca().get_images():
            im.set_clim(self.data.min(), self.data.max())

        self.update1()
        self.pixdim = pixdim
        print pixdim

    def onscroll(self, event):
        if event.inaxes == self.ax1:
            if event.button=='up':
                self.ind1 = clip(self.ind1+1, 0, self.slices1-1)
            else:
                self.ind1 = clip(self.ind1-1, 0, self.slices1-1)
            self.update()

        if event.inaxes == self.ax2:
            if event.button=='up':
                self.ind2 = clip(self.ind2+1, 0, self.slices2-1)
            else:
                self.ind2 = clip(self.ind2-1, 0, self.slices2-1)
            self.update()

        if event.inaxes == self.ax3:
            if event.button=='up':
                self.ind3 = clip(self.ind3+1, 0, self.slices3-1)
            else:
                self.ind3 = clip(self.ind3-1, 0, self.slices3-1)
            self.update()

    def update(self):
        self.update1();self.update2();self.update3()

    def update1(self):
        self.im1.set_data(self.data[:,:,self.ind1].T)
        self.im1.axes.figure.canvas.draw()

    def update2(self):
        self.im2.set_data(self.data[:,self.ind2,:].T)
        self.im2.axes.figure.canvas.draw()

    def update3(self):
        self.im3.set_data(self.data[self.ind3,:,:].T)
        self.im3.axes.figure.canvas.draw()

    def click(self,event, pixdim=None):
        self.events=event
        if event.button == 3:
            self.showpopupmenu(None,event)
            return

        #print self.pixdim
        def printcoord():
            #coordinates = round(self.ind3*self.pixdim[0]+(self.translation[0])), round(self.ind2*self.pixdim[1]+(self.translation[1])), round(self.ind1*self.pixdim[2]+(self.translation[2]))
            coordinates = self.coordinates = array([round(self.ind2*self.pixdim[1]+(self.translation[1])), round(self.ind3*self.pixdim[0]+(self.translation[0])), round(self.ind1*self.pixdim[2]+(self.translation[2]))])
            coordinates = self.coordinates = array([round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2])])
            print coordinates, 'mm'#, self.ind3, self.pixdim,(self.translation[0])
            return coordinates

        if event.inaxes == self.ax1:
            self.ind2=int(event.ydata)
            self.ind3=int(event.xdata)
            #print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            printcoord()
            self.update()
        if event.inaxes == self.ax2:
            self.ind1=int(event.ydata)
            self.ind3=int(event.xdata)
            #print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            printcoord()
            self.update()
        if event.inaxes == self.ax3:
            self.ind1=int(event.ydata)
            self.ind2=int(event.xdata)
            #print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            printcoord()
            self.update()
        #print self.ind1,self.ind2,self.ind3
        #self.coord.title.set_text([round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2])])
        return self.ind3*self.pixdim[0], self.ind2*self.pixdim[1], self.ind1*self.pixdim[2]#event

    def showpopupmenu(self,widget,event):
        print('button ',event.button)
        if event.button == 3:
            m = self.builder.get_object("menufunctions")
            print(widget, event)
            m.show_all()
            m.popup(None,None,None,3,0)

    def display(self,data=None, overlay=None, colormap=cm.gray, pixdim=None, translation=None):
        self.get_color_maps()
        try:
            if os.path.splitext(data.__module__)[0] == 'nibabel':
                self.hdr = img.get_header()
                pixdim = self.hdr['pixdim'][0:3]
                transform = img._affine[0:3,0:3];print 'orig trans',transform
                translation = img._affine[0:3,3]; print 'translation', translation
                data = squeeze(img.get_data())
                self.img = img
        except:
            pass

        if translation == None:
            translation == [0,0,0]
        print '------------',translation

        if pixdim == None:
            pixdim = [1.0,1.0,1.0]; #unitless
        ax1 = self.fig.add_subplot(221);#axis('off')
        #colorbar(fig,ax=ax1)
        xlabel('Anterior (A->P 1st Dim)');ylabel('Right (R->L 2nd Dim)')
        ax2 = self.fig.add_subplot(222);#axis('off')
        xlabel('Inferior (I->S Dim)');ylabel('Anterior (A->P 1st Dim)')
        ax3 = self.fig.add_subplot(223);#axis('off')
        xlabel('Infererior (I->S 3rd dim)');ylabel('Right (R->L 2nd Dim)')
        #coord = self.fig.add_subplot(224);axis('off')
        tracker = self.IndexTracker(data, ax1, ax2, ax3, colormap, pixdim, overlay, translation)#, coord)
        self.fig.canvas.mpl_connect('scroll_event', self.onscroll)
        self.fig.canvas.mpl_connect('button_press_event', self.click)
        #ax1.imshow(data[100])
        print 'plot done'

        return tracker

    def get_color_maps(self):
        self.color_list = []
        m = inspect.getmembers(cm)
        for i in m:
            try:
                if i[1].__module__ == 'matplotlib.colors':
                    self.color_list.append(i[0])
            except:
                pass
        self.populate_combo(colorlabels=self.color_list)



    def populate_combo(self, colorlabels=None):
        print 'populating channel list'
        #if colorlabels == None:
            #colorlabels = arange(50)
        combobox = self.builder.get_object("combobox1")
        combobox.clear()
        liststore = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_wrap_width(int(ceil(sqrt(len(colorlabels)))))

        for n in colorlabels: #range(50):
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
            #self.chan_ind = index
            self.color_sel = str(model[index][0])
        #self.im1.axes.clear()
        self.im1.set_cmap(self.color_sel)
        self.im1.axes.figure.canvas.draw()
        self.im2.set_cmap(self.color_sel)
        self.im2.axes.figure.canvas.draw()
        self.im3.set_cmap(self.color_sel)
        self.im3.axes.figure.canvas.draw()
        return

if __name__ == "__main__":
    mainwindow = setup_gui()
    mainwindow.window.show()
    from pdf2py import pdf
    from mri import img_nibabel
    fn = '/home/danc/python/data/standardmri/colin_1mm.img'
    #fn = '/home/danc/python/data/standardmri/ch3.nii.gz'
    img = nibabel.load(fn)
    h = img.get_header()

    pixdim = h['pixdim'][0:3]
    transform = img._affine[0:3,0:3];#print 'orig trans',transform
    translation = img._affine[0:3,3]
    #a = array([[0,1,0],[1,0,0],[0,0,1]]);print 'new trans',a
    a = dot(eye(3),img._affine[0:3,0:3])- img._affine[0:3,0:3]
    print 'new transform',a

    #d = squeeze(img.get_data())
    r = nibabel.apply_orientation(squeeze(img.get_data()),a)#transform)#a[0:3,0:3])

    t = mainwindow.display(img)#, pixdim=pixdim,translation=translation)
    mainwindow.get_color_maps()


    #ion()
    #gtk.set_interactive(1)
    gtk.main()
