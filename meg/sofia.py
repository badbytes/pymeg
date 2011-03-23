'''sofia'''

# concentration problem

# ROI concentration = lfall_X248X3 * lf_ROIX248X3
# Entire concentration = lfall_X248X3 * lf_AllGridX248X3


##rc = lf.leadfield
##
##rc = dot(lf.leadfield,lf.leadfield[newxyz-3:newxyz+3].T)

ROI = array([99,100,101,102]) #ROI grid points

#EXT = arange(0,size(lf.leadfield,0),1)
EXT = append(arange(0,99,1),arange(103,244,1))

#EXT = EXT.append(
##LFext = zeros([size(lf.leadfield,0)-size(ROI),size(lf.leadfield,1),size(lf.leadfield,2)]) #empty ext mat
##for e in range(0, size(lf.leadfield,0)): #for each grid point
##    if 
##    LFext[



def euclid(X1, X2, Y1, Y2, Z1, Z2):
    #or could use ... sqrt(sum((x - y)**2))
    s = sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2));
    return s

for i in range(0, 2): #for each angle (x,y,z)
    
    P = dot(lf.leadfield[:,:,i].T,lf.leadfield[:,:,i])
    U,q,Uh = svd(P)
    M,N = shape(P)
    Q = mat(diagsvd(q,M,N))

    #Oi = array([])
    ##for ch in range(0, 248):
    ##    Oi = dot(1/sqrt(q[ch]),dot(U,lf.leadfield[:,:,0].T))
    Oi = (1/sqrt(q))*dot(U,lf.leadfield[:,:,i].T).T



    Pext_ij = dot(Oi[EXT].T,Oi[EXT])
    Pint_ij = dot(Oi[ROI].T,Oi[ROI])
    
    #U,q,Uh = svd(Pext_ij)

    V,qext,Vh = svd(Pext_ij)
    V,qint,Vh = svd(Pint)
    
    
    
'''lbex'''


distmat=zeros([size(lf.grid ,0), size(lf.grid ,0)]); #create empty matrix 248X248
for i in range(0,size(lf.grid,0)):# %get euclid dist between grid points
    for ii in range(0,size(lf.grid ,0)):
        distmat[i,ii] = euclid(lf.grid[i,0], lf.grid[ii,0],\
        lf.grid[i,1], lf.grid[ii,1], \
        lf.grid[i,2], lf.grid[ii,2]);
        
        
distmatcut = copy(distmat)
#get closest gridpoints
pnt = 200
ROI = array([pnt],dtype='int') 
x = distmat[pnt] == nanmin(distmatcut[pnt])
distmatcut[pnt][x]=nan #pop off itself since its 0m from itself
for i in range(0, 3): #10 closest points
    x=distmatcut[pnt] == nanmin(distmatcut[pnt])  #get next point
    ROI = append(ROI,nonzero(x == True))
    distmatcut[pnt][x]=nan #pop off

wi = zeros([size(lf.leadfield,1),3]) #square matrix for eigenvalues
ci = zeros([size(lf.leadfield,1),size(lf.leadfield,1),3]) #3D square matrix for eigenvectors

'''lfp = permute(lfr,[3,1,2]); 3X255X248
lfint = reshape(lfp(:,ROI,:),3*9,248); 27X248
lfext = reshape(lfp(:,:,:),3*255,248); 765X248
[v,d] = eig(lfint'*lfint, lfext'*lfext);'''
numch = size(lf.leadfield,1)
numgrid = size(lf.leadfield,0)
lfp = rollaxis(lf.leadfield, 1,0).T
lfint = reshape(lfp[:,ROI,:],[3*size(ROI,0),numch])
lfext = reshape(lfp[:,:,:],(3*numgrid,numch))

w,c = eigh(dot(lfint.T,lfint), dot(lfext.T,lfext))

##for i in range(0, 3): #for each angle (x,y,z)
##    Dint = dot(lf.leadfield[ROI,:,i].T,lf.leadfield[ROI,:,i])
##    Dext = dot(lf.leadfield[:,:,i].T,lf.leadfield[:,:,i])
##    #e = linalg.eigh(P)
##    w,c = eig(Dint, b=Dext)
##    wi[:,i] = w
##    ci[:,:,i] = c    
    
figure();plot(sort(nanmax(e[1],axis=1))[::-1]);show()

wint,cint = eigh(Dint)
wext,cext = eigh(Dext)

kint = dot(vint,Dint) #k = CK
kext = dot(vext,Dext) #k = CK

kmn_int = dot(kint.T,kint)
kmn_ext = dot(kext.T,kext)

cdint = dot(dot(cint.T,Dint),cint) #EigVec.T*DeltaROI*EigVec
cdext = dot(dot(cext.T,Dext),cext) #EigVec.T*DeltaROI*EigVec

# Cmt*Delta*Cn  ... EigVec(transposed)*P*EigVec 
Dmdmn_int = dot(dot(vint.T,Pint),vint)
Dmdmn_ext = dot(dot(vext.T,Pext),vext)



Y = dot(e[1].T,e[1])