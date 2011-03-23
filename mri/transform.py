# Copyright 2008 Dan Collins
#
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

#'credit to eugene kronberg for use of his code for some of this transform'

#bugfix-090402-danc-'Bug in z= cross and y= cross sections of meg2mri function fixed'

from numpy import *
from scipy import linalg
#from numpy import linalg
#from pylab import norm #depreciated
from numpy.linalg import norm
from pdf2py import pdf

'''dip = N X 3
lpa rps and nas = 1X3
###make sure coords are in mm and not cm
NOT SURE ABOUT UNITS HERE. is mm or cm important'''

def generic(p1,p2,p3):
    '''return generic transform matrix from 3 points'''
    origin = mean([[p1],[p2]],0)
    x = p3 - origin;
    x = x/norm(x);
    y = p2 - origin;
    z = cross(x,y);
    z = z/norm(z);
    y = cross(x,z);
    y = y/norm(y);

    transformvector = origin; #translation
    transformmatrix = concatenate((x, y, z)); #rotation
    return transformvector,transformmatrix #ie translation and rotation

def meg2mri(lpa,rpa,nas, dipole=None):
    'requires lpa, rpa, and nas. Dipole is optional (dipole=NX3)'
    print 'what are your units of your dipole and lpa,rpa,nas?, should be in mm'
    origin = mean([[lpa],[rpa]],0)
    x = nas - origin;
    x = x/norm(x);
    y = rpa - origin;
    z = cross(x,y);
    z = z/norm(z);
    y = cross(x,z);
    y = y/norm(y);

    transformvector = origin; #translation
    transformmatrix = concatenate((x, y, z)); #rotation

    if dipole != None:
        xyz = dipoletransform(dipole, transformvector, transformmatrix)
        return xyz
    else:
        return transformvector,transformmatrix #ie translation and rotation

def dipoletransform(dipole, transformvector, transformmatrix):
        dip=dipole
        print 'dipole transform'
        if size(dip.shape) == 1: #convert to 2D
            dip = array([dip])
        t=tile(transformvector,(len(dip),1));
        xyz = dot(transformmatrix.T, dipole.T).T+transformvector
        print 'note: coordinates returned are in the MRI convention R/L,P/A,I/S'
        #print 'The convention for the mriviewer is R/L,P/A,I/S'
        print 'to use with nifti orient=0 files (I/S,P/A,I/S) we need to use flipup(xyz,1,axis=0)'
        return xyz

def mri2meg(translation,rotation, mrixyz):
    'requires rotation and translation matrix and the mrixyz (3XN)'
    print 'what are your units?'
    trep=tile(translation.transpose(),size(mrixyz,1)).reshape([size(mrixyz,0),size(mrixyz,1)])
    megxyz = dot(rotation, (mrixyz - trep));

    return megxyz

def scalesourcespace(datapdf, megxyz, lpa, rpa, nas, voxdim, brain='no'):
    #megxyz = dec.megxyz
    #lpa = eval(dec.origimg.description)[0]
    #rpa = eval(dec.origimg.description)[1]
    #nas = eval(dec.origimg.description)[2]
    #voxdim = dec.origimg.voxdim
    print 'what are your units?', 'assuming cm'
    scale = 1000 #from meters (hs.index points) to mm.
    p=pdf.read(datapdf)
    sx=abs(p.hs.index_nasion[0])+abs(min(p.hs.hs_point[:,0])); #from nas to back of head
    sy=abs(p.hs.index_lpa[1])+abs(p.hs.index_rpa[1]); #from lpa to rpa
    sz=abs(max(p.hs.hs_point[:,2])); #top of head
    mriLRdim = (lpa*voxdim - rpa*voxdim)[1]#166; #lpa to rpa in mri
    mriAPdim = (((lpa[0]+rpa[0])/2)-nas[0])*2#211;  #nas to center of head X 2
    mriISdim = mriLRdim/1.11 #this is a guess. based on standard ch brain, the AP to IS ratio is 1.11
    scalemegx=mriAPdim/(sx*scale); print 'xfactor',scalemegx
    scalemegy=mriLRdim/(sy*scale); print 'yfactor',scalemegy
    scalemegz=mriISdim/(sz*scale); print 'zfactor',scalemegz
    sourcespacescaledmegx=megxyz[0,:]*scalemegx;
    sourcespacescaledmegy=megxyz[1,:]*scalemegy;
    sourcespacescaledmegz=megxyz[2,:]*scalemegz;
    #sourcespacescaledmeg=[]
    sourcespacescaledmeg=array([sourcespacescaledmegx,sourcespacescaledmegy,sourcespacescaledmegz]);
    #sourcespacescaledmeg=sourcespacescaledmeg#.transpose()
    if brain == 'yes':
        print 'your using a brain sourcespace. adding additional scaling factor of 1.1'
        sourcespacescaledmeg = sourcespacescaledmeg/1.1
    else:
        print 'your using a full head sourcespace (not a skullstripped image). no additional scaling'
    return sourcespacescaledmeg

def crossproduct(a,b):
    C_0 = a[1]*b[2] - a[2]*b[1]
    C_1 = a[2]*b[0] - a[0]*b[2]
    C_2 = a[0]*b[1] - a[1]*b[0]
    return [C_0, C_1, C_2]

def normalize(a):
    B_0 = (a[0])/(((a[0]**2)+(a[1]**2)+((a[2])**2))**(1/2))
    B_1 = (a[1])/(((a[0]**2)+(a[1]**2)+((a[2])**2))**(1/2))
    B_2 = (a[2])/(((a[0]**2)+(a[1]**2)+((a[2])**2))**(1/2))
    return [B_0, B_1, B_2]

def rotation_matrix(first, second):
    U = matrixmultiply(first, second)
    return U

if __name__ == '__main__':
    transform()


