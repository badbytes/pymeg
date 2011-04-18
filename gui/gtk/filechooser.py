#!/usr/bin/python2
#!/usr/bin/env python

# example filechooser.py

import pygtk
pygtk.require('2.0')

import gtk

def open(path=None):
    # Check for new pygtk: this is new class in PyGtk 2.4
    if gtk.pygtk_version < (2,3,90):
       print "PyGtk 2.3.90 or later required for this example"
       raise SystemExit

    dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_select_multiple(True)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name("Images")
    filter.add_mime_type("image/png")
    filter.add_mime_type("image/jpeg")
    filter.add_mime_type("image/gif")
    filter.add_pattern("*.png")
    filter.add_pattern("*.jpg")
    filter.add_pattern("*.gif")
    filter.add_pattern("*.tif")
    filter.add_pattern("*.xpm")
    dialog.add_filter(filter)

    if path != None:
        dialog.set_current_folder(path)

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        print dialog.get_filenames(), 'selected'
        fn = dialog.get_filenames()
        dialog.destroy()
        return fn
    elif response == gtk.RESPONSE_CANCEL:
        print 'Closed, no files selected'
        dialog.destroy()
