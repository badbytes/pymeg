import pygtk
pygtk.require('2.0')
import gtk
import vtk
from markers import Marker
from pbrainlib.gtkutils import ProgressBarDialog
class Viewer:
        
    def update_viewer(self, event, *args):
        raise NotImplementedError


class UndoRegistry:
    __sharedState = {}
    commands = []
    lastPop = None, []

    def __init__(self):
        self.__dict__ = self.__sharedState    

    def push_command(self, func, *args):
        self.commands.append((func, args))

    def undo(self):
        if len(self.commands)==0: return
        func, args = self.commands.pop()
        self.lastPop = func, args
        func(*args)

        
    def flush(self):
        self.commands = []

    def get_last_pop(self):
        return self.lastPop

class EventHandler:
    __sharedState = {}
    markers = vtk.vtkActorCollection()
    defaultColor = (0,0,1)
    labelsOn = 1
    observers = {}
    selected = {}

    def __init__(self):
        self.__dict__ = self.__sharedState            

    def add_selection(self, marker):
        self.selected[marker] = 1
        self.notify('select marker', marker)
        
    def remove_selection(self, marker):
        if self.selected.has_key(marker):
            del self.selected[marker]
            self.notify('unselect marker', marker)
        
        
    def select_new(self, marker):
        for oldMarker in self.selected.keys():
            self.remove_selection(oldMarker)
        self.add_selection(marker)
    
    def add_marker(self, marker):
        # break undo cycle 
        func, args = UndoRegistry().get_last_pop()
        #print 'add', func, args
        if len(args)==0 or \
               (func, args[0]) != (self.add_marker, marker):
            UndoRegistry().push_command(self.remove_marker, marker)
        self.markers.AddItem(marker)
        self.notify('add marker', marker) # fixme


    def remove_marker(self, marker):
        # break undo cycle

        func, args = UndoRegistry().get_last_pop()
        #print 'remove', func, args
        if len(args)==0 or \
               (func, args[0]) != (self.remove_marker, marker):
            UndoRegistry().push_command(self.add_marker, marker)
        self.markers.RemoveItem(marker)
        self.notify('remove marker', marker)

    def get_markers(self):
        return self.markers

    def get_markers_as_seq(self):
        numMarkers = self.markers.GetNumberOfItems()
        self.markers.InitTraversal()
        return [self.markers.GetNextActor() for i in range(numMarkers)]


    def set_default_color(self, color):
        self.defaultColor = color

    def get_default_color(self):
        return self.defaultColor


    def save_markers_as(self, fname):
        fh = file(fname, 'w')
        self.markers.InitTraversal()
        numMarkers = self.markers.GetNumberOfItems()
        lines = []
        for i in range(numMarkers):
            marker = self.markers.GetNextActor()
            if marker is None: continue
            lines.append(marker.to_string())
        lines.sort()
        fh.write('\n'.join(lines) + '\n')
        
    def load_markers_from(self, fname):
        prog = ProgressBarDialog(
            title='Loading markers',
            parent=None,
            msg='Please hold on...',
            size=(300,40),
            )
        prog.show()
        

        self.notify('render off')
        lines = file(fname, 'r').readlines()
        for i,line in enumerate(lines):
            marker = Marker.from_string(line)
            self.add_marker(marker)
            prog.bar.set_fraction(float(i)/len(lines))
            while gtk.events_pending(): gtk.mainiteration()
        self.notify('render on')
        UndoRegistry().flush()
        prog.destroy()

    def attach(self, observer):
        self.observers[observer] = 1

    def detach(self, observer):
        try:
            del self.observers[observer]
        except KeyError: pass

    def notify(self, event, *args):
        for observer in self.observers.keys():
            observer.update_viewer(event, *args)

    def get_labels_on(self):
        return self.labelsOn

    def set_labels_on(self):
        self.labelsOn = 1
        self.notify('labels on')

    def set_labels_off(self):
        self.labelsOn = 0
        self.notify('labels off')


    def is_selected(self, marker):
        return self.selected.has_key(marker)

    def get_selected(self):
        return self.selected.keys()

    def get_num_selected(self):
        return len(self.selected)
