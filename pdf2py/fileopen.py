'''simple '''

from wxPython.wx import wxPySimpleApp, wxFileDialog
def open():
    application = wxPySimpleApp()
    dialog = wxFileDialog ( None, style = wxOPEN )

    if dialog.ShowModal() == wxID_OK:
        print 'Selected:', dialog.GetPath()
        return str(dialog.GetPath())

    # The user did not select anything

    else:
       print 'Nothing was selected.'

    # Destroy the dialog

dialog.Destroy()




##def fileopen(self):
##    dlg = wx.FileDialog(self, "Select a 4D MEG file", os.getcwd(), "", "*", wx.OPEN)
##    if dlg.ShowModal() == wx.ID_OK:
##        self.megpath = path = dlg.GetPath()
##        dlg.Destroy()
##
##
##
##
##from Tkinter import *
##from tkMessageBox import *
##from tkColorChooser import askcolor              
##from tkFileDialog   import askopenfilename      
##
##def callback():
##    askopenfilename() 
##    
##    
##errmsg = 'Error!'
##Button(text='Quit', command=callback).pack(fill=X)
##Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
##mainloop()
