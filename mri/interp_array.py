from numpy import *

def rebin( a, newshape ):
        '''Rebin an array to a new shape.
        '''
        assert len(a.shape) == len(newshape)
        
        slices = [ slice(0,old, float(old)/new) for old,new in zip(a.shape,newshape) ]
        #print slices
        coordinates = mgrid[slices]
        indices = coordinates.astype('i')   #choose the biggest smaller integer index
        
        return a[tuple(indices)]
