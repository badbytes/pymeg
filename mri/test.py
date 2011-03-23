figim = figure(figsize=(8,4))
axsrc24 = figim.add_subplot(121, xlim=(0,200), ylim=(0,200),  
autoscale_on=False)
axsrc24.set_title('Click to zoom')
axsrc70 = figim.add_subplot(122, xlim=(0,100), ylim=(0,100),  
autoscale_on=False)
axsrc70.set_title('Click to zoom')

def clicker(event):
    if event.inaxes == axsrc24:
        print 'you clicked on the 24 micron image'
    if event.inaxes == axsrc70:
        print 'you clicked on the 70 micron image'
    return

figim.canvas.mpl_connect("button_press_event",clicker)
