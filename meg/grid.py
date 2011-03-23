#       grid.py
#      
#       Copyright 2009 danc <quaninux@gmail.com>
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
import numpy as np
from meg import euclid

def cube(location, gridsize, spacing):
    '''make 3d grid with given location of center, gridsize, and spacing
    g = grid.doit(array([1,1,1]),2,1)
    makes a grid (g) centered around location 1,1,1 of size 3, with a spacing of 1'''
    gridtmp = np.ones([gridsize,gridsize,gridsize])
    grid = spacing * np.squeeze(np.array([np.where(gridtmp)]))
    z = np.tile(location,[np.size(grid,1),1])
    gridind = (grid + z.T)
     
    newgrid = gridind - np.array([np.mean(gridind,axis=1)]).T + gridind
    gridfinal = newgrid.T - (gridind.T-location)
    return gridfinal.T#,gridind#, gridtmp,np.array([np.mean(gridtmp,axis=1)]).T,test#,z

def sphere(location, gridsize, spacing):#, radius):
    '''make 3d sphere grid with given location of center, gridsize, spacing, and radius
    g = grid.sphere(array([1,1,1]),12,.5)
    makes a grid (g) centered around location 1,1,1 of size 12, with a spacing of 1'''
    radius = (gridsize*spacing)/2.
    cgrid = cube(location, gridsize, spacing)
    print cgrid.shape, location
    e = np.zeros(np.size(cgrid,1))
    g = np.copy(e)
    for i in range(0,np.size(cgrid,1)):
        #e[:,i] = euclid.dist(location[0],cgrid[0][i],location[1],cgrid[1][i],location[2],cgrid[2][i])
        e[i] = euclid.dist(location,cgrid[:,i])
    #e = e*10
    print 'diameter', e.max(), 'mm'
    sgrid = cgrid[:,e < radius].reshape([3,np.size(cgrid[:,e < radius])/3])
    #cgrid[e > radius].reshape([3,np.size(cgrid[e > radius])/3]) == 0
    
    return sgrid#,cgrid
    
