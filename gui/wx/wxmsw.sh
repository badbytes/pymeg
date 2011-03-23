#!/bin/bash
source ~/.bashrc
PYMEGPATH=/home/danc/python/pymeg
cd $PYMEGPATH/gui

#sh -c "cd $PYMEGPATH/gui && ./wxmsw.py"

#xterm -hold -e /usr/bin/env
export PYTHONPATH=$PYTHONPATH:/home/danc/python/pymeg
export STAGE=/opt/msw_danc

xterm -hold -e python $PYMEGPATH/gui/PyMEG.py
#python wxmsw.py

#!/usr/bin/env python

#from gui.wxmsw import main
#main()
