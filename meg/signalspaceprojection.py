#       sourcespaceprojection.py
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
Can do SSP with leadfields with angle vector qn or using weights
from meg import sourcespaceprojection
from meg import leadfield
from pdf2py import pdf
p = pdf.read('path2pdf')
p.data.set.channels('meg')
xyz = array([ 0.501 ,  -5.756 ,   7.504])
qxqyqz = array([0.935  ,  0.184 ,   0.347])
lf = leadfield.calc(p, p.data.channels, xyz)
sourcespaceprojection.calc(data, L=lf, qn=qxzyqz || weight=weight2use)

'''

from numpy import invert,linalg, shape,array, dot, zeros, transpose, squeeze, size, float, int, mean,sqrt,abs
from scipy import linalg

def calc(data, L=None, qn=None, weight=None):
    if L != None:
        Li=linalg.pinv(squeeze(L)); #3x248 inverted leadfield

    #s=(qn.conj().transpose())*(Li) #s=(qn')*(Li);
    if qn != None:
        'source space projection'
        #s=dot(qn,Li).transpose();
        s = dot(dot(data,Li.T), qn/linalg.norm(qn))#q(t) = B(r,t) * L-1 (rq, r) * (q(rq) / |q(rq)|)from Ross
        #s = dot(dot(data,Li.T), qn/sum(qn))
        return s
    if weight != None:
        print 'weight projection'
        if size(weight.shape,0) == 1:
            print 'finite projection'
        else: #dynamic projection
            print 'dynamic projection'
            #s=weight.transpose();
            #s = dot(data, weight/sum(weight))
        #s = dot(data, (linalg.pinv([weight/(weight.max()-weight.min())*2])))
        s = dot(data, (weight/linalg.norm(weight)).T)
        return s

    SSPvirch=zeros((shape(data)[0],1),float) #make an empty virchan array. Should by number of timepoints X 1.
    datadim = shape(data) #data dimensions. Assuming 2D for now. Maybe later can accomadate 3D.
    nump = datadim[0] #number of points
    print 'num of pnts', nump

    if size(s.shape,0) == 1: #'finite weight projection'
        print 'finite weighting'
        for eachpoint in range(0,nump):
            SSPvirch[eachpoint,0] = array(dot(data[eachpoint,:],s))
        return SSPvirch #, s
    else:
        if (int(nump)/size(s,1) - float(nump)/size(s,1)) != 0: #frames not evenly divisable by data, can't do dynamic projection
            print "frames not evenly divisable by data, can't do dynamic projection"

            return
        print size(s,1), int(nump)/size(s,1)
        for pntframe in range(0,int(nump)/size(s,1)): #for each frame
            for pntweight in range(0, size(s,1)): #for each point in weight
                stepind = pntframe*size(s,1)+pntweight
                SSPvirch[stepind,0] = array(dot(data[stepind,:],s[:,pntweight]))


        return SSPvirch


