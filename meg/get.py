"""Return sensors and headshape positions"""

from msiread import getposted
from numpy import *

pdf=getposted.read()
hs=pdf.head_shape.hs_points
m=pdf.GetSignalMEGDevices()
x=[]; y=[]; z=[];

class headshape():
    """hs=pos.headshape.hsm"""
    hsa=array(hs)
    hsm=zeros((size(hsa),3))
    for i in range(len(hsa)):
        hsm[i,:]=( hsa[i].x, hsa[i].y, hsa[i].z);

class sensors():
    """chu=pos.headshape.chu"""
    """chl=pos.headshape.chl"""
    cha=array(m)
    chl=zeros((size(cha),3))
    chu=zeros((size(cha),3))
    for i in range(len(cha)):
        chl[i,:]=( cha[i].loops[0].Position.x, cha[i].loops[0].Position.y, cha[i].loops[0].Position.z);
        chu[i,:]=( cha[i].loops[1].Position.x, cha[i].loops[1].Position.y, cha[i].loops[1].Position.z);
        
class plot(headshape):
    def __init__(self,data):
        headshape.__init__(self)
        import pylab as p
        import matplotlib.axes3d as p3
        fig=p.figure()
        ax = p3.Axes3D(fig)
        ax.scatter(data[:,0],data[:,1],data[:,2])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        mn=data.min()
        mx=data.max()
        ax.set_xlim(data[:,0].min(),data[:,0].max())
        ax.set_ylim(data[:,1].min(),data[:,1].max())
        ax.set_zlim(data[:,2].min(),data[:,2].max())
        p.show()
    