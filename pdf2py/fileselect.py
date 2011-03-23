#!/usr/bin/env python

import sys
import getopt
import gtk

class FileChooser(gtk.FileSelection):
    def __init__(self, modal=gtk.TRUE, multiple=gtk.TRUE):
        gtk.FileSelection.__init__(self)
        self.multiple = multiple
        self.connect("destroy", self.quit)
        self.connect("delete_event", self.quit)
        if modal:
            self.set_modal(gtk.TRUE)
        self.cancel_button.connect('clicked', self.quit)
        self.ok_button.connect('clicked', self.ok_cb)
        if multiple:
            self.set_select_multiple(gtk.TRUE)
##         self.hide_fileop_buttons()
        self.ret = None
    def quit(self, *args):
        self.hide()
        self.destroy()
        gtk.main_quit()
        #gtk.mainquit()
    def ok_cb(self, b):
        if self.multiple:
            self.ret = self.get_selections()
        else:
            self.ret = self.get_filename()
        self.quit()

def file_sel_box(title="Browse", modal=gtk.FALSE, multiple=gtk.TRUE):
    win = FileChooser(modal=modal, multiple=multiple)
    win.set_title(title)
    win.show()
    gtk.main()#gtk.mainloop()
    return win.ret

def file_open_box(modal=gtk.TRUE):
    return file_sel_box("Open", modal=modal, multiple=gtk.TRUE)
def file_save_box(modal=gtk.TRUE):
    return file_sel_box("Save As", modal=modal, multiple=gtk.FALSE)

def test():
    result = file_open_box()
    print 'open result:', result
    result = file_save_box()
    print 'save result:', result

USAGE_TEXT = """
Usage:
    python simple_dialog.py [options]
Options:
    -h, --help      Display this help message.
Example:
    python simple_dialog.py
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)

def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'h', ['help'])
    except:
        usage()
    relink = 1
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
    if len(args) != 0:
        usage()
    test()

if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')
