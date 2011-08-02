#       simsource.py
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
sim=simsource.calc(ldf, xyz, qxqyqz);
'''
from numpy import *
from meg import closestposition

def calc(lf, xyz, qxqyqz):
    '''requires three arguments...
    leadfield-instance, xyz (3XN), qxqyqx (3XN)'''
    xyz = array(xyz)
    if len(xyz.shape) == 1: #1D to 2D vector
        print '1D to 2D reshape of xyz'
        xyz=array([xyz])
        #return xyz



    if len(qxqyqz.shape) == 1: #1D to 2D vector
        print '1D to 2D reshape of qxqyqz'
        qxqyqz=array([qxqyqz])
        #return qxqyqz


    sim = array([])
    for i in range(0, size(xyz,0)):
        #for j in range(0, size(qxqyqz,0)):
        minpos = closestposition.run(lf.grid, xyz[i,:]);
        qn = transpose(qxqyqz[i,:]);
        L = lf.leadfield[minpos,:,:];
        Li = linalg.pinv(L);print shape(Li),shape(qn)
        sim = append(sim,dot((L),dot(qn,10)));
    return sim.reshape(i+1,size(L,0))
    #return squeeze(sim.reshape(i+1, size(qxqyqz,0),size(L,0)))
