# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:32:17 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyqtgraph as pg
import numpy as np
import array 

import pyaudio
import wave



CHANNELS=2
SIZE=1024
RATE = 16000
Time_duration=1#s
RECORD_SECONDS = 1
FORMAT = pyaudio.paInt16
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=SIZE*2)




i=range(0,SIZE)
x_sin=np.sin(np.array(i)*np.pi*0.125)

#array_FFT=array.array("d")

app = pg.mkQApp()
win=pg.GraphicsWindow()
win.setWindowTitle("Test")
win.resize(1000,300)
plot_sin=win.addPlot()
plot_fft=win.addPlot()
#plot_fft_r=win.addPlot()
#plot_fft_i=win.addPlot()
#plot_sin=pg.plot(x_sin,title='sin')
curve_sin=plot_sin.plot(pen="y")
curve_fft=plot_fft.plot(pen="r")
#curve_fft_r=plot_fft_r.plot(pen="r")
#curve_fft_i=plot_fft_i.plot(pen="r")
#idx=0
frames = []
def update():
    for i in range(0, int((RATE / SIZE * Time_duration))>>1):
        data = stream.read(SIZE*2)
        wave_data = np.frombuffer(data, dtype=np.short)

    

        array_sin=np.array(wave_data)
        array_FFT_c=np.fft.fft(wave_data,SIZE)
        curve_sin.setData(array_sin)
        del array_sin
    
        array_FFT=np.absolute(array_FFT_c)
    
        curve_fft.setData(array_FFT)
        #curve_fft_r.setData(np.real(array_FFT_c))
        #curve_fft_i.setData(np.imag(array_FFT_c))
    #idx+=1
    
timer=pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(Time_duration*1000)    
app.exec_()
stream.stop_stream()
stream.close()
p.terminate()