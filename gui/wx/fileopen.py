'''simple fileopen dialog'''
'''x = fileopen.open()'''
from wxPython.wx import wxPySimpleApp, wxFileDialog, wxMULTIPLE, wxID_OK
import os

def open():
    
    application = wxPySimpleApp()
    #dialog = wxFileDialog ( None, style = wxOPEN )
    dialog = wxFileDialog(None, "Select a file(s)", os.getcwd(), "*", "*", wxMULTIPLE)
    l = []
    if dialog.ShowModal() == wxID_OK:
        #print 'Selected:', dialog.GetPaths()
        #return eval(str(dialog.GetPaths()))
        for i in range(0, len(dialog.GetPaths())):
            l.append(str(dialog.GetPaths()[i]))
        print 'Selected:', l
        return l

    # The user did not select anything

    else:
       print 'Nothing was selected.'

    # Destroy the dialog

    dialog.Destroy()


