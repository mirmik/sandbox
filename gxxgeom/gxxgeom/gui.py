import PyQt5 as qt
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore

import sys
import numpy

spectroWidth=500
spectroHeight=500

app = widgets.QApplication(sys.argv)

w = widgets.QMainWindow()
#w.resize(500, 300)
w.setWindowTitle('gxxgeom')
w.show()

a=numpy.zeros((spectroHeight, spectroWidth))
#a=numpy.random.random(spectroHeight*spectroWidth)*255
#a=numpy.reshape(a,(spectroHeight,spectroWidth))
#a=numpy.require(a, numpy.uint8, 'C')

l = widgets.QLabel()

def updateData():
	global a
	QI=qtgui.QImage(a.data, spectroWidth, spectroHeight, qtgui.QImage.Format_Indexed8)
	l.setPixmap(qtgui.QPixmap.fromImage(QI))

#updateData()

timer = qtcore.QTimer()
timer.start(.1)
timer.timeout.connect(updateData)

#b = widgets.QImage()
w.setCentralWidget(l)

def guiexec():
	sys.exit(app.exec())