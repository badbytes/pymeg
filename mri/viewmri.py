# Copyright 2008 Dan Collins

# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


'''This is a simple mri viewer the mri is read using the img module with the read function
   from mri import img
   nim=img.read()'
   data=nim.data()'
   t=viewmri.plotit(numpy.flipud(nim.data))'''

import numpy
from numpy import shape, flipud, swapaxes, sum, array
from pylab import imshow, cm, figure, subplots_adjust, xlabel, ylabel, axis, gca, connect, show, ion, ioff
#from com import socket_talk

class IndexTracker:
    def __init__(self, data, ax1, ax2, ax3, colormap, pixdim, overlay, coord):
        self.overlay = overlay
        self.ax1 = ax1
        ax1.set_title('Axial')
        self.ax2 = ax2
        ax2.set_title('Sagital')
        self.ax3 = ax3
        ax3.set_title('Coronal')
        coord.set_title('\n\n\n\ncoord')

        self.data = (data)
        rows,cols,self.slices1 = data.shape
        rows,self.slices2,cols = data.shape
        self.slices3,rows,cols = data.shape

        self.ind1 = self.slices1/2
        self.ind2 = self.slices2/2
        self.ind3 = self.slices3/2
        print data.shape

        self.im1 = ax1.imshow(self.data[:,:,self.ind1], aspect = 'auto',cmap=colormap); ax1.set_ylim(ax1.get_ylim()[::-1]);
        self.im2 = ax2.imshow(self.data[:,self.ind2,:].T, aspect = 'auto',cmap=colormap); ax2.set_ylim(ax2.get_ylim()[::-1]);
        self.im3 = ax3.imshow(self.data[self.ind3,:,:].T, aspect = 'auto',cmap=colormap); ax3.set_ylim(ax3.get_ylim()[::-1]);


        self.coord = coord

        for im in gca().get_images():
            im.set_clim(self.data.min(), self.data.max())

        self.update1()
        self.pixdim = pixdim
        print pixdim

        #self.socket = socket_talk.setup()


    def onscroll(self, event):
        if event.inaxes == self.ax1:
            if event.button=='up':
                self.ind1 = numpy.clip(self.ind1+1, 0, self.slices1-1)
            else:
                self.ind1 = numpy.clip(self.ind1-1, 0, self.slices1-1)

            self.update()

        if event.inaxes == self.ax2:
            if event.button=='up':
                self.ind2 = numpy.clip(self.ind2+1, 0, self.slices2-1)
            else:
                self.ind2 = numpy.clip(self.ind2-1, 0, self.slices2-1)

            self.update()

        if event.inaxes == self.ax3:
            if event.button=='up':
                self.ind3 = numpy.clip(self.ind3+1, 0, self.slices3-1)
            else:
                self.ind3 = numpy.clip(self.ind3-1, 0, self.slices3-1)

            self.update()

    def update(self):
        self.update1();self.update2();self.update3()

    def update1(self):
        self.im1.set_data(self.data[:,:,self.ind1])
        self.im1.axes.figure.canvas.draw()

    def update2(self):
        self.im2.set_data(self.data[:,self.ind2,:].T)
        self.im2.axes.figure.canvas.draw()

    def update3(self):
        self.im3.set_data(self.data[self.ind3,:,:].T)
        self.im3.axes.figure.canvas.draw()

    def click(self,event, pixdim=None):
        self.events=event
        #print self.pixdim


        if event.inaxes == self.ax1:
            self.ind2=int(event.xdata)
            self.ind3=int(event.ydata)
            print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            self.update()
        if event.inaxes == self.ax2:
            self.ind1=int(event.ydata)
            self.ind3=int(event.xdata)
            print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            self.update()
        if event.inaxes == self.ax3:
            self.ind1=int(event.ydata)
            self.ind2=int(event.xdata)
            print round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2]), 'mm'
            self.update()

        #coords = array([self.ind3*self.pixdim[0], self.ind2*self.pixdim[1], self.ind1*self.pixdim[2]])
        #self.socket.client(coords)
        self.coord.title.set_text([round(self.ind3*self.pixdim[0]), round(self.ind2*self.pixdim[1]), round(self.ind1*self.pixdim[2])])
        return self.ind3*self.pixdim[0], self.ind2*self.pixdim[1], self.ind1*self.pixdim[2]


def display(data=None, orient='LPS', overlay=None, colormap=cm.gray, pixdim=None):
    "mri=img.decimate(nim, 5)"
    "ex. slice.plot(mri)"

    import sys
    print sys.argv
    if data == None:
        try:
            fn=sys.argv[1]
            from mri import img
            data = img.read(fn)
        except AttributeError:
            print 'not passing data arg'
            print('lets plot random data')
            from numpy import random
            data = random.randn(10,10,10)

    try:
        data.qform
        print 'think its a nifti volume'
        nim = data
        mrdata = nim.data
        print shape(mrdata)
        pixdim = nim.voxdim[::-1]

    except AttributeError:
        if pixdim != None:
            print 'using user supplied pixeldimensions', pixdim
        else:
            print 'probably not a nifti volume. using voxel units instead of actual distance units'
            pixdim = [1.0,1.0,1.0]; #unitless
        mrdata = data

    fig = figure()
    subplots_adjust(left=.15, bottom=.15,right=1, top=.95,wspace=.25, hspace=.35)

    ax1 = fig.add_subplot(221);#axis('off')
    #colorbar(fig,ax=ax1)
    xlabel('Anterior (A->P 1st Dim)');ylabel('Right (R->L 2nd Dim)')
    ax2 = fig.add_subplot(222);#axis('off')
    xlabel('Inferior (I->S Dim)');ylabel('Anterior (A->P 1st Dim)')
    ax3 = fig.add_subplot(223);#axis('off')
    xlabel('Infererior (I->S 3rd dim)');ylabel('Right (R->L 2nd Dim)')
    coord = fig.add_subplot(224);axis('off')
    tracker = IndexTracker(mrdata, ax1, ax2, ax3, colormap, pixdim, overlay, coord)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    cid = connect('button_press_event', tracker.click)

    show()


    return tracker

if __name__=='__main__':
    from numpy import random
    data = random.randn(10,10,10)
    display(data)
