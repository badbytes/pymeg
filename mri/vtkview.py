#!/usr/bin/env python
# Copyright 2008 Dan Collins
#
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# And is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Build; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import vtk
import Tkinter
import sys
from scipy import signal
from numpy import arange,sqrt,reshape,transpose

from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor
switchdata = 'v1'


def vtkrender(d1=None, d2=None):
    
    x = (arange(50.0)-25)/2.0
    y = (arange(50.0)-25)/2.0
    r = sqrt(x[:]**2+y**2)
    z = 5.0*signal.special.j0(r)  # Bessel function of order 0
    z1 = reshape(transpose(z), (-1,))
    point_data = vtk.vtkPointData(vtk.vtkScalars(z1))
    grid = vtk.vtkStructuredPoints((50,50, 1), (-12.5, -12.5, 0), (0.5, 0.5, 1))
    data = vtk.VtkData(grid, point_data)
    data.tofile('/tmp/test.vtk')
    d1 = d2 = '/tmp/test.vtk'
    
    #v2,v1,data1,data2 = inputs()
    if d1 == None:
        d1 = "/home/danc/E0058brain.vtk"
        #d1 = "/home/danc/vtk/data1.vtk"
    if d2 == None:
        d2 = "/home/danc/E0058MEG.vtk"
        #d2='/home/danc/vtk/data2.vtk'
        #d2 = "/home/danc/mrvtk_0003overlay.vtk"


    v1 = vtk.vtkStructuredPointsReader()

    #v1.SetFileName("/home/danc/mrvtk.vtk")
    v1.SetFileName(d1)
    v2 = vtk.vtkStructuredPointsReader()
    #v2.SetFileName("/home/danc/mrvtk_overlay.vtk")
    v2.SetFileName(d2)
    v1.SetLookupTableName('/home/danc/colortable.lut')
    v1.SetReadAllColorScalars
    v1.Update()
    v2.Update()


    global xMax, xMin, yMin, yMax, zMin, zMax, current_widget, slice_number
    xMin, xMax, yMin, yMax, zMin, zMax = v1.GetOutput().GetWholeExtent()

    spacing = v1.GetOutput().GetSpacing()
    sx, sy, sz = spacing

    origin = v1.GetOutput().GetOrigin()
    ox, oy, oz = origin

    # An outline is shown for context.
    outline = vtk.vtkOutlineFilter()
    outline.SetInput(v1.GetOutput())

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInput(outline.GetOutput())

    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(1,1,1)

    # The shared picker enables us to use 3 planes at one time
    # and gets the picking order right
    picker = vtk.vtkCellPicker()
    picker.SetTolerance(0.005)

    # The 3 image plane widgets are used to probe the dataset.
    planeWidgetX = vtk.vtkImagePlaneWidget()
    planeWidgetX.DisplayTextOn()
    planeWidgetX.SetInput(v1.GetOutput())
    planeWidgetX.SetPlaneOrientationToXAxes()
    planeWidgetX.SetSliceIndex(int(round(xMax/2)))
    planeWidgetX.SetPicker(picker)
    planeWidgetX.SetKeyPressActivationValue("x")
    planeWidgetX.GetPlaneProperty().SetDiffuseColor((0,1,1))
    #planeWidgetX.GetPlaneProperty().SetColor(0,1,1)
    #planeWidgetX.GetPlaneProperty().SetSpecularColor(0,1,1)
    #planeWidgetX.GetPlaneProperty().SetAmbientColor(0,1,1)
    planeWidgetX.GetPlaneProperty().SetFrontfaceCulling(10)
    planeWidgetX.GetPlaneProperty().SetRepresentationToWireframe
    #planeWidgetX.GetColorMap()
    #print planeWidgetX.GetColorMap()
    #planeWidgetX.SetHueRange(0.667,0.0)
    #planeWidgetX.SetLookupTable('/home/danc/colortable.lut')

    prop1 = planeWidgetX.GetPlaneProperty()
    prop1.SetDiffuseColor(1, 0, 0)
    prop1.SetColor(1,0,0)
    prop1.SetSpecularColor(0, 1, 1)
    #print planeWidgetX.GetLookupTable()
    g = planeWidgetX.GetLookupTable()
    #print g



