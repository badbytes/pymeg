from numpy import *

def calc(lf, dat,noisecov=None):

    Nchan = lf.leadfield.shape[1];
    #count leadfield components
    Nsource = 0;
    for i in range(0, lf.leadfield.shape[0]):
        Nsource = Nsource + size(lf.leadfield, 0);

    #concatenate the leadfield components of all sources into one large matrix
    Lf = zeros([Nchan, Nsource]);
    n = 1;
    for i in range(0, size(lf.grid,0)):
        cbeg = n;
        cend = n + size(lf.leadfield[i], 1) - 1;
        Lf[:,cbeg:cend] = lf.leadfield[i];
        n = n + size(lf.leadfield[i], 1);
    
    self.Lf = Lf
    return

    if noisecov == None:
        w = linalg.pinv(lf.leadfield)
    else:
        #the noise covariance has been given and can be used to regularise the solution
        if sourcecov == None:
            sourcecov = eye(Nsource)
            
        #rename some variables for consistency with the publications
        A = lf.leadfield
        R = sourcecov;
        C = noisecov;
        # the regularisation parameter can be estimated from the noise covariance, see equation 6 in Lin et al. 2004
        #5 was used for the signal-to-noise ratio (SNR),
        snr = 5
        if lambDa == None:
            lambDa = trace(dot(dot(A , R) , A.transpose()))/dot((trace(C),snr**2))
            # equation 5 from Lin et al 2004 (this implements Dale et al 2000, and Liu et al. 2002)
            w = dot(dot(R , A.transpose()) , inv( dot(dot(A , R) , A.transpose()) + dot((lambDa**2) , C)))
            
    #for each of the timebins, estimate the source strength
    mom = dot(w , dat.transpose());

    n = 1;
    dipoutmom = zeros(Nchan, Nsource);
    for i in range(0, lf.grid.shape[0]):
        cbeg = n;
        cend = n + size(lf.leadfield[i], 1) - 1;
        dipoutmom[i] = mom[cbeg:cend,:];
        n = n + size(lf.leadfield[i], 1);