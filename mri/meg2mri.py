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

from numpy import *
from scipy import linalg
from pylab import norm

'''dip = N X 3
lpa rps and nas = 1X3
    make sure coords are in mm and not cm'''
def transform(lpa, rpa, nas, dipole=None):
    'requires lpa, rpa, and nas. Dipole is optional (dipole=NX3)'
    origin = mean([[lpa],[rpa]],0)
    x = nas - origin;
    x = x/norm(x);
    y = lpa - origin;
    z = cross(y,x);
    z = z/norm(z);
    y = cross(x,z);
    y = y/norm(y);
    transformvector = origin; #translation
    transformmatrix = concatenate((x, y, z)); #rotation
    
#meg2mri
    if dipole != None:
        print 'no dipole transform'
        t=tile(transformvector,(len(dip),1));
        xyz = dot(transformmatrix, dip.transpose())+t.transpose();
        return xyz
    else:
        return transformvector,transformmatrix
    
if __name__ == '__main__':
    transform()

    
