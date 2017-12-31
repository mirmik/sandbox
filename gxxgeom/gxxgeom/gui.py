import PyQt5 as qt
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore

import sys
import numpy

from gxxgeom.render import Render

class MQMainWindow(widgets.QMainWindow) :
	changePosition = qtcore.pyqtSignal(qtcore.QPoint)
	changeCenter = qtcore.pyqtSignal(qtcore.QPoint)
	wheelSignal = qtcore.pyqtSignal(int)
	
	def __init__(self):
		super(widgets.QMainWindow, self).__init__()
		self.handlers = {}

	
	def mousePressEvent(self, event):
		self.lastpos = event.pos()
		
	def mouseMoveEvent(self, event):
		diff = event.pos() - self.lastpos
		self.lastpos = event.pos()

		if event.buttons() == qtcore.Qt.LeftButton:
			self.changePosition.emit(diff)

		if event.buttons() == qtcore.Qt.MiddleButton:
			self.changeCenter.emit(diff)


	def keyPressEvent(self, event):
		if type(event) == qtgui.QKeyEvent:
			event.accept()

		if event.key() in self.handlers:
			self.handlers[event.key()]()

		else:
			event.ignore()

	def wheelEvent(self, event):
		self.wheelSignal.emit(event.angleDelta().y())

class GUI:
	def __init__(self):
		self.app = widgets.QApplication(sys.argv)
	
		self.w = MQMainWindow()
		self.w.setWindowTitle('gxxgeom')
		self.w.show()
			
		self.l = widgets.QLabel()
		self.w.setCentralWidget(self.l)

		self.w.resize(500,500)

	def setTimeoutHandler(self, handler, time = 0.1):
		self.timer = qtcore.QTimer()
		self.timer.start(.1)
		self.timer.timeout.connect(handler)
		
	def setData(self, array):
		a = numpy.require(array, numpy.uint8, 'C')
		self.QI = qtgui.QImage(a.data, array.shape[0], array.shape[1], qtgui.QImage.Format_Indexed8)
		self.l.setPixmap(qtgui.QPixmap.fromImage(self.QI))
	
	def connectMouseHandler(self, func):
		self.w.changePosition.connect(func)

	def connectWheelHandler(self, func):
		self.w.wheelSignal.connect(func)

	def connectCenterHandler(self, func):
		self.w.changeCenter.connect(func)

	def addKeyHandler(self, chr, handler):
		self.w.handlers[chr] = handler

	def exec(self):
		sys.exit(self.app.exec())