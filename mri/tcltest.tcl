# f(x,y,z) plotter
#  by Mark Dewing
#  version 0.1


import vtk
from math import *
from Tkinter import *
import vtk.tk.vtkTkRenderWindowInteractor

root= Tk()
display_frame = Frame(root)
render_frame = Frame(display_frame)
tools_frame = Frame(display_frame)

# left window - 3d view
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0.0, 0.0, 0.5, 1.0)

# right window - 2d cut plane
ren2 = vtk.vtkRenderer()
ren2.SetViewport(0.5, 0.0, 1.0, 1.0)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)

render_widget = vtk.tk.vtkTkRenderWindowInteractor.\
vtkTkRenderWindowInteractor(render_frame,rw=renWin,width=600,height=300)



# this generates points for the 3d function
pointSource = vtk.vtkProgrammableSource()
  
class plot_3d:
   npoints = 10
   scale = .05
   def readPoints(self):
      npts = self.npoints
      scale = self.scale
      spoint = pointSource.GetStructuredPointsOutput()
      spoint.SetExtent(0,npts-1,0,npts-1,0,npts-1)
      spoint.SetWholeExtent(0,npts-1,0,npts-1,0,npts-1)
      spoint.SetUpdateExtent(0,npts-1,0,npts-1,0,npts-1)
      spoint.SetNumberOfScalarComponents(1)
      derivs = vtk.vtkFloatArray()
      spoint.SetSpacing(2*scale,2*scale,2*scale)
      for i in range(0,npts):
         x = (i-npts/2)*scale
         for j in range(0,npts):
            y = (j-npts/2)*scale
            for k in range(0,npts):
               z = (k-npts/2)*scale
               val = self.plot_func(x,y,z)
               spoint.SetScalarComponentFromFloat(i,j,k,0,val)
               derivs.InsertNextValue(val)
     
      spoint.GetPointData().SetScalars(derivs)
      spoint.UpdateData()
   def eval_func(self):
      self.plot_func = eval("lambda x,y,z : " + self.func)

func = "sqrt(x*x + y*y + z*z)*cos(x)" 
#hook up the actual point generating function and the initial function
plt = plot_3d()
plt.func = func
plt.eval_func()
pointSource.SetExecuteMethod(plt.readPoints)
pointSource.UpdateInformation()

# generate isosurface contours and feed those to the left window

cf= vtk.vtkContourFilter()
cf.SetInput(pointSource.GetStructuredPointsOutput())
cf.GenerateValues(10,0.0,0.5)


(cx,cy,cz) = pointSource.GetStructuredPointsOutput().GetCenter()
#print cx,cy,cz
pointSource.GetStructuredPointsOutput().SetOrigin(-cx,-cy,-cz)

# cut plane in the left window

cut_plane = vtk.vtkPlane()
cut_plane.SetNormal(0,0,1)
cut_plane.SetOrigin(0,0,0)

cutter = vtk.vtkCutter()
cutter.SetInput(pointSource.GetStructuredPointsOutput())
cutter.SetCutFunction(cut_plane)
cutter.GenerateValues(1,0.0,0.0)


# the VTK data flow is data source -> mapper -> actor -> renderer

iso_mapper = vtk.vtkPolyDataMapper()
iso_mapper.SetInput(cf.GetOutput())

isoActor = vtk.vtkActor()
isoActor.SetMapper(iso_mapper)
isoActor.GetProperty().SetOpacity(.3)
isoActor.SetOrigin(cx,cy,cz)

cutterMapper = vtk.vtkPolyDataMapper()
cutterMapper.SetInput(cutter.GetOutput())
cutterMapper.SetScalarRange(0.0,1.0)

cutActor = vtk.vtkActor()
cutActor.SetMapper(cutterMapper)

# generate the view in the right window

warp = vtk.vtkWarpScalar()
warp.SetInput(cutter.GetOutput())
warp.SetScaleFactor(2.0)


plane_mapper = vtk.vtkPolyDataMapper()
plane_mapper.SetInput(warp.GetPolyDataOutput())

# try keep it steady under translations of the source
# haven't figured out yet how to remove the rotations
transform_plane = vtk.vtkTransform()
transform_plane.Translate(-cx/2,-cy/2,-cz/2)

carpetActor = vtk.vtkActor()
carpetActor.SetMapper(plane_mapper)
carpetActor.SetUserTransform(transform_plane)

# add the actors to the windows

ren1.AddActor(isoActor)
ren1.AddActor(cutActor)

ren1.GetActiveCamera().Dolly(.25)

ren2.AddActor(carpetActor)

ren2.GetActiveCamera().Dolly(.25)


prev_x = 0.0
prev_y = 0.0
prev_z = 0.0

myplane = vtk.vtkPlane()

def plane_callback(obj,event):
   global cut_plane,prev_x,prev_y,prev_z
   obj.GetPlane(myplane)
   (ox,oy,oz) = myplane.GetOrigin()
   (px,py,pz) = myplane.GetNormal()
   #cut_plane.SetOrigin(ox-px*cx,oy-py*cy,oz-pz*cz)
   #cut_plane.SetNormal(px,py,pz)
   cut_plane.SetOrigin(ox,oy,oz)
   cut_plane.SetNormal(px,py,pz)
   cutter.GenerateValues(1,0,0)

# this lets us create and interact with the cut plane in the left window

planeWidget = vtk.vtkImplicitPlaneWidget()
planeWidget.SetInteractor(render_widget)
planeWidget.SetInput(pointSource.GetStructuredPointsOutput())
planeWidget.SetPlaceFactor(1.25)
planeWidget.PlaceWidget()
planeWidget.AddObserver("InteractionEvent",plane_callback)
planeWidget.DrawPlaneOff()
planeWidget.SetNormal(0,0,1)
#planeWidget.SetOrigin(-cx,-cy,-cz)



def change_entry():
  func = entry.get()
  plt.func = func
  plt.eval_func()
  pointSource.Modified()
  pointSource.UpdateInformation()
  cf.Modified()
  cutter.Modified()
  render_widget.Render()

label = Label(tools_frame,text='Function f(x,y,z) = ')
label.pack(side=LEFT)


def toggle_cutplane():
     planeWidget.SetCurrentRenderer(ren1)
     if (planeWidget.GetEnabled()):
        planeWidget.EnabledOff()
     else:
        planeWidget.EnabledOn()

show_cutplane_button = Button(tools_frame,text='Manipulate cut plane',command=toggle_cutplane)
show_cutplane_button.pack(side=RIGHT)

update_button = Button(tools_frame,text='Update',command=change_entry)
update_button.pack(side=RIGHT)
tools_frame.pack(side=TOP)

entry = Entry(tools_frame)
entry.pack(side=LEFT)
entry.insert(0,func)



display_frame.pack(expand=YES,fill=BOTH)
render_widget.pack(expand=YES,fill=BOTH)
render_frame.pack(expand=YES,fill=BOTH)
root.mainloop()
