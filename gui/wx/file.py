'''simple fileopen dialog'''
'''x = fileopen.open()'''
from wxPython.wx import wxPySimpleApp, wxFileDialog, wxMULTIPLE, wxID_OK, wxSAVE
import os

def open():
    application = wxPySimpleApp()
    dialog = wxFileDialog(None, "Select a file(s)", os.getcwd(), "*", "*", wxMULTIPLE)
    l = []
    if dialog.ShowModal() == wxID_OK:
        dialog.Destroy()
        for i in range(0, len(dialog.GetPaths())):
            l.append(str(dialog.GetPaths()[i]))
        print 'Selected:', l
        return l
    else:
       print 'Nothing was selected.'
    dialog.Destroy()
    
    
def save(text=None, suffix='*', filter='*'):
    application = wxPySimpleApp()
    if text == None: text = "Select a save file name"
    dialog = wxFileDialog(None, text, os.getcwd(), suffix, filter, wxSAVE)
    l = []
    if dialog.ShowModal() == wxID_OK:
        for i in range(0, len(dialog.GetPaths())):
            l.append(str(dialog.GetPaths()[i]))
        print 'Selected:', l
        return l[0]
    else:
       print 'Nothing was choosen'
    dialog.Destroy()

