#!/usr/bin/env python

# This example demonstrates how to use 2D Delaunay triangulation.
# We create a fancy image of a 2D Delaunay triangulation. Points are
# randomly generated.

# Copyright 2008 Dan Collins

# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''
Plot data points in 3D using vtk library stack
plotvtk.display(points)
'''

import vtk
from vtk.util.colors import *
from numpy import float_, tile, array, arange, shape, size, transpose,copy

'data need to be N x 3'

def vtkpoints(points, color=None, radius=None):
    # Create a polydata with the points we just created.
    profile = vtk.vtkPolyData()
    profile.SetPoints(points)

    # Perform a 2D Delaunay triangulation on them.
    delny = vtk.vtkDelaunay2D()
    delny.SetInput(profile)
    delny.SetTolerance(0.001)
    mapMesh = vtk.vtkPolyDataMapper()
    mapMesh.SetInputConnection(delny.GetOutputPort())
    meshActor = vtk.vtkActor()
    meshActor.SetMapper(mapMesh)
    meshActor.GetProperty().SetColor(.1, .2, .1)

    # We will now create a nice looking mesh by wrapping the edges in tubes,
    # and putting fat spheres at the points.
    extract = vtk.vtkExtractEdges()
    extract.SetInputConnection(delny.GetOutputPort())

    ball = vtk.vtkSphereSource()

    if radius == None:
        rad = .002
    else:
        rad = radius
    print rad
    ball.SetRadius(rad)
    ball.SetThetaResolution(50)
    ball.SetPhiResolution(5)
    balls = vtk.vtkGlyph3D()
    balls.SetInputConnection(delny.GetOutputPort())
    balls.SetSourceConnection(ball.GetOutputPort())
    mapBalls = vtk.vtkPolyDataMapper()
    mapBalls.SetInputConnection(balls.GetOutputPort())
    ballActor = vtk.vtkActor()
    ballActor.SetMapper(mapBalls)
    if color == None:
        ballcolor = red;
    else:
        ballcolor = color
    print 'setting ball color to...', ballcolor
    ballActor.GetProperty().SetColor(ballcolor)
    ballActor.GetProperty().SetSpecularColor(0, 0, 0)
    ballActor.GetProperty().SetSpecular(0.3)
    ballActor.GetProperty().SetSpecularPower(500)
    ballActor.GetProperty().SetAmbient(0.2)
    ballActor.GetProperty().SetDiffuse(0.8)
    return ballActor,profile
    
def vtkdisk(c=(0,0,1)):
    # create a rendering window and renderer
    #ren = vtk.vtkRenderer()
    #renWin = vtk.vtkRenderWindow()
    #renWin.AddRenderer(ren)
     
    # create a renderwindowinteractor
    #iren = vtk.vtkRenderWindowInteractor()
    #iren.SetRenderWindow(renWin)
     
    # create source
    
    source = vtk.vtkDiskSource()
    source = vtk.vtkCylinderSource()

    source.SetCenter(c)
    source.SetRadius(.01)
    #source.SetOuterRadius(.2)
    source.SetResolution(10)
    source.SetHeight(.001)

    #source.SetCircumferentialResolution(100)
    source.Update()
    
    
    #source2.SetCenter(.3,0,0)
    #source2.Update()
    
    
    
     
    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(source.GetOutput())
     
    # actor
    diskactor = vtk.vtkActor()
    diskactor.SetMapper(mapper)
    return diskactor
    # assign actor to the renderer
    #ren.AddActor(diskactor)
    
def vtkwindow():
    # Create the rendering window, renderer, and interactive renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ### Mouse interaction
    ##style = vtk.vtkInteractorStyleTrackballCamera()
    ##iren.SetInteractorStyle(style)
    ren.SetBackground(0, 0, 0)
    renWin.SetSize(500, 500)

    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1)
    return ren,renWin,iren

def vtkactors(actors):
    pass

def scaledata(data):
    scalefactor=(1/((data.max()-data.min())/2))*.1 #scale data to 1.0 -1.0
    data=data*scalefactor
    return data, scalefactor

#def display(data, datascalevec=None, data2=None, data3=None, radius=None):
def display(data, datascalevec=None, radius=None, color=None, shape_type=None):
    '''display(data, radius=1, datascalevec=.5):
    or
    r = random.randn(10,3)
    d = {1:r,2:r+2}
    plotvtk.display(d,color=[[255,0,0],[0,0,255]],radius=[[.004],[.01]])
    or
    radius={'0':.004,'1':.004}
    color={'0':[255,0,0],'1':[0,0,255]}
    plotvtk.display(d,color=color,radius=radius)
    '''
    try:
        if shape(data)[0] == 3 and shape(data)[1] != 3:
            print 'array is probably transposed wrong. transposing'
            data = transpose(data)
    except IndexError: #it probably a dictionary
        pass
        for i in data.keys():
            if len(shape(data[i])) == 1:
                #data 1D array
                pass

            elif shape(data[i])[0] == 3 and shape(data[i])[1] != 3:
                print 'dictionary array is probably transposed wrong. transposing'
                data[i] = transpose(data[i])

    #set some defaults if nothing defined
    defcolor = array([[255,0,0]])#red
    defradius = array([[.004]])

    #Adding feature to handle a single array or a dictionary of arrays
    #so as to handle multiple data.
    if type(data) == dict:
        for d in data.keys():
            numdata = len(data[d])
            if color == None:
                #color = red
                print 'making default color scheme'
                color = array([arange(0,255,255/len(data[d]))[::-1],arange(0,255,255/len(data[d])),arange(0,255,255/len(data[d]))]).T

            if radius == None:
                radius = tile([defradius],len(data[d])).T
    else:
        print 'data in non dict form'
        data = {1:data}
        radius = defradius
        color = defcolor

    [ren,renWin,iren]=vtkwindow()
    for k in range(0,len(data.keys())):
        print shape(data[data.keys()[k]])#, len(data[k]), shape(color)

        if k == -1:
            [sdata, scalefactor]=scaledata(float_(data[data.keys()[k]]))
        else:
            sdata = float_(data[data.keys()[k]])

        points = vtk.vtkPoints()
        math = vtk.vtkMath()
        #some 2 pnts of fake data at 0,0,0
        pointsfake = vtk.vtkPoints()
        pointsfake.InsertNextPoint(0,0,0);
        pointsfake.InsertNextPoint(0,0,0);
        pointsfake.InsertNextPoint(0,0,0);
        ballActor,profile = vtkpoints(pointsfake, color=[0,255,0], radius=.0000)#radius[k])
        ren.AddActor(ballActor) # Add the actors to the renderer, set the background and size
        #end of fake data

        print 'lengthofdata',len(sdata)
        if len(shape(sdata)) == 1: #add dimension
            sdata = array([sdata])
        if len(sdata) < 3: #tile to fix some bug where no points plotted unless = or greater than 3 points
            sdata = tile(sdata,[3 - len(sdata) + 1,1])
        print 'len',len(sdata)
        for i in range(len(sdata)):
            points.InsertNextPoint( sdata[i,0],sdata[i,1], sdata[i,2]);

        #make color and radius dictonaries.
        if type(color) == list and type(radius) == list:
            c = {}; r = {};
            for cr in range(0,len(color)):
                c[cr] = color[cr]
            for cr in range(len(radius)):
                r[cr] = radius[cr]
            color = c;
            radius = r

        print k
        #print shape_type.keys()[k]#shape_type[shape_type.keys()[k]]
        try:
            if shape_type.keys()[k] == 'points':
                ballActor, profile = vtkpoints(points, color=color[color.keys()[k]], radius=radius[radius.keys()[k]])
                ren.AddActor(ballActor) # Add the actors to the renderer, set the background and size
            if shape_type.keys()[k] == 'disks':
                print 'trying disk plot'
                disk_pos = data[data.keys()[k]]
                disk_dir = shape_type[shape_type.keys()[k]]
                for i in range(0,size(disk_pos,0)):
                    d = disk_dir[i]*90
                    diskactor = vtkdisk(c=(0,0,0))
                    diskactor.RotateX(90)
                    diskactor.SetPosition(disk_pos[i][0],disk_pos[i][1],disk_pos[i][2])
                    diskactor.RotateZ(d[0])
                    diskactor.RotateX(d[1]) 
                    ren.AddActor(diskactor)
                print 'done disk'
                
        except AttributeError:
            pass
            ballActor, profile = vtkpoints(points, color=color[color.keys()[k]], radius=radius[radius.keys()[k]])
            ren.AddActor(ballActor) # Add the actors to the renderer, set the background and size
    


    iren.Initialize()
    renWin.Render()
    iren.Start()
    
if __name__ == '__main__':
    from pdf2py import pdf
    p = pdf.read('/home/danc/programming/python/data/0611/0611piez/e,rfhp1.0Hz,ra,f50lp,o')
    p.data.setchannels('meg')
    p.data.channels.getchannellocations()
    points = p.data.channels.chlpos
    dirs = p.data.channels.chudir
    d = {'data':points}#,'color':[255,0,0],'radius':[.01,.01,.01]}
    display(d, color={'color':[255,0,0]}, radius={'radius':.01},shape_type={'disks':dirs})
    quit
    #renWin.Render()
    #iren.Start()