##    arrow = vtk.vtkArrowSource()
####    arrow.SetShaftRadius(100)
####    arrow.SetShaftResolution(80)
####    arrow.SetTipRadius(100)
####    arrow.SetTipLength(1000)
####    #arrow.SetTipResolution(80)
##    arrowMapper = vtk.vtkPolyDataMapper()
##    arrowMapper.SetInput(arrow.GetOutput())
##    arrowActor = vtk.vtkActor()
##    arrowActor.SetMapper(arrowMapper)
##    arrowActor.SetPosition(0, 0, 0)
##    arrowActor.GetProperty().SetColor(0, 1, 0)


    planeWidgetY = vtk.vtkImagePlaneWidget()
    planeWidgetY.DisplayTextOn()
    planeWidgetY.SetInput(v1.GetOutput())
    planeWidgetY.SetPlaneOrientationToYAxes()
    planeWidgetY.SetSliceIndex(int(round(yMax/2)))
    planeWidgetY.SetPicker(picker)
    planeWidgetY.SetKeyPressActivationValue("y")
    prop2 = planeWidgetY.GetPlaneProperty()
    prop2.SetColor(1, 1, 0)
    planeWidgetY.SetLookupTable(planeWidgetX.GetLookupTable())
    planeWidgetY.GetPlaneProperty().SetDiffuseColor(0,1,1)


    # for the z-slice, turn off texture interpolation:
    # interpolation is now nearest neighbour, to demonstrate
    # cross-hair cursor snapping to pixel centers
    planeWidgetZ = vtk.vtkImagePlaneWidget()

    planeWidgetZ.SetSliceIndex(100)
    planeWidgetZ.SetSlicePosition(100)
    planeWidgetZ.DisplayTextOn()
    planeWidgetZ.SetInput(v1.GetOutput())
    planeWidgetZ.SetPlaneOrientationToZAxes()
    planeWidgetZ.SetSliceIndex(int(round(yMax/2)))
    planeWidgetZ.SetPicker(picker)
    planeWidgetZ.SetKeyPressActivationValue("z")
    prop3 = planeWidgetZ.GetPlaneProperty()
    prop3.SetColor(0, 0, 1)
    planeWidgetZ.SetLookupTable(planeWidgetX.GetLookupTable())
    planeWidgetZ.GetPlaneProperty().SetDiffuseColor(0,1,1)

    filelist = [v2,v1];
    for i in filelist:


        coloroniso = vtk.vtkStructuredPointsReader()
        coloroniso.SetFileName(i.GetFileName())
        coloroniso.SetScalarsName("colors")
        coloroniso.Update()

        isosurface = vtk.vtkStructuredPointsReader()
        isosurface.SetFileName(i.GetFileName())
        isosurface.SetScalarsName("scalars")
        isosurface.Update()

        iso = vtk.vtkContourFilter()
        iso.SetInput(i.GetOutput())
        #iso.SetInput(isosurface.GetOutput())
        if i == v1:
            iso.SetValue(0, 20)
        else:
            iso.SetValue(0,10)
        #iso.SetNumberOfContours(10)

        probe = vtk.vtkProbeFilter()
        probe.SetInput(iso.GetOutput())
        probe.SetSource(coloroniso.GetOutput())

        cast = vtk.vtkCastToConcrete()
        cast.SetInput(probe.GetOutput())

        normals = vtk.vtkPolyDataNormals()
        #normals.SetMaxRecursionDepth(100)
        normals.SetInput(cast.GetPolyDataOutput())
        normals.SetFeatureAngle(45)

    ##    clut = vtk.vtkLookupTable()
    ##    clut.SetHueRange(0, .67)
    ##    clut.Build()
    ##    clut.SetValueRange(coloroniso.GetOutput().GetScalarRange())


    ##    normals = vtk.vtkPolyDataNormals()
    ##    normals.SetInput(iso.GetOutput())
    ##    normals.SetFeatureAngle(45)
        isoMapper = vtk.vtkPolyDataMapper()
        isoMapper.SetInput(normals.GetOutput())
        isoMapper.ScalarVisibilityOn()
        #isoMapper.SetColorModeToMapScalars()
        isoMapper.ColorByArrayComponent(0, 100)#("VelocityMagnitude", 0)

        isoMapper.SetScalarRange([1, 200])
    ##    isoMapper.SetLookupTable(clut)

        isoActor = vtk.vtkActor()
        isoActor.SetMapper(isoMapper)

    ##    isoActor.GetProperty().SetDiffuseColor([.5,.5,.5])
    ##    isoActor.GetProperty().SetSpecularColor([1,1,1])
    ##    isoActor.GetProperty().SetDiffuse(.5)
    ##    isoActor.GetProperty().SetSpecular(.5)
    ##    isoActor.GetProperty().SetSpecularPower(15)
    ##    isoActor.GetProperty().SetOpacity(.6)

        isoActor.GetProperty().SetDiffuseColor(1, .2, .2)
        isoActor.GetProperty().SetSpecular(.7)
        isoActor.GetProperty().SetSpecularPower(20)
        isoActor.GetProperty().SetOpacity(0.5)


        if i == v1:
            print 'under'
            isoActorUnderlay = isoActor
        else:
            print 'over'
            isoActorOverlay = isoActor




    # Create the RenderWindow and Renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # Add the outline actor to the renderer, set the background color and size
    ren.AddActor(outlineActor)
    #ren.AddActor(sphereActor)


    renWin.SetSize(700, 700)
    ren.SetBackground(0, 0, 0)

    current_widget = planeWidgetZ
    mode_widget = planeWidgetZ

    # Create the GUI
    # We first create the supporting functions (callbacks) for the GUI
    #
    # Align the camera so that it faces the desired widget
    def AlignCamera():
        #global ox, oy, oz, sx, sy, sz, xMax, xMin, yMax, yMin, zMax, \
        #      zMin, slice_number
        #global current_widget
        cx = ox+(0.5*(xMax-xMin))*sx
        cy = oy+(0.5*(yMax-yMin))*sy
        cz = oy+(0.5*(zMax-zMin))*sz
        vx, vy, vz = 0, 0, 0
        nx, ny, nz = 0, 0, 0
        iaxis = current_widget.GetPlaneOrientation()
        if iaxis == 0:
            vz = -1
            nx = ox + xMax*sx
            cx = ox + slice_number*sx
        elif iaxis == 1:
            vz = -1
            ny = oy+yMax*sy
            cy = oy+slice_number*sy
        else:
            vy = 1
            nz = oz+zMax*sz
            cz = oz+slice_number*sz

        px = cx+nx*2
        py = cy+ny*2
        pz = cz+nz*3

        camera = ren.GetActiveCamera()
        camera.SetViewUp(vx, vy, vz)
        camera.SetFocalPoint(cx, cy, cz)
        camera.SetPosition(px, py, pz)
        camera.OrthogonalizeViewUp()
        ren.ResetCameraClippingRange()
        renWin.Render()

    # Capture the display and place in a tiff
    def CaptureImage():
        w2i = vtk.vtkWindowToImageFilter()
        writer = vtk.vtkTIFFWriter()
        w2i.SetInput(renWin)
        w2i.Update()
        writer.SetInput(w2i.GetOutput())
        writer.SetFileName("/home/danc/image.tif")
        renWin.Render()
        writer.Write()


    # Align the widget back into orthonormal position,
    # set the slider to reflect the widget's position,
    # call AlignCamera to set the camera facing the widget
    def AlignXaxis():
        global xMax, xMin, current_widget, slice_number
        po = planeWidgetX.GetPlaneOrientation()
        if po == 3:
            planeWidgetX.SetPlaneOrientationToXAxes()
            slice_number = (xMax-xMin)/2
            planeWidgetX.SetSliceIndex(slice_number)
        else:
            slice_number = planeWidgetX.GetSliceIndex()

        current_widget = planeWidgetX

        slice.config(from_=xMin, to=xMax)
        slice.set(slice_number)
        AlignCamera()


    def AlignYaxis():
        global yMin, yMax, current_widget, slice_number
        po = planeWidgetY.GetPlaneOrientation()
        if po == 3:
            planeWidgetY.SetPlaneOrientationToYAxes()
            slice_number = (yMax-yMin)/2
            planeWidgetY.SetSliceIndex(slice_number)
        else:
            slice_number = planeWidgetY.GetSliceIndex()

        current_widget = planeWidgetY

        slice.config(from_=yMin, to=yMax)
        slice.set(slice_number)
        AlignCamera()

    def AlignZaxis():
        global yMin, yMax, current_widget, slice_number
        po = planeWidgetZ.GetPlaneOrientation()
        if po == 3:
            planeWidgetZ.SetPlaneOrientationToZAxes()
            slice_number = (zMax-zMin)/2
            planeWidgetZ.SetSliceIndex(slice_number)
        else:
            slice_number = planeWidgetZ.GetSliceIndex()

        current_widget = planeWidgetZ

        slice.config(from_=zMin, to=zMax)
        slice.set(slice_number)
        AlignCamera()

    ##################def flag(sw):


    def underlay():
        print 'under'
        global overunderstatus
        overunderstatus = 'under'
        isoActor = isoActorUnderlay
        u_button.config(relief='sunken')
        o_button.config(relief='raised')
        six=planeWidgetX.GetSliceIndex()
        siy=planeWidgetY.GetSliceIndex()
        siz=planeWidgetZ.GetSliceIndex()
        data = v1
        planeWidgetX.SetInput(data.GetOutput())
        planeWidgetY.SetInput(data.GetOutput())
        planeWidgetZ.SetInput(data.GetOutput())
        planeWidgetX.SetSliceIndex(six)
        planeWidgetY.SetSliceIndex(siy)
        planeWidgetZ.SetSliceIndex(siz)
        renWin.Render()


    def overlay():
        print 'over'
        global overunderstatus
        overunderstatus = 'over'
        isoActor = isoActorOverlay
        o_button.config(relief='sunken')
        u_button.config(relief='raised')
        six=planeWidgetX.GetSliceIndex()
        siy=planeWidgetY.GetSliceIndex()
        siz=planeWidgetZ.GetSliceIndex()
        data = v2
        planeWidgetX.SetInput(data.GetOutput())
        planeWidgetY.SetInput(data.GetOutput())
        planeWidgetZ.SetInput(data.GetOutput())
        planeWidgetX.SetSliceIndex(six)
        planeWidgetY.SetSliceIndex(siy)
        planeWidgetZ.SetSliceIndex(siz)
        renWin.Render()


    def render3d():
        print '3d rend'
        global buttonpos
        try:
            if overunderstatus == 'under':
                isoActor = isoActorUnderlay
            else:
                isoActor = isoActorOverlay
        except NameError:
            isoActor = isoActorUnderlay
        try:
            buttonpos
            print buttonpos
        except NameError:
            buttonpos = 0
            print buttonpos
            r_button.config(relief='sunken')
            ren.AddActor(isoActor)

            renWin.Render()
        else:
            if buttonpos == 0:
                buttonpos = 1
                r_button.config(relief='raised')
                ren.RemoveActor(isoActor)
                ren.RemoveActor(isoActorUnderlay)
                ren.RemoveActor(isoActorOverlay)
                renWin.Render()
            else:
                buttonpos = 0
                r_button.config(relief='sunken')
                print o_button
                ren.AddActor(isoActor)
                renWin.Render()
        return buttonpos

    # Set the widget's reslice interpolation mode
    # to the corresponding popup menu choice
    def SetInterpolation():
        global mode_widget, mode
        if mode.get() == 0:
            mode_widget.TextureInterpolateOff()
        else:
            mode_widget.TextureInterpolateOn()

        mode_widget.SetResliceInterpolate(mode.get())
        renWin.Render()

    # Share the popup menu among buttons, keeping track of associated
    # widget's interpolation mode
    def buttonEvent(event, arg=None):
        global mode, mode_widget, popm
        if arg == 0:
            mode_widget = planeWidgetX
        elif arg == 1:
            mode_widget = planeWidgetY
        elif arg == 2:
            mode_widget = planeWidgetZ
        else:
            return
        mode.set(mode_widget.GetResliceInterpolate())
        popm.entryconfigure(arg, variable=mode)
        popm.post(event.x + event.x_root, event.y + event.y_root)

    def SetSlice(sl):
        global current_widget
        current_widget.SetSliceIndex(int(sl))
        ren.ResetCameraClippingRange()
        renWin.Render()


    ###
    # Now actually create the GUI
    root = Tkinter.Tk()
    root.withdraw()
    top = Tkinter.Toplevel(root)

    # Define a quit method that exits cleanly.
    def quit(obj=root):
        print obj
        obj.quit()
        obj.destroy()
        #vtkrender.destroy()


    # Popup menu
    popm = Tkinter.Menu(top, tearoff=0)
    mode = Tkinter.IntVar()
    mode.set(1)
    popm.add_radiobutton(label="nearest", variable=mode, value=0,
                         command=SetInterpolation)
    popm.add_radiobutton(label="linear", variable=mode, value=1,
                         command=SetInterpolation)
    popm.add_radiobutton(label="cubic", variable=mode, value=2,
                         command=SetInterpolation)

    display_frame = Tkinter.Frame(top)
    display_frame.pack(side="top", anchor="n", fill="both", expand="false")

    # Buttons
    ctrl_buttons = Tkinter.Frame(top)
    ctrl_buttons.pack(side="top", anchor="n", fill="both", expand="false")

    quit_button = Tkinter.Button(ctrl_buttons, text="Quit", command=quit)
    capture_button = Tkinter.Button(ctrl_buttons, text="Tif",
                                    command=CaptureImage)
    quit_button.config(background='#C0C0C0')

    x_button = Tkinter.Button(ctrl_buttons, text="x", command=AlignXaxis)
    y_button = Tkinter.Button(ctrl_buttons, text="y", command=AlignYaxis)
    z_button = Tkinter.Button(ctrl_buttons, text="z", command=AlignZaxis)
    u_button = Tkinter.Button(ctrl_buttons, text="underlay", command=underlay)
    o_button = Tkinter.Button(ctrl_buttons, text="overlay", command=overlay)
    r_button = Tkinter.Button(ctrl_buttons, text="3d render", command=render3d)
    o_button.config(background='#FFFFFF')
    u_button.config(relief='sunken')



    x_button.bind("<Button-3>", lambda e: buttonEvent(e, 0))
    y_button.bind("<Button-3>", lambda e: buttonEvent(e, 1))
    z_button.bind("<Button-3>", lambda e: buttonEvent(e, 2))
    u_button.bind("<Button-3>", lambda e: buttonEvent(e, 3))
    o_button.bind("<Button-3>", lambda e: buttonEvent(e, 4))
    r_button.bind("<Button-3>", lambda e: buttonEvent(e, 5))

    for i in (quit_button, capture_button, x_button, y_button, z_button, u_button, o_button, r_button):
        i.pack(side="left", expand="true", fill="both")


    # Create the render widget
    renderer_frame = Tkinter.Frame(display_frame)
    renderer_frame.pack(padx=3, pady=3,side="left", anchor="n",
                        fill="both", expand="false")

    render_widget = vtkTkRenderWindowInteractor(renderer_frame,
                                                rw=renWin, width=600,
                                                height=600)
    for i in (render_widget, display_frame):
        i.pack(side="top", anchor="n",fill="both", expand="false")

    # Add a slice scale to browse the current slice stack
    slice_number = Tkinter.IntVar()
    slice_number.set(current_widget.GetSliceIndex())
    slice = Tkinter.Scale(top, from_=zMin, to=zMax, orient="horizontal",
                          command=SetSlice,variable=slice_number,
                          label="Slice")
    slice.pack(fill="x", expand="false")

    # Done with the GUI.
    ###

    # Set the interactor for the widgets
    iact = render_widget.GetRenderWindow().GetInteractor()
    planeWidgetX.SetInteractor(iact)
    planeWidgetX.On()
    planeWidgetY.SetInteractor(iact)
    planeWidgetY.On()
    planeWidgetZ.SetInteractor(iact)
    planeWidgetZ.On()

    # Create an initial interesting view
    cam1 = ren.GetActiveCamera()
    cam1.Elevation(210)
    cam1.SetViewUp(1, -1, 1)
    cam1.Azimuth(-145)
    ren.ResetCameraClippingRange()

    # Render it
    render_widget.Render()

    iact.Initialize()
    renWin.Render()
    iact.Start()

    # Start Tkinter event loop
    root.mainloop()

def show(data1=None, data2=None):
    vtkrender()

if __name__ == "__main__":
    show()


