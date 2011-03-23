'''spatial filter
f = spatialfilter.applyfilter(p.data.data_block, a)
where a is the filter. for static filter a should be same length as last dim of data
'''

from numpy import invert,linalg, shape,array, dot, zeros, transpose, squeeze, size

class applyfilter():
    '''f = spatialfilter.applyfilter(p.data.data_block, a)
    where a is the filter. for static filter a should be same length as last dim of data'''
    def __init__(self, data, weight):
        res = self.checksizes(data,weight)
        if res == 'dynamic': self.dynamic(data, weight)
        if res == 'static': self.static(data, weight)


    def checksizes(self, data, weight):
        if len(shape(weight)) == 2: # try dynamic
            if len(shape(data)) == 2: #weight assumed to be same exact dimensions as data ie 100X248 & 100X248
                if len(weight) != len(data):
                    print('mismatch between data and weight. had assumed they were equal')
                    print('lets try to reshape your 2D data into 3D and try again')
                    try:
                        data = data.reshape((size(data,0)/size(weight,0),size(weight,0),size(weight,1) ))
                    except ValueError:
                        print('cant reshape to work with filter. goodbye')
                        return

                    print 'reshaped'

                else:
                    return 'dynamic'
            else:
                print('2d weight to 3d data filtering')

        if len(shape(weight)) == 1:
            if size(data,-1) != size(weight,0): #error
                print('error. your last dim of data needs to match filter vector!', size(data,-1), size(weight,0))
                return
            else: #aok
                return 'static'


    def static(self, data, weight):
        print('computing filtered results')
        #a = p.data.data_block[207] #spatial filter
        dp = dot(data, weight/linalg.norm(weight)) #dot product of data and |filter|
        self.spatialfilter_result = (dot(array([weight]).T,array([dp]))/linalg.norm(weight)).T #spatial filter component
        self.spatialfilter_reverse = data - self.spatialfilter_result #removing component from original


    def dynamic(data, weight):
        print('doing dynamic')
        pass

##---old wrong method---
#def calc(data, sfilter):
    #print('this method is wrong')
    #sfilter=sfilter.transpose(); #result 248x1

    #SFvirch=zeros((shape(data)[0],1),float) #make an empty virchan array. Should by number of timepoints X 1.
    #datadim = shape(data) #data dimensions. Assuming 2D for now. Maybe later can accomadate 3D.
    #nump = datadim[0] #number of points

    #for eachpoint in range(0,nump):
        #SFvirch[eachpoint,0] = dot(data[eachpoint,:],sfilter)
    #return SFvirch


