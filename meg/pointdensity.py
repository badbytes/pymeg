'''point density'''

from meg import euclid
from numpy import size, zeros, array


#poximity based density method
def proximity(points, scale=None):
    '''scale is the slice thickness
    if 3D and non cubic then scale'''
    distmat=zeros([size(points ,0), size(points ,0)]);
    for i in range(0,size(points,0)):# %get euclid dist between all pairs of points
        for ii in range(0,size(points ,0)):
            distmat[i,ii] = 1/euclid.dist(  
            points[i,0], points[ii,0],\
            points[i,1], points[ii,1], \
            points[i,2], points[ii,2]);
            
    return distmat
            
            
if __name__ == '__main__':
    points = array([[1,2,3],[1,2,5],[1,2,10]])
    x=proximity(points)
    print x