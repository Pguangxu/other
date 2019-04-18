# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 08:29:39 2019

@author: M088107
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:05:48 2019

@author: GuangXu Pang
"""

import serial
import time
import struct
import pandas as pd
import numpy as np 
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

SER_COM='COM6'

list_array=[]
Record_Length=1024
Sample_rate=1600
#QtGui.QApplication.setGraphicsSystem('raster')
app = pg.mkQApp()
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="fft")
win.resize(1000,600)
win.setWindowTitle('Spectrum')
plot_a_x = win.addPlot(row=0, col=0, rowspan=1, colspan=1)
plot_a_y = win.addPlot(row=0, col=1, rowspan=1, colspan=1)
plot_a_z = win.addPlot(row=0, col=2, rowspan=1, colspan=1)
plot_a_a = win.addPlot(row=0, col=3, rowspan=1, colspan=1)

plot_s_x = win.addPlot(row=1, col=0, rowspan=1, colspan=1)
plot_s_y = win.addPlot(row=1, col=1, rowspan=1, colspan=1)
plot_s_z = win.addPlot(row=1, col=2, rowspan=1, colspan=1)
plot_s_a = win.addPlot(row=1, col=3, rowspan=1, colspan=1)

plot_d_x = win.addPlot(row=2, col=0, rowspan=1, colspan=1)
plot_d_y = win.addPlot(row=2, col=1, rowspan=1, colspan=1)
plot_d_z = win.addPlot(row=2, col=2, rowspan=1, colspan=1)
plot_d_a = win.addPlot(row=2, col=3, rowspan=1, colspan=1)
#p1.setWindowTiltle('X')

#加速度
curve_x=plot_a_x.plot(pen='r')
curve_y=plot_a_y.plot(pen='g')
curve_z=plot_a_z.plot(pen='b')
curve_a=plot_a_a.plot()
#速度
curve2_x=plot_s_x.plot(pen='r')
curve2_y=plot_s_y.plot(pen='g')
curve2_z=plot_s_z.plot(pen='b')
curve2_a=plot_s_a.plot()
#位移7
curve3_x=plot_d_x.plot(pen='r')
curve3_y=plot_d_y.plot(pen='g')
curve3_z=plot_d_z.plot(pen='b')
curve3_a=plot_d_a.plot()
#ser.close()
ser = serial.Serial(port=SER_COM, baudrate=115200)#parity
byte_received=b''
array_integral_factor=np.zeros(Sample_rate>>1)
array_float_acceleration=np.zeros(Sample_rate>>1)
array_float_speed=np.array([])
array_float_distance=np.array([])
#for i in range(0,Record_Length>>1):
    #list_integral_factor.append( i*Sample_rate/Record_Length*2*np.pi)
def plotdata():
    
    global byte_received 
    global Record_Length 
    global array_integral_factor
    global list_array
    global array_float_acceleration
    global array_float_speed
    global array_float_distance
    i_read_number =int(12+256)
    data=ser.read(i_read_number)  
                                                                            
    byte_received+=  data
    #data = ser.read_until('UUUU')
    index_head=byte_received.find(b'BEG\r')
    if index_head>0:
        uint16_trcord_length=byte_received[index_head+6:index_head+7]
        Record_Length=struct.unpack('<B',uint16_trcord_length)[0]
        Record_Length=np.power(2,Record_Length)
        #print(Record_Length)
        i_read_number=int(Record_Length*2-256)
        data=ser.read(i_read_number)
        byte_received+=  data
    else:
        pass
    
    
    if len(byte_received)>=(index_head+Record_Length*2+12):
        byte_fft=byte_received[index_head+12:index_head+Record_Length*2+12]
        list_float=[]
        

            
        if b'A'==  byte_received[index_head+4:index_head+5]:
            for i in range(0,Record_Length):
                uint16_amplitude=byte_fft[i*2:i*2+2]
                float_temp=(struct.unpack('<h',uint16_amplitude)[0])
                list_float.append(float_temp)
        else:
            for i in range(0,Record_Length>>1):
                #print(byte_fft)
                uint16_amplitude=byte_fft[i*2:i*2+2]
                float_temp=(struct.unpack('<H',uint16_amplitude)[0])/2048.0
                list_float.append(float_temp)


                result =i*Sample_rate/Record_Length*2*np.pi

                if result==0:
                    result=1000000000
                array_integral_factor[i]=result
            
            
            
            
        t=np.arange(Sample_rate>>1)
        #print(str(list_float[0])+' '+str(list_float[1]))
        for i in range(0,Sample_rate>>1):
            array_float_acceleration[i]=list_float[(Record_Length*i)//Sample_rate]
            

        array_float_speed=np.zeros(800)#array_float_acceleration/array_integral_factor
        array_float_distance=np.zeros(800) #array_float_speed/array_integral_factor
        if b'X'==  byte_received[index_head+4:index_head+5]:      
    
            curve_x.setData(t,array_float_acceleration)
            curve2_x.setData(t,array_float_speed)
            curve3_x.setData(t,array_float_distance)
            list_float.insert(0,0)
            list_array.append(list_float)
            list_speed=list(array_float_speed)
            list_speed.insert(0,1) 
            list_distance= list(array_float_distance)
            list_distance.insert(0,2)
            list_array.append( list_speed  )
            list_array.append(list_distance  )
        if b'Y'==  byte_received[index_head+4:index_head+5]:      

            curve_y.setData(t,array_float_acceleration)
            curve2_y.setData(t,array_float_speed)
            curve3_y.setData(t,array_float_distance)
            list_float.insert(0,3)
            list_array.append(list_float)
            list_speed=list(array_float_speed)
            list_speed.insert(0,4) 
            list_distance= list(array_float_distance)
            list_distance.insert(0,5)
            list_array.append( list_speed  )
            list_array.append(list_distance  )
        if b'Z'==  byte_received[index_head+4:index_head+5]:
            print('z')
            curve_z.setData(t,array_float_acceleration)
            #curve2_z.setData(t,array_float_speed)
            #curve3_z.setData(t,array_float_distance)
            list_float.insert(0,6)
            list_array.append(list_float)
            list_speed=list(array_float_speed)
            list_speed.insert(0,7) 
            list_distance= list(array_float_distance)
            list_distance.insert(0,8)
            list_array.append( list_speed  )
            list_array.append(list_distance  )
        if b'A'==  byte_received[index_head+4:index_head+5]:
            print(list_float)
            print(len(list_float))
            array_float=np.array(list_float)
            #print(len(array_float))
            array_float_hann=array_float*( 0.5-np.cos(np.arange(0,len(list_float))*np.pi*2/( len(list_float) )) *0.5 )
            array_fft_complex=np.fft.fft(array_float)
            array_fft_complex_hann=np.fft.fft(array_float_hann)
            array_fft_mag=np.abs(array_fft_complex)
            array_fft_mag=array_fft_mag

            array_fft_mag_hann=np.abs(array_fft_complex_hann)
            array_fft_mag_hann = array_fft_mag_hann
            array_fft_mag=array_fft_mag/(Record_Length)
            array_fft_mag_hann=array_fft_mag_hann/(Record_Length)
            list_float=list(array_float_acceleration)
            array_float_acceleration_hann=np.zeros(Sample_rate>>1)


            
            ser_len= int(len(array_fft_mag)/2)
            #print(ser_len)
            curve_a.setData(np.arange(ser_len),array_fft_mag[0:ser_len] )
            curve2_a.setData(np.arange(ser_len),array_fft_mag_hann[0:ser_len] )
            curve3_a.setData(np.arange(len(array_float_hann)),array_float_hann)
            curve3_z.setData(np.arange(len(array_float)),array_float)
            list_float.insert(0,9)
            
            list_array.append(list_float)
            list_speed=list(array_float_speed)
            list_speed.insert(0,10) 
            list_distance= list(array_float_distance)
            list_distance.insert(0,11)
            list_array.append( list_speed  )
            list_array.append(list_distance  )
        byte_received=byte_received[index_head+Record_Length*2+12:]
    #data=data[index_head:index_head+4100]

    else:
        pass
        
def closeWindow():
    print('close')  

timer=pg.QtCore.QTimer()
timer.timeout.connect(plotdata)
timer.start(100)

'''
while True:
    time.sleep(1)
    list_float=[]
    data=ser.read(8200)
    #print(data)
    #data = ser.read_until('UUUU')
    index_head=data.find(b'UUUU')+4
    data=data[index_head:index_head+4100]
    if 1025*4==len(data):
        print('hh')
        for i in range(0,Record_Length):
            byte_afloat=data[i*4:i*4+4]
            float_temp=struct.unpack('<f',byte_afloat)[0]
            list_float.append(float_temp)

        y=np.array(list_float)
        plotdata()'''

        
app.exec_()
ser.close()
print('Serial port closed')
print(len(list_array[0]) )
df=pd.DataFrame(np.array(list_array)  )
print('dataframe created')
df.to_csv('fft_result.csv',index=False,encoding='utf_8')

print('data writed to csv')
 