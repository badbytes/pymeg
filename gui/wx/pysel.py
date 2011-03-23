#!/usr/bin/python

# pysel

import os
import wx

class MyTextDropTarget(wx.TextDropTarget):
    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        self.object.InsertStringItem(0, data)


class DragDrop(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(650, 500))
        
        self.frame_main_menubar = wx.MenuBar()
        wx_menu = wx.Menu()
        wx_menu.Append(12, "dbswitcher", "", wx.ITEM_NORMAL)
        self.frame_main_menubar.Append(wx_menu, "Menu")
        wx_menu = wx.Menu()
        wx_menu.Append(1, "Psel", "", wx.ITEM_NORMAL)
        self.SetMenuBar(self.frame_main_menubar)
        
        self.button_1 = wx.Button(self, -1, "Get Selection")
        self.button_1.SetBackgroundColour(wx.Colour(90, 128, 12))
        self.button_2 = wx.Button(self, -1, "Clear Selections")
        self.button_2.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.statusbar = self.CreateStatusBar()
        
        #~ self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_DOCKABLE|wx.TB_TEXT)
        #~ self.SetToolBar(self.toolbar)
        #~ self.toolbar.AddLabelTool(1, "Get Selections(s)", wx.Bitmap("getsel.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        #~ self.toolbar.AddLabelTool(2, "Clear Selection(s)", wx.Bitmap("clear.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        #~ self.Bind(wx.EVT_TOOL, self.GetSel, id=1)
        #~ self.Bind(wx.EVT_TOOL, self.ClearSel, id=2)

        splitter1 = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(splitter1, wx.EXPAND, wx.EXPAND, 3)
        self.SetSizer(sizer_1)
        sizer_1.Add(self.button_1, 0, 0, 1)
        sizer_1.Add(self.button_2, 0, 0, 1)
        stage = os.environ['STAGE']
        
        self.dir = wx.GenericDirCtrl(splitter1, -1, dir=stage+'/data/', style=wx.DIRCTRL_DIR_ONLY)
        self.lc1 = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        self.lc2 = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        
        self.x = MyDataObject()
        self.fnlist = []
        self.x.SetData(self.fnlist)
        
        dt = MyTextDropTarget(self.lc2)
        self.lc2.SetDropTarget(dt)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDragInit, id=self.lc1.GetId())
        tree = self.dir.GetTreeCtrl()

        splitter2.SplitHorizontally(self.lc1, self.lc2)
        splitter1.SplitVertically(self.dir, splitter2)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, id=tree.GetId())

        self.Bind(wx.EVT_BUTTON, self.GetSel, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.ClearSel, self.button_2)
        
        self.OnSelect(0)
        self.Centre()
        self.Show(True)
        
    def ClearSel(self, event):
        self.lc2.ClearAll()
        self.fnlist = []
        
    def GetSel(self, event):
        #exitfunction()
        globals()["fnlist"] = self.fnlist
        self.Close()
        
    def exitfunction(self):
        self.Destroy()

    def OnSelect(self, event):
        list = os.listdir(self.dir.GetPath())
        #print self.dir.GetPath()
        
        self.lc1.ClearAll()
        #self.lc2.ClearAll()
        for i in range(len(list)):
            if list[i][0] != '.':
                self.lc1.InsertStringItem(0, list[i])
        #return self.dir.GetPath()

    def OnDragInit(self, event):
        text = self.lc1.GetItemText(event.GetIndex())
        tdo = wx.TextDataObject(text)
        tds = wx.DropSource(self.lc1)
        tds.SetData(tdo)
        tds.DoDragDrop(True)
        self.fn = str(self.dir.GetPath()+'/'+text)
        self.fnlist.append(self.fn)
        #print self.fnlist
        
class MyDataObject(wx.PyDataObjectSimple):
    def __init__(self):
        wx.PyDataObjectSimple.__init__(
            self, wx.CustomDataFormat('MyDOFormat'))
        self.data = ''

    def GetDataSize(self):
        return len(self.data)
    def GetDataHere(self):
        return self.data  # returns a string  
    def SetData(self, data):
        self.data = data
        return True

#~ class START(DragDrop):
    #~ def __init__(self):
        #~ app = wx.App()
        #~ DragDrop(None, -1, 'pysel')
        #~ app.MainLoop()
        #~ self.fnlist = userInput
        

def start():
    app = wx.App()
    DragDrop(None, -1, 'pysel')
    app.MainLoop()
    #app.Exit()
    return fnlist
    
    
#~ app = wx.App()
#~ DragDrop(None, -1, 'pysel')
#~ app.MainLoop()
    
