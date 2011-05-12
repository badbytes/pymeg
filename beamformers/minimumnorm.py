#       minimumnorm.py
#       
#       Copyright 2011 danc <danc@badbytes.net>
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

'''pow, weight = minimumnorm.calc(data,leadfields,noisecovariance)

ex.
mr = img_nibabel.loadimage('/path/skullstrippedbrain.nii.gz')
mr.decimate(10)
lf = leadfield.calc(channels, grid=mr.megxyz)
noisecovariance = dot(data_block[0:50].T,data_block[0:50])
'''

from numpy import *;
from scipy.linalg import *
from meg import leadfield

def calc(data,lf,noisecov):
    
    
    Nsource = size(lf.leadfield,2)*size(lf.leadfield,0)
    sourcecov = eye(Nsource,Nsource);#sourcecov = sparse.eye(Nsource,Nsource);
    
    #squeeze directional vector and num of sources and then reshape NumOfCh X NumSources*LeadfieldDir, ie 248X48
    lfr = swapaxes(lf.leadfield,1,2).reshape((size(lf.leadfield,0)*size(lf.leadfield,2),size(lf.leadfield,1)),order='F').T
    
    ##Reduce rank
    #[u, s, v] = svd(lfr);
    #s = diag(s) #make square
    #r = diag(s); #take diag
    #s[:] = 0;
    #for j in range(0,2):
        #s[j,j] = r[j];
    
    ##% recompose the leadfield with reduced rank
    #tmp = zeros((size(lfr,0),size(lfr,1))) #make not square
    #print tmp.shape,s.shape
    #tmp[:,0:size(s,1)] = s #replace
    #s = tmp #reset
    #lfrr = dot(dot(u , s) , v.T); #reconstruct
    
    #normalize lf
    nrm = sum(lfr**2)**.5 #normfact
    lfn = lfr / nrm
    
    #A = lfr;
    A = lfn
    R = sourcecov; #Nsources X Nsources
    C = noisecov;
    snr = 10
    lambd = trace(dot(dot(A , R) , A.T)) / (dot(trace(C),snr**2));
    w = dot(dot(R, A.T) , inv(dot(dot(A, R), A.T) + dot(lambd**2 , C)))
    
    mom = dot(w,data.T)
    momr = mom.reshape((size(lf.grid,1),size(lf.grid,0),size(mom,1)))
    momp = sqrt(momr[0]**2 + momr[1]**2 + momr[2]**2)
    return momp.T, w.T

