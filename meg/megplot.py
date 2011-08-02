"""plot MEG data"""
#from msiread import getposted
import numpy
from pylab import plot,show,text,axis,grid,yticks

"from meg import megplot"
"megplot.display(data)"

#def display(data):
    #dmin=numpy.min(data)
    #dmax=numpy.max(data)
    #step=abs(dmin+dmax/2)
    #inc=0
    #for i in range(0,len(data)):
        #plot(data[i,:]+inc)
        #inc=step+inc

    #show()


def display(data):
    '''shape of data should be Times X Channels'''
    dmin=numpy.min(data)
    dmax=numpy.max(data)
    step=-abs((dmin+dmax)*5)
    print 'step',step
    inc=0
    for i in range(0,numpy.size(data,1)):
        plot(data[:,i]+inc)
        inc=step+inc
        text(-12,inc-step/2,i)



    show()
    #axis('off')
    yticks([])
    grid('on')

if __name__ == "__main__":
    pdf=getposted.read()
    slices = pdf.GetSliceRangeMEGChannels(0, 3390)#pdf.n_slices)
    plotmeg(slices)
