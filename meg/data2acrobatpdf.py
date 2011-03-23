'''data2pdf'''

from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import String
from reportlab.graphics import renderPDF

from pdf2py import channel, data

from numpy import size, arange, around

def demo():
    drawing = Drawing(400, 200)
    data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (5, 20, 46, 38, 23, 21, 6, 14)
    ]
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 125
    lc.width = 300
    lc.data = data
    lc.joinedLines = 1
    catNames = string.split('Jan Feb Mar Apr May Jun Jul Aug', ' ')
    lc.categoryAxis.categoryNames = catNames
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 60
    lc.valueAxis.valueStep = 15
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeWidth = 1.5
    drawing.add(lc)
    renderPDF.drawToFile(drawing, 'example1.pdf', 'My First Drawing')
    return drawing

def getdata(datapath, chtype):
    ch = channel.index(datapath, chtype)
    d = data.read(datapath)
    labels = ch.chlabel[ch.channelsind]
    d.getdata(0, d.pnts_in_file, ch.channelsind)
    return d, labels

def scalevalue(d):
    numch = size(d.data_block,1)
    range = d.data_block.max()-d.data_block.min()
    scaleval = arange(0,range,range/numch)
    scaleval = scaleval + scaleval[1]
    return scaleval

def drawdata(data, times, labels):
    drawing = Drawing(10000, 200)
    fontstep = 5.5
    for i in range(0, size(labels)):
        drawing.add(String(40,(i+9.8)*fontstep,str(labels[i]), textAnchor="middle", fontSize=5))
    #drawing.add(String(20,175,"labels", textAnchor="middle", fontSize=5))
    #data = [1, 2, 3, 4, 5, 6]
    lc = HorizontalLineChart()
    #lc.valueAxis = 0
    lc.x = 50
    lc.y = 50
    lc.height = 155
    lc.width = 10000
    lc.data = data
    lc.joinedLines = 1
    #catNames = string.split('Jan Feb Mar Apr May Jun Jul Aug', ' ')
    #catNames = times
    #lc.categoryAxis.categoryNames = catNames
    #lc.categoryAxis.labels.boxAnchor = 'n'
    lc.categoryAxis.visible = 0
    fontstep = 40
    for i in range(0, size(times)):
        drawing.add(String((i+1.3)*fontstep,45,str(times[i]), textAnchor="middle", fontSize=5))
    
    lc.lineLabelArray = ['1','2']
    #lc.valueAxis.valueMin = 0
    #lc.valueAxis.valueMax = 60

    lc.valueAxis.valueStep = 1
    #lc.valueAxis.valueSteps = [1, 2, 3, 5, 6]
    lc.lines[0].strokeWidth = .5
    lc.lines[1].strokeWidth = .5
    drawing.add(lc)
    renderPDF.drawToFile(drawing, 'example1.pdf', 'EEG data')
    return drawing, lc

def from4dpdf(datapath, chtype, timechunk):
    '''datapath = '/opt/msw/data/spartan_data0/E-0031/Epilepsy/04%28%05@09:47/1/c,rfhp1.0Hz,f3-70n,o'
    chtype = 'eeg'
    timechunk = 5 #in sec'''
    [d,labels] = getdata(datapath, chtype)
    scaleval = scalevalue(d)
    #return scaleval
    d.data_block = d.data_block+scaleval #space/scale data
    
    numchunks = round(d.wintime[-1]/timechunk)
    
    #startind = 0; endind = d.wintime
    ind = d.wintime < timechunk
    times=around(d.wintime[ind][:-1:200],1)
    #times = str(d.wintime[ind])#('1',' ')
    for i in range(0, numchunks):
        drawdata(d.data_block[ind,:].T, times, labels)
        return
        
def fromraw(data, chlabels, timechunk):
    numch = size(d.data_block,1)
    range = d.data_block.max()-d.data_block.min()
    scaleval = arange(0,range,range/numch)
    scaleval = scaleval + scaleval[1]
    
    
    
    
##    """Shows basic use of a line chart."""
##    drawing = Drawing(400, 200)
##    data = [
##    ((1,1), (2,2), (2.5,1), (3,3), (4,5)),
##    ((1,2), (2,3), (2.5,2), (3.5,5), (4,6))
##    ]
##    lp = LinePlot()
##    lp.x = 50
##    lp.y = 50
##    lp.height = 125
##    lp.width = 300
##    lp.data = data
##    lp.joinedLines = 1
##    lp.lineLabelFormat = '%2.0f'
##    lp.strokeColor = colors.black
##    lp.lines[0].strokeColor = colors.red
##    lp.lines[0].symbol = makeMarker('FilledCircle')
##    lp.lines[1].strokeColor = colors.blue
##    lp.lines[1].symbol = makeMarker('FilledDiamond')
##    lp.xValueAxis.valueMin = 0
##    lp.xValueAxis.valueMax = 5
##    lp.xValueAxis.valueStep = 1
##    lp.yValueAxis.valueMin = 0
##    lp.yValueAxis.valueMax = 7
##    lp.yValueAxis.valueStep = 1
##    drawing.add(lp)
    

#renderPDF.drawToFile(d, 'example1.pdf', 'My First Drawing')
