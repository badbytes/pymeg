#mri image overlay subplot

from pylab import subplot,plot,imshow, show, figure
from numpy import sqrt, ceil, hstack, zeros

def compute(underlay, overlay):
    if len(overlay.data.shape) > 3: #4D mri, first D is time
        axisD = 1
    else: #3D mri
        axisD = 0

    ul = underlay
    rf = nansum(ul.getQForm()/ overlay.getQForm(),axis=0)[0:3]*100 #get resample factor(s)
    rf1 = rf[0] #assuming uniform decimation
    squaresize = ceil(sqrt(overlay.data.shape[axisD]))
    #ulsquaresize = ceil((underlay.data.shape[0]/rf))
    try: del a; del u
    except NameError: pass
    for i in range(0, overlay.data.shape[axisD]): #for each slice
        print i
        try:
            #a = append(a,overlay.data[axisD][i].T)
            a = hstack((a,overlay.data[axisD][i].T))
            u = hstack((u,underlay.data[i*rf1].T))
        except NameError:
            a = overlay.data[axisD][i].T
            u = underlay.data[i*rf1].T
        #subplot(squaresize, squaresize, i+1)
        #imshow(overlay.data[axisD][i].T)
        #axis('off')

t = zeros((a.shape[0],(((a.shape[0]*squaresize)*squaresize)-a.shape[1])))
a = hstack((a,t)) #make longer so can make it square.

sizexy = ceil(sqrt(a.shape[1]/a.shape[0]))
tmp = zeros((sizexy*a.shape[0],sizexy*a.shape[0]))
for i in range(0, squaresize):
    print i
    #tmp[0+(i*a.shape[0]):a.shape[0]+(i*a.shape[0])+a.shape[0],:] = a[:,0+(i*a.shape[0]):a.shape[0]*sizexy]
    tmp[0+(i*a.shape[0]):(i*a.shape[0])+a.shape[0],:] = a[:,0+(i*a.shape[0]*sizexy):(a.shape[0]*sizexy)+(i*a.shape[0]*sizexy)]


tt = interp_array.rebin(a, (181,3982))
f = ndimage.gaussian_filter1d(tt, 8, axis=0)
f = ndimage.gaussian_filter1d(f, 8, axis=1)

#b = a.reshape(18,396, order='F')
imshow(flipud(a))
axis('off')
