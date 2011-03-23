import numpy
from numpy import shape
from pylab import figure, show, connect

##import sys
##for arg in sys.argv:
##    
##    print arg
##    data=arg


class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheen to navigate images')

        self.X = X
        rows,cols,self.slices = X.shape
        self.ind  = self.slices/2

        self.im = ax.imshow(self.X[:,:,self.ind])
        self.update()

    def onscroll(self, event):
        #print event.button
        if event.button=='up':
            self.ind = numpy.clip(self.ind+1, 0, self.slices-1)
        else:
            self.ind = numpy.clip(self.ind-1, 0, self.slices-1)

        self.update()


    def update(self):
        self.im.set_data(self.X[:,:,self.ind])
        #ax.set_ylabel('slice %s'%self.ind)
        #print self.ind        
        self.im.axes.figure.canvas.draw()

    def click(event):
        print 'you clicked', event.xdata, event.ydata
#        i=IndexTracker(ax, X)
#        print i.ind
        #return event

def __init__(self, data):
    pass
##    print data

##if __name__ == "__main__":

##def plot(data):
"mri=img.decimate(nim, 5)"
"ex. slice.plot(mri)"
X=data
fig = figure()
ax = fig.add_subplot(111)
tracker = IndexTracker(ax, X)
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
connect('button_press_event', click)
show()
