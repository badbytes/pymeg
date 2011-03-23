#!/usr/bin/python

# dragdrop.py

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

        splitter1 = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        self.dir = wx.GenericDirCtrl(splitter1, -1, dir='/home/', style=wx.DIRCTRL_DIR_ONLY)
        self.lc1 = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        self.lc2 = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)

        dt = MyTextDropTarget(self.lc2)
        self.lc2.SetDropTarget(dt)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDragInit, id=self.lc1.GetId())

        tree = self.dir.GetTreeCtrl()

        splitter2.SplitHorizontally(self.lc1, self.lc2)
        splitter1.SplitVertically(self.dir, splitter2)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, id=tree.GetId())

        self.OnSelect(0)
        self.Centre()
        self.Show(True)
        

    def OnSelect(self, event):
        list = os.listdir(self.dir.GetPath())
        self.lc1.ClearAll()
        self.lc2.ClearAll()
        for i in range(len(list)):
            if list[i][0] != '.':
                self.lc1.InsertStringItem(0, list[i])

    def OnDragInit(self, event):
        text = self.lc1.GetItemText(event.GetIndex())
        tdo = wx.TextDataObject(text)
        tds = wx.DropSource(self.lc1)
        tds.SetData(tdo)
        tds.DoDragDrop(True)
        


app = wx.App()
DragDrop(None, -1, 'dragdrop.py')
app.MainLoop()

