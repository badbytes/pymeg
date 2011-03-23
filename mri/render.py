
import vtk

v2 = vtk.vtkStructuredPointsReader()
v2.SetFileName("/home/danc/mri_overlay.vtk")

iso = vtk.vtkContourFilter()
iso.SetInput(v2.GetOutput())
iso.SetValue(0, .5)
iso.SetNumberOfContours(13)
normals = vtk.vtkPolyDataNormals()
normals.SetInput(iso.GetOutput())
normals.SetFeatureAngle(45)
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInput(normals.GetOutput())
isoMapper.ScalarVisibilityOff()
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetDiffuseColor([1,.5,.5])
isoActor.GetProperty().SetSpecularColor([1,1,1])
isoActor.GetProperty().SetDiffuse(.5)
isoActor.GetProperty().SetSpecular(.5)
isoActor.GetProperty().SetSpecularPower(5)
isoActor.GetProperty().SetOpacity(1)


ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(isoActor)
isoActor.VisibilityOn()
#ren.AddActor(cut)
#cut.GetProperty().SetOpacity(1)
ren.SetBackground(1, 1, 1)
renWin.SetSize(640, 480)

iren.Initialize()
renWin.Render()
iren.Start()