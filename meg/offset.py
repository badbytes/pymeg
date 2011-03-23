#offset correct
from numpy import mean, shape

##class correct:
##    def __init__(self, data, start=0, end=-1, fn='filename'):
##            m=mean(data[start:end,:],0)
##            self.data=data-m;
##            #return datacorrected

def correct(data, start=0, end=-1):
    if len(shape(data)) == 1:
        print 'Data 1 dimensional vector, no offseting needed'
        return -1
    m=mean(data[start:end,:],0)
    datacorrected=data-m;
    return datacorrected
