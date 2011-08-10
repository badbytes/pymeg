#       euclid.py
#
#       Copyright 2010 danc <danc@badbytes.net>
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

'''cos = array([0,0,.04])
euclid.dist(cos, random.randn(3,10))'''

from numpy import sqrt, size, shape, zeros, array

def dist(xyz1, xyz2):
    '''cos = array([0,0,.04])
    euclid.dist(cos, euclid.dist(cos, random.randn(3,10))'''

    if len(shape(xyz1)) == 1: #vector, reshape to 2d array
        xyz1 = array([xyz1])
    if len(shape(xyz2)) == 1: #vector, reshape to 2d array
        xyz2 = array([xyz2])

    s = zeros((size(xyz1,0),size(xyz2,0)))
    for i in range(0, size(xyz1,0)): #for each position
        for j in range(0, size(xyz2,0)): #for each xyz2 position
            s[i,j] = sqrt(((xyz1[i,0]-xyz2[j,0])**2)+((xyz1[i,1]-xyz2[j,1])**2)+((xyz1[i,2]-xyz2[j,2])**2));
    return s

def dist_old(X1, X2, Y1, Y2, Z1, Z2):
    #or could use ... sqrt(sum((x - y)**2))
    s = sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2));
    return s

def get_neighbors(target_channel_pos, other_channel_pos, neighbor_num):
    d = dist(target_channel_pos,other_channel_pos)
    distsort = d.argsort()
    r = distsort[:,0:neighbor_num]
    return r

def get_proximity(target_channel_pos, other_channel_pos, distance_in_mm):
    s = dist(target_channel_pos,other_channel_pos)
    #distind = argwhere(s < distance_in_mm)
    distind = where(s < distance_in_mm)
    out = array([[]],dtype=object)
    for i in s:
        print i,'ch'
        out = append(out,argwhere(i < 30))
        #out = append(argwhere(i < 30).T)

    fftout.pow[:,distind]


if __name__ == '__main__':
    dist()



#def distarray(xyz1, xyz2): #use with two arrays of three vals
    ##or could use ... sqrt(sum((x - y)**2))
    #if size(xyz1) != size(xyz2):
        #print 'arrays dont match in length'
        #return

    #if len(shape(xyz1)) == 2:
        #s = zeros((size(xyz1,0),size(xyz2,0)))
        #for i in range(0, size(xyz1,0)): #for each position
            #for j in range(0, size(xyz2,0)): #for each xyz2 position
                #s[i,j] = sqrt(((xyz1[i,0]-xyz2[j,0])**2)+((xyz1[i,1]-xyz2[j,1])**2)+((xyz1[i,2]-xyz2[j,2])**2));
    ##s = sqrt(((xyz1[0]-xyz2[0])**2)+((xyz1[1]-xyz2[1])**2)+((xyz1[2]-xyz2[2])**2));
        #return s
