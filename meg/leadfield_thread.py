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

ex. x=leadfield.calclf(channelinstance, grid) ....
    will return the leadfield sum from both upper and lower coils

    grid is N X 3 array. Make sure to reshape it if Ndim=1 to by 1X3
    ex. IF....shape(grid) RETURNS (3,) THEN grid=grid.reshape(1,3)
    or just make grid like... grid=array([[0, 6, 3]])"""


from numpy import zeros, array, dot, cross, shape, append, reshape, size
from numpy.linalg import norm
from pdf2py import pdf
from time import time,sleep
import sys
from misc import progressbar

import logging
import threading

class calc:
    #def __init__(self,datapdf,channelinstance,grid, centerofsphere=None):
    def __init__(self,channelinstance=None,grid=None,centerofsphere=None,chlpos=None,chupos=None,chldir=None,chudir=None):
        '''calc leadfield script to use pos.py and getlf class to get the sum of upper and lower coils
        returns leadfield
        grid=voxel location. dimensions: N X 3'''
        self.ext = 'pymlf'

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
            #self.spherecenter = c.spherecenter
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
        print shape(grid)
        #print 'Calculating Lower Coil LeadFields for', size(grid,0), 'grid points\n'
        #lowerlf = code(grid, chlpos ,chldir, cent = self.spherecenter)
        sys.stdout.flush()
        finished = []
        #from Queue import Queue
        #queue = Queue()
        #logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

        ts = time()
        from multiprocessing import Process
        for i in range(2):
            t = threaded(args=(1))
            t.start()
            #p = Process(target=parrallel, args=(i,))
            #p.start();p.join()
        te = time()
        print 'elapsed time', te-ts, 'seconds'
        return

        #for i in range(size(grid,0)):
            #t = code(args=(i,chlpos,chldir,cos))#,queue)#, kwargs={'a':'A', 'b':'B'})

            #t.setDaemon(True)
            #t.start();
        #for i in range(size(grid,0)):
            #r = code(args=(i,chupos,chudir,cos))
            #r.start();
        #self.q = queue
        #sleep(1)
        #queue.join()
        #queue.all_tasks_done
        #print 'QS',queue.qsize()
        #self.lowerlf = array(queue.queue)
        #while queue.qsize() < size(grid,0):
            #sleep(1)
        #sleep(1)
        #print '[[[[[[',shape(self.lowerlf),queue.qsize(),queue.unfinished_tasks


        #self.lowerlf = zeros((size(grid,0),size(grid,1),size(chlpos,0)));#print lowerlf.shape
        #self.upperlf = zeros((size(grid,0),size(grid,1),size(chlpos,0)));#print lowerlf.shape
        #for j in range(size(grid,0)):
            #self.upperlf[j] = queue.get().reshape((size(grid,1),size(chlpos,0)));#print j
            #self.lowerlf[j] = queue.get().reshape((size(grid,1),size(chlpos,0)));#print j

        #te = time()
        #print ' ' #sys.stdout.flush()
        #print 'elapsed time', te-ts, 'seconds'
        #return

        #lowerlf = queue.get()

        #for i in range(size(grid,0)):
            #t = code(args=(i, chupos ,chudir, self.spherecenter,queue))#, kwargs={'a':'A', 'b':'B'})
            #t.setDaemon(True)
            #t.start()
        #queue.join()
        #upperlf = queue.get()

        #print 'Calculating Upper Coil LeadFields for', size(grid,0), 'grid points\n'
        #upperlf = code(grid, chupos ,chudir, cent = self.spherecenter)

        sizegrid=len(grid)
        leadfieldfinal=(lowerlf+upperlf)

        print shape(leadfieldfinal),sizegrid,len(leadfieldfinal)

        leadfieldfinal=leadfieldfinal.reshape([sizegrid, len(leadfieldfinal)/3/sizegrid,3])#,sizegrid], order='FORTRAN') #need to double check result to make sure rows and columns are right
        te = time()
        #print ' ' #sys.stdout.flush()
        print 'elapsed time', te-ts, 'seconds'

        self.leadfield = leadfieldfinal
        self.grid = grid

def parrallel(inputdata):
    for i in range(10000000):
        i = float(i*i)


class threaded(threading.Thread):
    def __init__(self,group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, target=target)
        self.args = args
        self.kwargs = kwargs
        return
    def run(self):
        for i in range(10000000):
            i = float(i*i)

class code(threading.Thread):
    def __init__(self,group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, target=target)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):

        #logging.debug('running with %s and %s', self.args[0], self.kwargs)
        #print self.args[0]

        #grid, pos, ori, cent
        grid = self.args[0]
        pos = self.args[1]
        ori = self.args[2]
        cent = self.args[3]
        #queue = self.args[4]
        chp = pos - cent
        loc = grid - cent
        #print 'center of sphere', cent,loc


        gridshape=shape(loc)
        if len(gridshape) == 1:
            loc=array([loc])#loc[1,3]

        lf=array([])
        #pbar = progressbar.ProgressBar().start()
        #for j in range(0,len(loc)): #for each grid point
        "for each R point (chp) calculate the leadfield"
        #sys.stdout.flush()
        #pbar.update((float(j)/float(len(loc)))*100)
        nchans = len(chp)
        R=loc[0]#[j,:]
        #print 'shapeR',shape(R)
        position=chp;position=chp
        orientation=ori;orientation=ori
        lftmp = zeros((nchans,3),float);
        tmp2 = norm(R);

        for i in range(0,nchans):
            t = position[i];#print 'tshape',shape(t),shape(R)
            o = orientation[i]
            tmp1 = norm(t);
            tmp3 = norm(t-R);
            tmp4 = dot(t,R);
            tmp5 = dot(t,t-R);
            tmp6 = dot(R,t-R);
            tmp7 = (tmp1*tmp2)**2 - tmp4**2; #% cross(r,R)**2
            #tmp7=tmp7
            alpha = 1 / (-tmp3 * (tmp1*tmp3+tmp5));
            A = 1/tmp3 - 2*alpha*tmp2**2 - 1/tmp1;
            B = 2*alpha*tmp4;
            C = -tmp6/(tmp3**3);
            beta = dot(A*t + B*R + C*(t-R), o)/tmp7;
            lftmp[i,:] = cross(alpha*o  + beta*t, R);

        #lf = append(lf, 1e-7*lftmp); #% multiply with u0/4pi
        lf = lf*1e-7
        #print lf
        #queue.put(lf)
        #queue.task_done()
        #queue.join()
        #return

class MyThreadWithArgs(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        print 'running'#,self.args,self.kwargs
        return
