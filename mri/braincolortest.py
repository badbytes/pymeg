import vtk

v2 = vtk.vtkStructuredPointsReader()
v2.SetFileName("/home/danc/mri_overlay.vtk")

coloroniso = vtk.vtkStructuredPointsReader()
coloroniso.SetFileName(v2.GetFileName())
coloroniso.SetScalarsName("colors")
coloroniso.Update()

isosurface = vtk.vtkStructuredPointsReader()
isosurface.SetFileName(v2.GetFileName())
isosurface.SetScalarsName("scalars")
isosurface.Update()

iso = vtk.vtkContourFilter()
#iso.SetInput(v2.GetOutput())
iso.SetInput(isosurface.GetOutput())
#iso.SetValue(0, .550)
#iso.SetNumberOfContours(13)
#iso.SetValue(0, 128)



probe = vtk.vtkProbeFilter()
probe.SetInput(iso.GetOutput())
probe.SetSource(coloroniso.GetOutput())

cast = vtk.vtkCastToConcrete()
cast.SetInput(probe.GetOutput())

normals = vtk.vtkPolyDataNormals()
#normals.SetMaxRecursionDepth(100)
normals.SetInput(cast.GetPolyDataOutput())
normals.SetFeatureAngle(45)

clut = vtk.vtkLookupTable()
clut.SetHueRange(0, .67)
clut.Build()
clut.SetValueRange(coloroniso.GetOutput().GetScalarRange())

##    normals = vtk.vtkPolyDataNormals()
##    normals.SetInput(iso.GetOutput())
##    normals.SetFeatureAngle(45)
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInput(normals.GetOutput())
isoMapper.ScalarVisibilityOn()
#isoMapper.SetColorModeToMapScalars()

isoMapper.SetScalarRange([0, .1])
isoMapper.SetLookupTable(clut)

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)


ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

ren.AddActor(isoActor)

renWin.Render()