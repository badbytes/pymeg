from numpy import *

def run(posmat, xyz):
    '''expecting a n by 3 array as posmat and an
    x,y,z to fit against
    ex. x=.025;y=3.479,z=8.517;'''
    
    if len(xyz.shape) == 1:
        xyz=array([xyz])
    if len(xyz.shape) == 2:
        xyz=array(xyz[0])
    
    x = xyz[0];
    y = xyz[1];
    z = xyz[2];
    
    if size(posmat,1) != 3: #check grid dimensions
        if size(posmat,0) != 3:
            print 'grid dimensions wrong'
            return
        posmat = posmat.transpose()
        print 'reshaping grid'
    minvec = copy(posmat)
    for i in range(0, size(posmat,0)):
        minvec[i,:] = posmat[i,:]-[x,y,z];
        
    sqvec = sqrt(minvec[:,0]**2+minvec[:,1]**2+minvec[:,2]**2);
    
    minpos = where(sqvec == min(sqvec))
    return squeeze(minpos)
