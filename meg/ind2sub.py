from numpy import *

def __init__(self, matrix):
    l = len(matrix.shape) 
        
        
    ind = zeros([])
    for d in range(0, len(matrix.shape)): #for each dimension
        ind = append([
    
    
    
##    nout = max(nargout,1);
##    siz = double(siz);
##
##    if length(siz)<=nout,
##      siz = [siz ones(1,nout-length(siz))];
##    else
##      siz = [siz(1:nout-1) prod(siz(nout:end))];
##    end
##    n = length(siz);
##    k = [1 cumprod(siz(1:end-1))];
##    for i = n:-1:1,
##      vi = rem(ndx-1, k(i)) + 1;         
##      vj = (ndx - vi)/k(i) + 1; 
##      varargout{i} = vj; 
##      ndx = vi;     
##    end