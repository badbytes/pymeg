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



import pylab as p
try:
    import numpy.core.ma as ma
except ImportError:
    import numpy.ma as ma
    
from scipy.io import write_array
from scipy.io import read_array
from numpy import shape, mgrid, interp, isnan
import time

import sys
try:
    sys.path.index('/usr/lib/python2.6')
except ValueError:
    from scikits.delaunay import *
    delaunay = 'yes'
else: #using python 2.6
    from matplotlib.mlab import griddata
    delaunay = 'no'

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

    #p.pcolor(xi,yi,zim,shading='interp',cmap=p.cm.jet)
    p.contourf(xi,yi,zim,cmap=p.cm.jet)
    #p.scatter(intx,inty, alpha=.5,s=.5)
    #p.draw()
    #p.show()
    #return p

def plot_data_loop(xi,yi,zi,intx,inty):
    pass
    
def display(data, chanlocs):

    xi, yi = mgrid[-.5:.5:67j,-.5:.5:67j]
    intx=chanlocs[1,:]
    inty=chanlocs[0,:]
    z = data
    
    
##    tri = Triangulation(intx,inty)
##    interp = tri.nn_interpolator(z)
##    zi = interp(xi,yi)
    
    if delaunay == 'yes':
        tri = Triangulation(intx,inty)
        interp = tri.nn_interpolator(z)
        zi = interp(xi,yi)
    else: #try griddata method
        zi = griddata(intx,inty,z,xi,yi)
        
    zim = ma.masked_where(isnan(zi),zi)
    plot_data(xi,yi,zi,intx,inty)

if __name__ == '__main__':
    main()
