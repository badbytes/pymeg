import wx
import time

def start(value):
    max = value
    app = wx.PySimpleApp()
    dlg = wx.ProgressDialog("Progress dialog","test",maximum = max,style = wx.PD_ELAPSED_TIME| wx.PD_ESTIMATED_TIME| wx.PD_REMAINING_TIME)

    keepGoing = True
    skip = False
    count = 0
    
    while keepGoing and count < max:
        count += 1
        newtext = 'test'
        #wx.MilliSleep(1000)
        #time.sleep(1)
        #newtext = "(before) count: %s, index: %s, skip: %s " % \
        (count, keepGoing, skip)
        #print newtext
        (keepGoing, skip) = dlg.Update(count, newtext)
        #newtext = "(after) count: %s, index: %s, skip: %s " % \
        (count, keepGoing, skip)
        #print newtext
    #dlg.Destoy()
    
    
def start2(percentdone):
    max = 100
    app = wx.PySimpleApp()
    dlg = wx.ProgressDialog("Progress dialog","test",maximum = max,style = wx.PD_ELAPSED_TIME| wx.PD_ESTIMATED_TIME| wx.PD_REMAINING_TIME)

    keepGoing = True
    skip = False
    count = 0
    
    while keepGoing and count < max:
        count += 1
        newtext = 'test'
        #wx.MilliSleep(1000)
        #time.sleep(1)
        #newtext = "(before) count: %s, index: %s, skip: %s " % \
        (count, keepGoing, skip)
        #print newtext
        (keepGoing, skip) = dlg.Update(count, newtext)
        #newtext = "(after) count: %s, index: %s, skip: %s " % \
        (count, keepGoing, skip)
        #print newtext
    #dlg.Destoy()
    
    
    

