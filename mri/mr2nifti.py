'''purpose is to take the output of pydicom and write a nifti formated file
mr = mr2nifti.start(dataarray, filename2saveas)
'''


from nifti import *
from numpy import argmax, array, abs, int16, shape, float32, flipud, fliplr \
,swapaxes, round_, zeros, sum, reshape, append, tile, copy

def check(mr):
    try:
        mr.imageorientation
        return 1
    except:# ValueError:
        print 'mr attribute imageorientation not in existence.'
        return -1

def setqform(orientcosines):
    '''data = nifti file
    orientcosines =  list of len = 6, ex [.01, .99, .0, .0,.12,-.99]'''

    a = argmax(abs(array(orientcosines[0:3])))
    b = argmax(abs(array(orientcosines[3:6])))

    #NO Flipping, lets just make use of the QForm fields in nifti header to define the orientation
    qform = x=array([[1.,0,0,0],[0,-1.,0,0],[0,0,-1.,0],[0,0,0,1]], dtype=float32) #starting qform
    if a+b == 3: #sagital
        #exchange 2nd and 3rd dimensions
        qform[1,:] = [0,0,-1.,0]
        qform[2,:] = [0,-1,0,0]
    if a+b == 2: #axial
        pass
    if a+b == 2: #coronal
        #exchange 2nd and 3rd dimensions
        qform[1,:] = [0,0,-1.,0]
        qform[2,:] = [0,-1,0,0]

    #nim = NiftiImage(int16(data))
    return qform

def get_qform(orientcosines, pixdim):
    '''orientcosines =  list of len = 6, ex [.01, .99, .0, .0,.12,-.99]'''
    a = argmax(abs(array(orientcosines[0:3])))
    b = argmax(abs(array(orientcosines[3:6])))
    print a,b, orientcosines
    r = round_(array(orientcosines))
    rotmat = zeros([4,4]);
    rotmat[0][0:3] = r[0:3]
    rotmat[1][0:3] = r[3:6]
    rotmat[2][sum(rotmat,axis=0)[0:3] == 0] = 1
    rotmat[3][3] = 1

    qform = reshape(append(tile(append(pixdim,0),[3,1])*rotmat[0:3],[0,0,0,1]),[4,4])
    return qform

def reorient(mrdata, orientcosines, pixdim):
    '''make axial
    data = nifti file
    orientcosines =  list of len = 6, ex [.01, .99, .0, .0,.12,-.99]'''
    print 'mr2nifti reorient'

    pixdimnew = copy(pixdim)
    a = argmax(abs(array(orientcosines[0:3])))
    b = argmax(abs(array(orientcosines[3:6])))
    print a,b, orientcosines

    qform = array([[pixdim[0],0,0,0],[0,pixdim[1],0,0],[0,0,pixdim[2],0],[0,0,0,1]], dtype=float32)

    if a+b == 3: #sagital
        #exchange 2nd and 3rd dimensions
        print 'sagital to axial reorient'
        if orientcosines[0:3][a] < 0: #Post to Anterior... flip
            mrdata = flipud(mrdata)
            print 'flipping 1st dim'
        if orientcosines[3:6][b] < 0: #Superior to Inferior... flip
            mrdata = fliplr(mrdata)
            print 'flipping 2nd dim'
        mrdata = swapaxes(mrdata,1,2) #swap 2nd and 3rd dim to make axial

    if a+b == 1: #axial
        print 'axial orient'
        print 'NOTE: Transposing data .T because pydicom order is 3,2,1'
        mrdata = swapaxes(mrdata.T,0,1) #swap 1st and 2nd dim to make MEG like
        qform[0]=[0,pixdim[0],0,0];
        qform[1]=[0,0,pixdim[1]*-1,0];
        qform[2]=[pixdim[2],0,0,0];
        if orientcosines[0:3][a] < 0: #Left to Right... flip
            mrdata = mrdata[:,::-1,:]
            print 'flipping 1st dim'
            qform[0]=qform[0]*-1
        if orientcosines[3:6][b] < 0: #Post to Anterior... flip
            mrdata = mrdata[:,:,::-1]
            print 'flipping 2nd dim'

    if a+b == 2: #coronal
        #exchange 2nd and 3rd dimensions
        print 'coronal to axial reorient'
        mrdata = swapaxes(mrdata,1,2) #swap 2nd and 3rd dim to make axial
        if orientcosines[0:3][a] < 0: #Left to Right... flip
            mrdata = mrdata[:,::-1,:]
            qform[0]=[0,pixdimnew[0],0,0];
            print 'flipping 1st dim'
        if orientcosines[3:6][b] < 0: #Superior to Inferior... flip
            mrdata = mrdata[:,:,::-1]
            qform[0]=[0,pixdim[0]*-1,0,0];
            qform[1]=[0,0,pixdim[2]*-1,0];
            qform[2]=[pixdim[1],0,0,0];
            print 'flipping 2nd dim'

    print qform
    return mrdata, qform


def start(mr, fn, method='reorient'):
    '''mr2nifti.start(mrobject, niftifilename2write)'''
    if check(mr) == -1:
        return
    for i in mr.seqdict.keys():
        if method == 'reorient':
            print 'reorienting', mr.datareshaped[i].shape, mr.imageorientation[i], mr.pixdim[i]
            redata,qform = reorient(mr.datareshaped[i], mr.imageorientation[i], mr.pixdim[i])
            nim = NiftiImage(int16(redata))
            nim.setQForm(qform)

        fnbase = fn.split('.')[0]
        fnnew = fnbase+i+'.nii.gz'

        print 'writing',fnnew
        nim.save(fnnew)

    #return redata

