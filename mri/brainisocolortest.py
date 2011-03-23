#!/usr/bin/env python

# This example shows how to color an isosurface with other
# data. Basically an isosurface is generated, and a data array is
# selected and used by the mapper to color the surface.

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Read some data. The important thing here is to read a function as a
# data array as well as the scalar and vector.  (here function 153 is
# named "Velocity Magnitude").Later this data array will be used to
# color the isosurface.

pl3d = vtk.vtkStructuredPointsReader()
#pl3d = vtk.vtkPLOT3DReader()

#pl3d.SetXYZFileName(VTK_DATA_ROOT + "/Data/combxyz.bin")
#pl3d.SetQFileName(VTK_DATA_ROOT + "/Data/combq.bin")
pl3d.SetFileName("/home/danc/mri_overlay.vtk")
#pl3d.SetQFileName("/home/danc/mri_overlay.vtk")

#pl3d.SetScalarFunctionNumber(100)
#pl3d.SetVectorFunctionNumber(202)
#pl3d.SetVectorsName("/home/danc/mri_overlay.vtk")
#pl3d.SetScalarsName("/home/danc/mri_overlay.vtk")

#pl3d.AddFunction(153)
pl3d.Update()
pl3d.DebugOn()
    
# The contour filter uses the labeled scalar (function number 100
# above to generate the contour surface; all other data is
# interpolated during the contouring process.
iso = vtk.vtkContourFilter()
iso.SetInput(pl3d.GetOutput())
iso.SetValue(0, .24)

normals = vtk.vtkPolyDataNormals()
normals.SetInput(iso.GetOutput())
normals.SetFeatureAngle(45)

# We indicate to the mapper to use the velcoity magnitude, which is a
# vtkDataArray that makes up part of the point attribute data.
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInput(normals.GetOutput())
isoMapper.ScalarVisibilityOn()
isoMapper.SetScalarRange(0, 1500)
isoMapper.SetScalarModeToUsePointFieldData()
isoMapper.ColorByArrayComponent("VelocityMagnitude", 0)

isoActor = vtk.vtkLODActor()
isoActor.SetMapper(isoMapper)
isoActor.SetNumberOfCloudPoints(1000)


# Create the usual rendering stuff.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindow
wInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(isoActor)
ren.SetBackground(1, 1, 1)
renWin.SetSize(500, 500)
ren.SetBackground(0.1, 0.2, 0.4)


iren.Initialize()
renWin.Render()
iren.Start()
