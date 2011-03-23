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

#090327 changed zi interp method from delaunay to griddata for compatibility with python 2.6


from pylab import plot, show, contour, pcolor, figure, cm, colorbar, contourf,scatter, draw, ion, ioff
#from scikits.delaunay import *
import numpy.core.ma as ma
from scipy.io import write_array
from scipy.io import read_array
from numpy import shape, mgrid, interp, isnan

import sys
try:
    sys.path.index('/usr/lib/python2.6')
except ValueError:
    from scikits.delaunay import *
    delaunay = 'yes'
else: #using python 2.6
    from matplotlib.mlab import griddata
    delaunay = 'no'

"""how to use: 
        eg. megcontour.display(data)"""


def plot_data(xi,yi,zi,intx,inty):
    """provide...
        xi=grid x data
        yi=grided y data
        zi=interpolated MEG data for contour
        intx and inty= sensor coords for channel plotting"""
    zim = ma.masked_where(isnan(zi),zi)
    #pcolor(xi,yi,zim,shading='interp',cmap=cm.jet)
    contourf(xi,yi,zim,cmap=cm.jet)
    #scatter(intx,inty, alpha=.5,s=.5)
    #contour(xi,yi,zim,cmap=cm.jet)
    draw()
    #show()
    


def display(data, chanlocs):
    xi, yi = mgrid[-.5:.5:67j,-.5:.5:67j]
    #chanlocs=read_array("/home/danc/programming/python/configs/megchannels.cfg")
    #return chanlocs
    ##intx=chan['intx']
    ##inty=chan['inty']
    intx=chanlocs[1,:]
    inty=chanlocs[0,:]
    #z = slices[:,100]
    z = data
    
    if delaunay == 'yes':
        tri = Triangulation(intx,inty)
        interp = tri.nn_interpolator(z)
        zi = interp(xi,yi)
    else: #try griddata method
        zi = griddata(intx,inty,z,xi,yi)
    
    
    #tri = Triangulation(intx,inty)
    #interp = tri.nn_interpolator(z)
    #zi = interp(xi,yi)
    plot_data(xi,yi,zi,intx,inty)


if __name__ == '__main__':
    main()
