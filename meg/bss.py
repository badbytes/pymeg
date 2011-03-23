'''R fastICA
using This is an R and C code implementation of the FastICA algorithm of Aapo Hyvarinen et al. (http://www.cis.hut.fi/aapo/) to perform Independent Component Analysis (ICA) and Projection Pursuit.
http://svitsrv25.epfl.ch/R-doc/library/fastICA/html/fastICA.html
'''


import rpy2.robjects as robjects
r = robjects.r
import rpy2.robjects.numpy2ri #to convert ndarray types to rpy2 object
r.library('fastICA')
from numpy import asarray

'''fastICA(X, n.comp, alg.typ = c("parallel","deflation"),
        fun = c("logcosh","exp"), alpha = 1.0, method = c("R","C"),
        row.norm = FALSE, maxit = 200, tol = 1e-04, verbose = FALSE,
        w.init = NULL)'''

class ICA:
    def __init__(self):#, X, ncomp, alg = "parallel", fun = "exp", alpha = 1.0, method = "C", maxit = 200, tol = 1e-04, verbose='FALSE',row = "FALSE"):
        '''i = bss.ICA()'''
        #self.ica = fastICA(X, ncomp, alg = "parallel", fun = "exp", alpha = 1.0, method = "C", maxit = 200, tol = 1e-04, verbose='FALSE',row = "FALSE")
        pass

    def convertica2array(self, inputvector):
        '''convert R data to numpy array'''
        print 'converting R data to array'
        self.I = {}; x = 0
        for j in (inputvector.names):
            m = r.matrix(inputvector)
            self.I[j] = asarray(m[x]); x = x+1
    
    def fastICA(self, X, ncomp, alg = "parallel", verbose='False',fun = "logcosh", alpha = 1.0, method = "C", maxit = 200, tol = 1e-04,row = "FALSE"):
        '''actual R fastICA command'''
        print 'calculating ICA components. Please wait'
        i = r.fastICA(X, ncomp, alg=alg, fun=fun, alpha=alpha, method="R", maxit=maxit, tol=tol, row=row)
        self.convertica2array(i)
        #self.activation(self.I)
        self.ica = i
    
    def activation(self, componentnumber):
        print 'calculating activation'
        from numpy import size, dot, zeros, shape, mean, sqrt, square
        #self.rmsact = zeros(shape(self.I['S']))
        #~ for ii in range(0, size(self.I['S'],1)):
            #~ #self.rmsact[:,ii] =  sqrt(mean(square(dot(self.I['S'][:,ii:ii+1],self.I['A'][ii:ii+1,:])), axis=1))
        ii = componentnumber
        print 'calculating act matrix from component number', ii
        self.act = dot(self.I['S'][:,ii:ii+1],self.I['A'][ii:ii+1,:])
        self.rmsact = sqrt(mean(square(self.act), axis=1))


if __name__ == '__main__':
    i = r.fastICA(e, 3, verbose='TRUE')
    
