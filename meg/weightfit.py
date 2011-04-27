#       weightfit.py
#
#       Copyright 2009 dan collins <quaninux@gmail.com>
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
Attribution to Source Localization of EEG/MEG Data by Correlating Columns of ICA Solution with Lead Field Matrix
    Hild, K.E.; Nagarajan, S.S.

weight fit
reload(weightfit); w=weightfit.calc(path2pdf, lfmat, winv)

'''


from numpy import *
from numpy import linalg
from scipy import *
from meg import sensors,leadfield,grid
from time import time

def setup(self): #set some things up
    lsc = ([0, 0, 4]);
    radius=10;

class calc:
    def __init__(self, path2pdf, leadfield, weight):
        '''leadfield structured, grid X channels X 3'''
        self.ext = 'pymwf'

        reducedrank=2;
        ts = time()

        if len(weight.shape) == 1: #check winv and if 1D make 2D.
            weight=array([weight])
        if size(weight,0) != size(leadfield,1): #need to reshape weight to match leadfields
            weight = weight.transpose()
            print 'weight reshaped to match leadfields'
            if size(weight,0) != size(leadfield,1): #something wrong, exit
                print 'something wrong... weight and leadfields dont match'
                return

        self.winv = winv = copy(weight) #should be channels X numofweights
        Lc=zeros((size(leadfield,1), size(leadfield,0)*2));

        for d in range(0, size(leadfield, 0)): #for each gridpoint
            u, s, vh = linalg.svd(leadfield[d,:,:]); v = vh.T
            self.u=u
            self.s=s
            self.v=v

            Lc[:,((d+1-1)*2):(d+1)*2] = u[:,0:2];
        self.Lc=Lc

        s=sensors.locations(path2pdf) #get sensor pos
        chanlocs=s.megchlpos
        chanlocsright = chanlocs[chanlocs[:,1] < 0]
        chanlocsleft = chanlocs[chanlocs[:,1] > 0]


        for i in range(0, size(winv,1)): #remove mean from matrix
            winv[:,i] = winv[:,i] - mean(winv[:,i])

        self.winv = winv
        self.winv_std = winv_std = sqrt(sum(winv**2,0));
        self.fn = fn=arange(size(leadfield,0));
        self.f = f = fn
        self.psi_reconstruct = psi_reconstruct = zeros((len(fn)*2,len(f)));

        for i in range(0,len(f)):
            L = Lc[:,(i+1-1)*2+1-1:(i+1)*2]; #check indicies
            self.L=L

            for j in range(0,size(L,1)):
                L[:,j] = L[:,j] - mean(L[:,j]);

            self.psi_tmp = psi_tmp = zeros([2,size(winv,1)]);
            self.corr_tmp = corr_tmp = zeros([size(winv,1)]);

            for j in range(0, size(winv,1)):
                #[Q,V] = linalg.eig(dot(dot(L.transpose(),winv[:,j]).reshape([2,1]),dot(winv[:,j].transpose(),L).reshape([1,2])),dot(L.transpose(),L)); # maximize normalized correlation
                w1 = dot(dot(L.transpose(),winv[:,j]).reshape([2,1]),dot(winv[:,j].transpose(),L).reshape([1,2]))
                w2 = dot(L.transpose(),L)
                self.w1 = w1
                self.w2 = w2
                self.A = A = linalg.eig(w1)#,w2); # maximize normalized correlation

                #[val,pos] = max(diag(V));
                self.pos = pos = A[0].argmax()
                self.poscopy = pos
                Q = A[1]
                if dot(Q[:,pos].transpose(),dot(L.transpose(),winv[:,j])) < 0:
                    Q[:,pos] = - Q[:,pos]; # correct the sign
                self.Q = Q
                self.psi_tmp[:,j] = psi_tmp[:,j] = Q[:,pos];

                self.L_std = L_std = sqrt(sum(dot(L,Q[:,pos])**2,axis=0));
                corr_tmp[j] = dot(dot(Q[:,pos].transpose(),L.transpose()),winv[:,j])/dot(L_std,winv_std[j]);
                self.corr_tmp = corr_tmp

            self.pos = pos = corr_tmp.argmax();
            prange = array([0,2])
            ##print 'working on', i+1, 'out of', size(f), 'gridpoints'
            psi_reconstruct[prange[0]+(i+1-1)*2:prange[1]+(i+1-1)*2,i] = psi_tmp[:,pos];
            self.psi_reconstruct = psi_reconstruct


        self.L = L = dot(Lc,psi_reconstruct);

        for i in range(0,size(L,1)):#remove mean
            L[:,i] = L[:,i] - mean(L[:,i])
        self.L = L

        #compute standard deviation of each column
        self.L_std = L_std = sqrt(sum(L**2,0));

        #compute absolute value of normalized corrrelation coefficient between columns
        #corr_mat[:,:] = NaN*ones(size(winv,1),size(leadfield, 0));
        self.corr_mat = corr_mat = zeros([size(winv,1),size(leadfield, 0)]);

        for i in range(0,len(f)):
            for j in range(0,size(winv,1)):
                corr_mat[j,f[i]] = (abs(dot(L[:,f[i]].transpose(),winv[:,j]))/dot(L_std[f[i]],winv_std[j]));


        te = time()
        print 'elapsed time', te-ts, 'seconds'
        del self.L, self.Lc, self.psi_reconstruct, self.winv, self.winv_std

from meg import euclid
from pdf2py import pdf

class bestfit(calc):
    def __init__(self, pdfdataobj, data, chind, power='off'):#, seedpoint, weight, iterations):
        '''
        p = pdf.read(path2pdf)
        p.data.setchannels('meg')
        p.data.channels.getposition()
        chind = p.data.channels.sensorpos.chlpos[:,1]>0
        '''
        p = pdf.read(pdfdataobj)
        p.data.setchannels('meg')
        p.data.channels.getposition()

        if size(data.shape) == 1: #make 2d
            data = array([data])

        numhspts = size(p.hs.hs_point,0)
        d = zeros([numhspts])
        for j in range(0, numhspts): #distance from 0,0,40 mm to all hs points
            d[j] = euclid.distarray([0,0,40],p.hs.hs_point[j]*1000)
        self.d = d

        self.n = euclid.distarray([0,0,40],p.hs.index_nasion*1000)

        numofgrids = ng = 6 #d.max()
        startgridspacing = gs = float((self.n.max()/ng)*2) #mm
        cog = centerofgrid = array([0,0,40]) #mm
        iterations = 10

        for i in range(0,iterations): #iterate over grids
            scaledgs = gs/(i+1); print 'gs',gs
            print cog,ng,scaledgs
            e = grid.sphere(cog,ng,scaledgs)
            self.e = e
            self.lf = leadfield.calc(pdfdataobj, p.data.channels, e)
            if power == 'on': #doing power localization. ABS of leadfields
                self.w = calc(pdfdataobj, abs(self.lf.leadfield[:,chind,:]), data[:,chind])
            else:
                self.w = calc(pdfdataobj, self.lf.leadfield[:,chind,:], data[:,chind])

            cog = self.lf.grid[argmax(self.w.corr_mat)]
            gof = self.w.corr_mat.max()
            print gof, cog
            gs = scaledgs
            self.bestfit = cog
            self.gof = gof
            #return


        #return cog
