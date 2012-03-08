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

# A portion of this code was used and adapted from meg_leadfield1.m function distributed with
# the matlab fieldtrip package at fcdonders, which was adapted from Luetkenhoener, Habilschrift '92.


"""Compute leadfields
pos=R point
pos= channel location vector
ori=signal channel orientation

ex. x=leadfield.calc(channelinstance, grid) ....
    will return the leadfield sum from both upper and lower coils

    grid is N X 3 array. Make sure to reshape it if Ndim=1 to by 1X3
    ex. IF....shape(grid) RETURNS (3,) THEN grid=grid.reshape(1,3)
    or just make grid like... grid=array([[0, 6, 3]])"""


from numpy import * #zeros, array, dot, cross, shape, append, reshape, size
from numpy.linalg import norm
from pdf2py import pdf
from time import time,sleep
import sys, logging
from misc import progressbar as pb
from multiprocessing import Pool,Process,cpu_count

class shared_data:
    def __init__(self,grid=None):
        self.grid = grid

class calc:
    def __init__(self,channelinstance=None,grid=None,centerofsphere=None,chlowerpos=None,chupperpos=None,chlowerdir=None,chupperdir=None):
        '''calc leadfield script to use pos.py and getlf class to get the sum of upper and lower coils
        returns leadfield
        grid=voxel location. dimensions: N X 3'''
        self.ext = 'pymlf'
        global chlpos,chldir,cos,chupos,chudir
        if channelinstance == None:
            if chlpos == None or chupos == None or chldir == None or chudir == None:
                print('if channelobject not supplied, you need to supply ch position and direction for upper and lower coil')
                raise Exception('InputError')
        else:
            chlpos=channelinstance.chlpos;
            chldir=channelinstance.chldir;
            chupos=channelinstance.chupos;
            chudir=channelinstance.chudir;


        #check grid and guess if units are correct
        if grid.max() < 15 and grid.min() > -15:
            print ''
            print 'Warning...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print 'Warning...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print 'Warning...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
            print 'Your grid point values are small. Max ==', grid.max(), 'Are you sure they are in mm\n'

        ts = time()
        coilsperch=2; #gradiometer config
        channelinstance.getposition()

        if centerofsphere == None:
            self.spherecenter = array([0,0,40])#c=cos.center()
        else:
            self.spherecenter = centerofsphere

        if array(self.spherecenter).max() < 10:
            print 'COS Warning!!! Your center of sphere is quite close to 0,0,0. Make sure your units are in mm'
        cos = self.spherecenter

        gridshape=shape(grid)
        if len(shape(grid)) == 1:
            grid = grid.reshape([1,3])

        print 'make sure your grid units are in mm'
        if size(grid,1) != 3: #check grid dimensions
            if size(grid,0) != 3:
                print 'grid dimensions wrong'
                return
            grid = grid.transpose()
            print 'reshaping grid'

        global y; y = float(len(grid))/float(cpu_count())
        global pbar; pbar = pb.ProgressBar().start()
        #Parallel Compute Leadfields
        logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)
        pool = Pool(processes=cpu_count())
        self.p = pool.map(code, grid)
        te = time()
        print 'Done. Elapsed time', te-ts, 'seconds'
        self.leadfield = squeeze(array(self.p))
        del(self.p)
        self.grid = grid
        return

import threading
import os
def code(grid):#=None, pos=None, ori=None, cent=None):

    #print("Task(%s) processid = %s" % ('layer', os.getpid()))
    try: x;
    except NameError: global x; x = 0
    x = x +1
    #print y
    """grid=voxel location. dimensions: N X 3
    pos=position of channels. returned by pos.py
    ori=orientation of channels. returned by pos.py"""

    #danc changed hdr read to convert to mm upfront.
    #pos=pos*1000 #convert channel pos from meters to mm

    #pbar = pb.ProgressBar().start()
    #sys.stdout.flush()
    if (float(x)/float(y))*100 < 100:
        pbar.update((float(x)/float(y))*100)
    #for i in [10,20,30,40,50,60,70,80,90,100]:
        #if (float(x)/float(y))*100 > 10:
            #pass
    #print (float(x)/float(y))*100, '%complete'

    R = grid - cos
    nchans = len(chupos)
    ncoils = 2
    nrank = 3
    lf=zeros((ncoils,nchans,nrank))
    #pbar = progressbar.ProgressBar().start()
    for h in [[chupos,chudir,0],[chlpos,chldir,1]]:
        #for j in range(0,len(loc)): #for each grid point
        "for each chp calculate the leadfield"


        chp = h[0] - cos
        position = chp
        orientation = h[1]
        lftmp = zeros((nchans,3),float);
        tmp2 = norm(R);

        for i in range(0,nchans):
            t = position[i]
            o = orientation[i]
            tmp1 = norm(t);
            tmp3 = norm(t-R);
            tmp4 = dot(t,R);
            tmp5 = dot(t,t-R);
            tmp6 = dot(R,t-R);
            tmp7 = (tmp1*tmp2)**2 - tmp4**2; #% cross(r,R)**2
            alpha = 1 / (-tmp3 * (tmp1*tmp3+tmp5));
            A = 1/tmp3 - 2*alpha*tmp2**2 - 1/tmp1;
            B = 2*alpha*tmp4;
            C = -tmp6/(tmp3**3);
            beta = dot(A*t + B*R + C*(t-R), o)/tmp7;
            lftmp[i,:] = cross(alpha*o  + beta*t, R);

        #lf = append(lf, 1e-7*lftmp); #% multiply with u0/4pi
        lf[h[2]] = 1e-7*lftmp; #For each coil, multiply with u0/4pi
    if ncoils > 1 and ncoils <= 2:
        lf = lf[1] + lf[0] #Average LeadField between the two coils
    return lf


if __name__ == '__main__':
    from numpy import *
    from gui.gtk import progressbar
    MT = progressbar.MainThread()

    def leadfieldthread():
        fn = '/home/danc/python/data/0611/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
        from pdf2py import pdf
        p = pdf.read(fn)
        p.data.setchannels('meg')
        grid=random.randn(3,10)
        lft = calc(p.data.channels,grid)
        print type(lft.leadfield), shape(lft.leadfield)



    MT.main(leadfieldthread)#,progresstype='fraction')
