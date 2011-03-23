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
    

#from scipy.io import write_array
#from scipy.io import read_array
from numpy import shape, mgrid, isnan, ceil, sqrt,\
size, imag, real, array, #interp, arange
#import time
import sys
try:
    sys.path.index('/usr/lib/python2.6')
except ValueError:
    from scikits.delaunay import *
    delaunay = 'yes'
else: #using python 2.6
    from matplotlib.mlab import griddata
    delaunay = 'no'
    


    
def display(data, chanlocs, labels='None', contourdata=None):

    xi, yi = mgrid[-.5:.5:67j,-.5:.5:67j]
    intx=chanlocs[1,:]
    inty=chanlocs[0,:]
    print '2d array of data'
    
    #tri = Triangulation(intx,inty)

    
    
    p.ion()
    fig = p.figure()
        
    print 'suplotting quiver'
    if len(data.shape) == 1:
        data = array([data])
    for i in range(0, size(data,0)):
        spnum = ceil(sqrt(shape(data)[0])) #get x and y dimension of subplots
        fig.add_subplot(spnum,spnum,i+1);#axis('off')
        
        if contourdata != None:

            dataslice=contourdata[i,:];
            z = dataslice
            
            if delaunay == 'yes':
                print 'delaunay is set'
                tri = Triangulation(intx,inty)
                interp = tri.nn_interpolator(z)
                zi = interp(xi,yi)
            else: #try griddata method
                print 'delaunay is off'
                zi = griddata(intx,inty,z,xi,yi)
                    
            
            interp = tri.nn_interpolator(z)
            zi = interp(xi,yi)
            zim = ma.masked_where(isnan(zi),zi)
            p.contourf(xi,yi,zim,cmap=p.cm.jet, alpha=.8)
            p.axis('off')
        
        
        dataslice=data[i,:];
        z = dataslice
        sc=data.max()*10
        #return intx, inty, z#imag(z), real(z)
        #print i
        p.quiver(intx,inty, imag(z), real(z))#, scale=sc)
        if labels != 'None':
            p.title(str(labels[i]))
        p.axis('off')
        



    #p.ioff()
    #p.show()


if __name__ == '__main__':
    main()
