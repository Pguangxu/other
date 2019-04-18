# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:05:48 2019

@author: Administrator
"""

import serial
import time
import struct

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
Record_Length=1024
#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="fft")
win.resize(1000,600)
win.setWindowTitle('Spectrum')
p1 = win.addPlot(title="Basic array plotting", y=np.random.normal(size=100))
curve=p1.plot(pen='r')
#ser.close()
ser = serial.Serial(port='COM7', baudrate=57600)

serial.Serial

while True:
    #sleep.sleep(0.5)
    list_float=[]
    data = ser.readline()
    print(data)
    data = ser.read_until('UUUU')
    if 1025*4==len(data):
        for i in range(0,Record_Length):
            byte_afloat=data[i*4,i*4+4]
            float_temp=struct.unpack('<f',byte_afloat)[0]
            list_float.append(float_temp)
            curve.setData(list_float)
        
        