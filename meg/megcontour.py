# Copyright 2008 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#090327 changed zi interp method from delaunay to griddata for compatibility with python 2.6
#
#
'''from meg import megcontour
p = pdf.read(fn[0])
p.data.setchannels('meg')
p.data.getdata(0,10)
p.data.channels.getposition()
megcontour.display(p.data.data_block[0,:], ch.chanlocs, labels=p.data.channels.channelsortedlabels)
'''

import pylab as p
import sys
#try:
    #sys.path.index('/usr/lib/python2.6')
#except ValueError:
    #from scikits.delaunay import *
    #delaunay = 'yes'
#else: #using python 2.6
    #from matplotlib.mlab import griddata
    #delaunay = 'no'

try: from scikits.delaunay import * ; delaunay = 'yes'
except ImportError: from matplotlib.mlab import griddata; delaunay = 'no'

#~ from scikits.delaunay import *
#~ delaunay = 'yes'

try:
    import numpy.core.ma as ma
except ImportError:
    import numpy.ma as ma


#from scipy.io import write_array
#from scipy.io import read_array
from numpy import shape, mgrid, interp, isnan, ceil, sqrt,arange , size
import time


'''how to use:
        eg. megcontour.display(data)
        ch=channel.index(pdf, 'meg')
        d=data.read(pdf, 0, 200, ch.sortedindtype)
        megcontour.display(d.data_block[100,:], ch.chanlocs)'''


def plot_data(xi,yi,zi,intx,inty):
    """provide...
        xi=grid x data
        yi=grided y data
        zi=interpolated MEG data for contour
        intx and inty= sensor coords for channel plotting"""

    tstart = time.time()

    zim = ma.masked_where(isnan(zi),zi)

    p.pcolor(xi,yi,zim,shading='interp',cmap=p.cm.jet)

    p.contourf(xi,yi,zim,cmap=p.cm.jet)
    p.scatter(intx,inty, alpha=.75,s=3)

    p.show()
    return p

def plot_data_loop(xi,yi,zi,intx,inty):
    pass

def printlabels(chanlocs, labels):
        #if labels != None:
    count = 0
    for l in labels:
        p.text(chanlocs[1,count], chanlocs[0,count], l, alpha=1, fontsize=9)
        count = count + 1

def titles(titletxt):
    print

def display(data, chanlocs, data2=None, subplot='off', animate='off', quiver='off', title=None, labels=None, colorbar='off'):

    if len(shape(chanlocs)) != 2:
        print 'Chanlocs shape error. Should be 2D array "(2,N)"'
        print 'transposing'
        chanlocs = chanlocs.T

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

        #p.ion()
        fig = p.figure()

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
                #del(z,interp,zi,zim)
        if subplot == 'on':
            print 'suplotting'
            for i in range(0, shape(data)[0]):
                spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
                fig.add_subplot(spnum,spnum,i+1);#axis('off')
                dataslice=data[i,:];
                p.scatter(intx,inty, alpha=.75,s=3)
                z = dataslice
                if delaunay == 'yes':
                    interp = tri.nn_interpolator(z)
                    zi = interp(xi,yi)
                else:
                    zi = griddata(intx,inty,z,xi,yi)

                zim = ma.masked_where(isnan(zi),zi)
                p.contourf(xi,yi,zim,cmap=p.cm.jet, alpha=.8)
                p.axis('off')
                if labels != None:
                    printlabels(chanlocs, labels)
                if title != None:
                    p.title(str(title[i]))
                else:
                    p.title(str(i))
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

        p.ioff()
        #p.colorbar()
        p.show()
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
        plot_data(xi,yi,zi,intx,inty)
        if labels != None:
            printlabels(chanlocs, labels)

        if colorbar == 'on':
            p.colorbar(cmap=p.cm.jet)



if __name__ == '__main__':
    main()
