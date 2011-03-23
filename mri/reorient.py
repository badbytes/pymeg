'''set nifti qform using dicom image orientation
'''
from numpy import flipud, fliplr, swapaxes, argmax, array
from nifti import *

def qform(data, orientcosines):
    '''data = nifti file
    orientcosines =  list of len = 6, ex [.01, .99, .0, .0,.12,-.99]'''
    if len(shape(data)) != 3:
        print 'needs to be 3D'
        return
    a = argmax(abs(array(orientcosines[0:3])))
    b = argmax(abs(array(orientcosines[3:6])))
    
    #NO Flipping, lets just make use of the QForm fields in nifti header to define the orientation
    qform = x=array([[1.,0,0,0],[0,-1.,0,0],[0,0,-1.,0],[0,0,0,1.]], dtype=float32) #starting qform
    #x=array([[1.,0,0,0],[0,0,-1.,0],[0,-1.,0,0],[0,0,0,1.]], dtype=float32)
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

        
def flip(mrdata, orientcosines):
    
    '''make axial
    data = nifti file
    orientcosines =  list of len = 6, ex [.01, .99, .0, .0,.12,-.99]'''

    a = argmax(abs(array(orientcosines[0:3])))
    b = argmax(abs(array(orientcosines[3:6])))
    
    if a+b == 3: #sagital
        #exchange 2nd and 3rd dimensions
        mrdata = swapaxes(mrdata,1,2)

    if a+b == 2: #axial
        pass
    if a+b == 2: #coronal
        #exchange 2nd and 3rd dimensions
        mrdata = swapaxes(mrdata,1,2)
