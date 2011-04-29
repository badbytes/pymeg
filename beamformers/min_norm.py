#       min_norm.py
#       Adapted from nutmeg code for python by dan collins <danc@badbytes.net>

'''
p.data.getdata(0,p.data.pnts_in_file)
leadfieldobj = leadfield.calc(p.data.channels,grid=array([[0,40,100],[0,-40,100]]),centerofsphere=[0,0,40])
localize(p.data.data_block,leadfieldobj)
mn = min_norm.localize(p.data.data_block, leadfieldobj)
'''

'''
Adapted from nutmeg code for python by dan collins <danc@badbytes.net>

Portions of NUTMEG contain code distributed under the GNU General Public License; see GPL.txt for the text of this license. The remainder is released under the revised BSD license, as follows:
Copyright (c) 2005-2009, the authors and the UCSF Biomagnetic Imaging Laboratory
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the University nor the names of its contributors may
  be used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from scipy.linalg import eig,inv
from numpy import array,sqrt,size,zeros,squeeze,dot,eye,shape,double
from meg import leadfield
import sys


class localize:
    def __init__(self,data,leadfieldobj):
        '''
        p.data.getdata(0,p.data.pnts_in_file)
        i = img_nibabel.loadimage('/home/danc/data/standardmri/ch3_brain.nii.gz') #coregistered MRI
        i.decimate(10) #reduce source space by factor of 10.
        leadfieldobj = leadfield.calc(p.data.channels,grid=i.megxyz),centerofsphere=[0,0,40]) #calculate leadfield for reduced dimension data.
        localize(p.data.data_block,leadfieldobj)
        mn = min_norm.localize(p.data.data_block, leadfieldobj)
        '''

        Lp = leadfieldobj.leadfield

        L = Lp.swapaxes(1,2)
        a,b,c=L.shape
        L = L.reshape((a*b,c)) #6 x 248
        G = dot(L.T,L) #248 x 248

        e = eig(dot(data.T,data))
        gamma = dot(1e0,max(e[0]))
        InvG = inv(G+gamma*eye(size(G,0)));

        Lp1 = squeeze(Lp[:,:,0])
        Lp2 = squeeze(Lp[:,:,1])
        Lp3 = squeeze(Lp[:,:,2])
        w1 = zeros(shape(Lp1.T));
        w2 = zeros(shape(Lp2.T));
        w3 = zeros(shape(Lp3.T));

        for i in range(0,size(Lp,0)):
            w1[:,i] = dot(InvG,Lp1[i])
            w2[:,i] = dot(InvG,Lp2[i])#dot(InvG,array([Lp2[i]]).T).T;
            w3[:,i] = dot(InvG,Lp3[i])#dot(InvG,array([Lp3[i]]).T).T;

        weight = zeros((size(w1,0),3,size(w1,1)))
        weight[:,0,:] = w1;
        weight[:,1,:] = w2;
        weight[:,2,:] = w3;

        #from nut_activation_viewer.m
        #% We have s_th and s_ph, so we must compute s_beam (power) here:
        #if(isfield(beam,'s_z'))
            #rivets.s_beam = double(beam.s_th.^2 + beam.s_ph.^2 + beam.s_z.^2);

        vecx = dot(data,w1)
        vecy = dot(data,w2)
        vecz = dot(data,w3)

        self.voxpow = double(vecx**2 + vecy**2 + vecz**2)
        self.weight = weight
        self.grid = leadfieldobj.grid





'''--------ORIG Matlab code from NUTMEG-------------


function [weight]=nut_MinNorm(Lp,data, flags) %---------------------------------------------------------
% should make flags.cn=0; flags.wn=0;
%

% global bolts

L = reshape(Lp,size(Lp,1),size(Lp,2)*size(Lp,3));
G = L*L';
clear L;

%  gamma = 1e-1*max(eig(G)); % lead-field scale dependent (like it shouldn't matter if you are working in fT or T)
gamma = 1e0*max(eig(data.y'*data.y)); % data-dependent regularization
%    gamma = 1e-17;
InvG = inv(G+gamma*eye(size(G)));

Lp1 = squeeze(Lp(:,1,:));
w1 = zeros(size(Lp1));
Lp2 = squeeze(Lp(:,2,:));
w2 = zeros(size(Lp2));
if size(Lp,2)>2
    Lp3 = squeeze(Lp(:,3,:));
    w3 = zeros(size(Lp3));
end

for i=1:size(Lp,3)
    w1(:,i)=InvG*Lp1(:,i);
%     J = inv(sqrt(Lp1(:,i)'*InvGLp));
%     w1(:,i) = InvGLp * J;

    w2(:,i)=InvG*Lp2(:,i);
%     J = inv(sqrt(Lp2(:,i)'*InvGLp));
%     w2(:,i) = InvGLp * J;

    if size(Lp,2)>2
        w3(:,i)=InvG*Lp3(:,i);
%         J = inv(sqrt(Lp3(:,i)'*InvGLp));
%         w3(:,i) = InvGLp * J;
    end
end

weight(:,1,:) = w1;
weight(:,2,:) = w2;
if size(Lp,2)>2
    weight(:,3,:) = w3;
end
disp('done');
% end
'''
