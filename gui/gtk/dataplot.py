import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk
from numpy import * #fromstring, arange, int16, float, log10
from matplotlib import rcParams

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


class MainWindow(PrefixWrapper):
    prefix = ''
    widgetName = 'windowMain'
    gladeFile = '/home/danc/python/pymeg/pbrain/gui/main.glade'
    
    
class EEGPlot():
    def __init__(self, eeg, canvas):
        
