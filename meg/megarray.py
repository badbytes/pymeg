"""Return sensors and headshape positions"""

from msiread import getposted
from numpy import zeros, array, size

pdf=getposted.read()
hs=pdf.head_shape.hs_points
m=pdf.GetSignalMEGDevices()
x=[]; y=[]; z=[];

class headshape():
    "get headshape data"
    def data(self): # define class methods
        """hs=pos.headshape.hsm"""
        hsa=array(hs)
        hsm=zeros((size(hsa),3))
        for i in range(len(hsa)):
            hsm[i,:]=( hsa[i].x, hsa[i].y, hsa[i].z);
        self.data = hsm        # self is the instance



class sensors():
    """chu=pos.headshape.chu"""
    """chl=pos.headshape.chl"""
    cha=array(m)
    chl=zeros((size(cha),3))
    chu=zeros((size(cha),3))
    for i in range(len(cha)):
        chl[i,:]=( cha[i].loops[0].Position.x, cha[i].loops[0].Position.y, cha[i].loops[0].Position.z);
        chu[i,:]=( cha[i].loops[1].Position.x, cha[i].loops[1].Position.y, cha[i].loops[1].Position.z);
        

    

class display(headshape, sensors):
    def plot3d(self):
        data=self.data
        print data
        "plot headshape or sensors"
        import pylab as p
        import matplotlib.axes3d as p3
        fig=p.figure()
        ax = p3.Axes3D(fig)
        ax.scatter(self.data[:,0],self.data[:,1],self.data[:,2])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        mn=data.min()
        mx=data.max()
        ax.set_xlim(self.data[:,0].min(),self.data[:,0].max())
        ax.set_ylim(self.data[:,1].min(),self.data[:,1].max())
        ax.set_zlim(self.data[:,2].min(),self.data[:,2].max())
        p.show()
        