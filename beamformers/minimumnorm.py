#fn = '/home/danc/python/data/0611/0611SEF/e,rfhp1.0Hz,n,x,baha001-1SEF,f50lp'
#from pdf2py import pdf

#p = pdf.read(fn)

#p.data.setchannels('meg')
#p.data.getdata(0,p.data.pnts_in_file)
#from mri import img_nibabel

#i = img_nibabel.loadimage('/home/danc/python/data/standardmri/ch3_brain.nii.gz')
#i.decimate(50)
#from meg import leadfield

#lf = leadfield.calc(p.data.channels, grid=i.megxyz)


from numpy import *;
from scipy.linalg import *
from meg import leadfield

#noisecov = dot(p.data.data_block[0:50].T,p.data.data_block[0:50])


def calc(data,lf,noisecov):
    
    Nsource = size(lf.leadfield,2)*size(lf.leadfield,0)
    sourcecov = eye(Nsource,Nsource);#sourcecov = sparse.eye(Nsource,Nsource);
    
    #squeeze directional vector and num of sources and then reshape NumOfCh X NumSources*LeadfieldDir, ie 248X48
    lfr = swapaxes(lf.leadfield,1,2).reshape((size(lf.leadfield,0)*size(lf.leadfield,2),size(lf.leadfield,1)),order='F').T
    #return lfr
    #REDuce rank
    [u, s, v] = svd(lfr);
    s = diag(s) #make square
    r = diag(s); #take diag
    s[:] = 0;
    for j in range(0,2):
        s[j,j] = r[j];
    
    ##% recompose the leadfield with reduced rank
    #tmp = zeros((size(lfr,0),size(lfr,1))) #make not square
    #print tmp.shape,s.shape
    #tmp[:,0:size(s,1)] = s #replace
    #s = tmp #reset
    #lfrr = dot(dot(u , s) , v.T); #reconstruct
    
    #normalize lf
    nrm = sum(lfr**2)**.5 #normfact
    lfn = lfr / nrm
    
    A = lfr;
    A = lfn
    R = sourcecov; #Nsources X Nsources
    C = noisecov;
    snr = 10
    lambd = trace(dot(dot(A , R) , A.T)) / (dot(trace(C),snr**2));
    w = dot(dot(R, A.T) , inv(dot(dot(A, R), A.T) + dot(lambd**2 , C)))
    
    mom = dot(w,data.T)
    momr = mom.reshape((size(lf.grid,1),size(lf.grid,0),size(mom,1)))
    momp = sqrt(momr[0]**2 + momr[1]**2 + momr[2]**2)
    return momp.T, w.T


#w = dot(dot(R , A.T).T , inv((dot(dot( A , R).T , A) + dot(lambd**2 , C));
  #w = R * A' * inv( A * R * A' + (lambda^2) * C);
