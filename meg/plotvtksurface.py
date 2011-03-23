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




import vtk
from vtk.util.colors import *

'data need to by N x 3'

def vtksetup(points, color=None, radius=None):
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
    
    # Construct the surface and create isosurface.
    #surf = vtk.vtkSurfaceReconstructionFilter()
    #surf.SetInput(pointSource.GetPolyDataOutput())
    cf = vtk.vtkPolyData()
    
    #cf = vtk.vtkContourFilter()
    cf.SetPoints(points)
    #cf.SetInput(surf.GetOutput())
    #cf.SetValue(0, 0.0)
    
##    map = vtk.vtkPolyDataMapper()
##    map.SetInput(reverse.GetOutput())
##    map.ScalarVisibilityOff()

    surfaceActor = vtk.vtkActor()
    surfaceActor.SetMapper(map)
    surfaceActor.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)
    surfaceActor.GetProperty().SetSpecularColor(1, 1, 1)
    surfaceActor.GetProperty().SetSpecular(.4)
    surfaceActor.GetProperty().SetSpecularPower(50)

    # We will now create a nice looking mesh by wrapping the edges in tubes,
    # and putting fat spheres at the points.
    extract = vtk.vtkExtractEdges()
    extract.SetInputConnection(delny.GetOutputPort())

    ball = vtk.vtkSphereSource()
    
    if radius == None:
        rad = .002
    else:
        rad = radius
    
    ball.SetRadius(rad)
    ball.SetThetaResolution(5)
    ball.SetPhiResolution(5)
    balls = vtk.vtkGlyph3D()
    balls.SetInputConnection(delny.GetOutputPort())
    balls.SetSourceConnection(ball.GetOutputPort())
    mapBalls = vtk.vtkPolyDataMapper()
    mapBalls.SetInputConnection(balls.GetOutputPort())
    ballActor = vtk.vtkActor()
    ballActor.SetMapper(mapBalls)
    if color == None:
        ballcolor = red
    else:
        ballcolor = color
    ballActor.GetProperty().SetColor(ballcolor)
    ballActor.GetProperty().SetSpecularColor(0, 0, 0)
    ballActor.GetProperty().SetSpecular(0.3)
    ballActor.GetProperty().SetSpecularPower(100)
    ballActor.GetProperty().SetAmbient(0.2)
    ballActor.GetProperty().SetDiffuse(0.8)
    return ballActor

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
    #ren.AddActor(edgeActor)

    

def scaledata(data):
    scalefactor=(1/((data.max()-data.min())/2))*.1 #scale data to 1.0 -1.0
    data=data*scalefactor
    return data, scalefactor

def display(data, data2=None, data3=None):
    # Generate some random points

    math = vtk.vtkMath()
    points = vtk.vtkPoints()
    
    [data, scalefactor]=scaledata(data)
    for i in range(len(data)):
        points.InsertNextPoint( data[i,0],data[i,1], data[i,2]);
    ballActor = vtksetup(points, color=red, radius=.001)
    [ren,renWin,iren]=vtkwindow()
    ren.AddActor(ballActor) # Add the actors to the renderer, set the background and size
    
    if data2 != None:
        data=data2*scalefactor
        points = vtk.vtkPoints()
        for i in range(len(data)):
            points.InsertNextPoint( data[i,0],data[i,1], data[i,2]);
        ballActor = vtksetup(points, color=blue)
        ren.AddActor(ballActor)
    
    if data3 != None:
        data=data3*scalefactor
        points = vtk.vtkPoints()
        for i in range(len(data)):
            points.InsertNextPoint( data[i,0],data[i,1], data[i,2]);
        ballActor = vtksetup(points, color=green, radius=.007)
        ren.AddActor(ballActor)



    # Interact with the data.
    iren.Initialize()
    renWin.Render()
    iren.Start()