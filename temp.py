# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyqtgraph as pg
import numpy as np
import array 


import pywintypes
import struct
import win32event
import win32com.directsound.directsound as ds


BytesPerSample=4
BitsPerSample=BytesPerSample*8
SIZE=1024
buffer_SIZE=176400#176400
d = ds.DirectSoundCaptureCreate(None, None)
sdesc = ds.DSCBUFFERDESC()
sdesc.dwBufferBytes = buffer_SIZE # 2 seconds
sdesc.lpwfxFormat = pywintypes.WAVEFORMATEX()
sdesc.lpwfxFormat.wFormatTag = pywintypes.WAVE_FORMAT_PCM
sdesc.lpwfxFormat.nChannels = 2
sdesc.lpwfxFormat.nSamplesPerSec = 44100
sdesc.lpwfxFormat.nAvgBytesPerSec = buffer_SIZE
sdesc.lpwfxFormat.nBlockAlign = BytesPerSample
sdesc.lpwfxFormat.wBitsPerSample = BytesPerSample*4
buffer = d.CreateCaptureBuffer(sdesc)







i=range(0,SIZE)
x_sin=np.sin(np.array(i)*np.pi*0.125)
array_sin=array.array("d")
#array_FFT=array.array("d")
buffer.Start(0)
app = pg.mkQApp()
win=pg.GraphicsWindow()
win.setWindowTitle("Test")
win.resize(1000,300)
plot_sin=win.addPlot()
plot_fft=win.addPlot()
plot_fft_r=win.addPlot()
plot_fft_i=win.addPlot()
#plot_sin=pg.plot(x_sin,title='sin')
curve_sin=plot_sin.plot(pen="y")
curve_fft=plot_fft.plot(pen="r")
curve_fft_r=plot_fft_r.plot(pen="r")
curve_fft_i=plot_fft_i.plot(pen="r")
#idx=0
def update():
    
    data = buffer.Update(0, buffer_SIZE)
    buffer.Start(0)
    
    '''
    global idx
    x_sin_a=np.sin(idx*np.pi*0.125)+2*np.sin(np.sin(idx*np.pi*0.25))
    if len(array_sin)<SIZE:
        array_sin.append(x_sin_a)
    else:   
        array_sin[:-1]=array_sin[1:]
        array_sin[-1]=x_sin_a
       '''
    array_sin=array.array("d")
    seg=BytesPerSample>>1
    for i in range(0,min(buffer_SIZE,SIZE)):
        temp=int.from_bytes(data[i:i+seg], byteorder='little', signed=False)
        array_sin.append(temp)
        print(array_sin)
    
    array_FFT_c=np.fft.fft(array_sin,SIZE)
    curve_sin.setData(array_sin)
    del array_sin

    array_FFT=np.absolute(array_FFT_c)

    curve_fft.setData(array_FFT)
    curve_fft_r.setData(np.real(array_FFT_c))
    curve_fft_i.setData(np.imag(array_FFT_c))
    #idx+=1
    
timer=pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)    
app.exec_()