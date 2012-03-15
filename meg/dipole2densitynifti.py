'''density calc returns the 1/euclid distance of the cartesian points supplied.
returns the distance square matrix of size numofpointsXnumofpoints.
ex.
c = array([[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3],
           [2, 2, 2]])

d = density.calc(c)

d...
array([[ 0.        ,  0.57735027,  0.28867513,  0.57735027],
       [ 0.57735027,  0.        ,  0.57735027,  1.        ],
       [ 0.28867513,  0.57735027,  0.        ,  0.57735027],
       [ 0.57735027,  1.        ,  0.57735027,  0.        ]])

gof = array([.92,.85,.99,.95])
gofscale = .9
s = gof-gofscale
sf = (1/(1-gofscale))*s
ds = d*sf

ds...
array([[ 0.        , -0.28867513,  0.25980762,  0.28867513],
       [ 0.11547005, -0.        ,  0.51961524,  0.5       ],
       [ 0.05773503, -0.28867513,  0.        ,  0.28867513],
       [ 0.11547005, -0.5       ,  0.51961524,  0.        ]])

meanvalue = mean(ds, axis=0)
and meanvalue is the value written to the MRI.
mean(ds,axis=0)
Out[89]: array([ 0.07216878, -0.26933757,  0.32475953,  0.26933757])
'''
from pdf2py import readwrite
from meg import density
from mri import transform
from scipy import ndimage
from mri import img_nibabel as img
from numpy import float32, int16, array
from pdf2py import readwrite
import nibabel,os


def handler(points,mr,gofscale=None,gof=None,sigma=3):
    report = {}
    filename = mr.nifti.get_filename()
    #try: xfm = readwrite.readdata(os.path.splitext(filename)[0]+'.pym')
    #except: print 'Error reading coregistration info'
    try:
        lpa = mr.lpa
        rpa = mr.rpa
        nas = mr.nas
    except:
        print 'Error reading coregistration info'
    #self.points = array([[0,0,0],[10,0,0],[0,20,0]])#DEBUG-----------------
    xyz = transform.meg2mri(lpa,rpa,nas, dipole=points)
    #readwrite.writedata(xyz, os.path.dirname(mripath)+'/'+'xyz')
    print 'lpa, rpa, nas', lpa, rpa, nas
    print 'xyz in mri space', xyz
    print 'pixdim', mr.pixdim

    #do some scaling of the dips using the GOF as a weight.
    #VoxDim = mr.voxdim[::-1]
    VoxDim = mr.pixdim
    xyzscaled = (xyz/VoxDim).T
    print 'xyzscaled',xyzscaled
    d = density.calc(xyz)
    if gofscale != None and gof != None:
        print 'Scaling density by gof midval of ',gofscale
        gofscale = float32(gofscale)
        print 'gofscale',gofscale
        s= gof-gofscale
        sf=(1/(1-gofscale))*s
        ds = d*sf
    else:
        print 'No density scaling'
        ds = d

    #apply a 1D gaussian filter
    z = density.val2img(mr.data, ds, xyzscaled)
    #sigma = float32(self.sigmaval.GetValue())
    print 'sigma',sigma
    #sigma = 3
    print 'filtering 1st dimension'
    f = ndimage.gaussian_filter1d(z, sigma*1/VoxDim[0], axis=0)
    print 'filtering 2nd dimension'
    f = ndimage.gaussian_filter1d(f, sigma*1/VoxDim[1], axis=1)
    print 'filtering 3rd dimension'
    f = ndimage.gaussian_filter1d(f, sigma*1/VoxDim[2], axis=2)

    scaledf = int16((z.max()/f.max())*f*1000)
    print 'writing nifti output image'
    #overlay = NiftiImage(int16(scaledf))
    overlay = nibabel.Nifti1Image(scaledf,mr.nifti.get_affine(),mr.nifti.get_header())
    #overlay = NiftiImage(int16(scaledf))
    #overlay.setDescription(mr.description)
    #filename = os.path.splitext(mr.nifti.get_filename())[0]
    #filename = mr.nifti.get_filename().strip('.nii.gz')#[0]
    #overlay.to_filename(filename+'dd.nii.gz')
    #print 'Density Image Saved', filename+'dd.nii.gz'
    #overlay.setFilename(mr.filename+'dd')
    #overlay.setQForm(mr.getQForm())

    return overlay

