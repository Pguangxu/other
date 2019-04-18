# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:23:46 2019

@author: M088107
"""


import urllib
import json
import base64
import struct
import pyqtgraph as pg
import serial
import sys
import random
import os
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports

import time
import numpy as np
SER_COM=0
ser=''
url_path='http://iot.beaconice.cn/v2/stream/messages'
device_id='aa0001000402'

sample_rate= 2000
mode=1
dircection = 'Z'
if_data_updated=False
x_N_mag=b''
y_N_mag=b''
z_N_mag=b''

x_N_mag_list=[]
y_N_mag_list=[]
z_N_mag_list=[]

byte_received=b''

win = pg.GraphicsWindow(title="fft")
win.resize(1000,600)
win.setWindowTitle('Spectrum')
plot_a_x = win.addPlot(row=0, col=0, rowspan=1, colspan=1)
plot_a_y = win.addPlot(row=0, col=1, rowspan=1, colspan=1)
plot_a_z = win.addPlot(row=0, col=2, rowspan=1, colspan=1)
curve_x=plot_a_x.plot(pen='r')
curve_y=plot_a_y.plot(pen='r')
curve_z=plot_a_z.plot(pen='r')
def ini_serial():
    global SER_COM
    global ser
    for info in comports(False):
        if 'USB Serial Port' in info.description:
            SER_COM=info.device
            print(SER_COM)
    ser = serial.Serial(port=SER_COM, baudrate=921600,timeout=None, xonxoff=0, rtscts=1)#parity
    
    


def get_data():
    global x_N_mag
    global y_N_mag
    global z_N_mag
    global sample_rate
    global mode
    global byte_received
    x_N_mag=b''
    y_N_mag=b''
    z_N_mag=b''
    byte_received +=ser.read_all()
    print(len(byte_received)/546)
    if 6< len(byte_received)/546:
        byte_received=b''
    elif 0==len(byte_received)/546:
        byte_received=b''
    else:
        pass
    
    if 6==len(byte_received)/546 :
        
        index_head=byte_received.find((b'\xe7\x03\xe7\x03') )
        if 6==index_head:              
            if_data_updated=True
            
            uint16_sample_rate=byte_received[4:6]
            sample_rate=struct.unpack('<H',uint16_sample_rate)[0]
            print('sample rate:'+str(sample_rate))
            uint8_mode=byte_received[1:2]
            mode=struct.unpack('<B',uint8_mode)[0]
            print('mode:'+str(mode))
            x_N_mag_list=[]
            y_N_mag_list=[]
            z_N_mag_list=[]
            x_N_mag=b''
            y_N_mag=b''
            z_N_mag=b''
            if 0==mode :
                i=34
                x_N_mag+=byte_received[i:i+512]
                while i<546:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    x_N_mag_list.append(float_temp)
                    i+=2
                i=34+546
                y_N_mag+=byte_received[i:i+512]
                while i<546*2:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    y_N_mag_list.append(float_temp)
                    i+=2
                i=34+546*2
                z_N_mag+=byte_received[i:i+512]
                while i<546*3:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    z_N_mag_list.append(float_temp)
                    i+=2
                            
            elif 1==mode:
                #  X axix
                i=34
                x_N_mag+=byte_received[i:i+512]
                while i<546:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    x_N_mag_list.append(float_temp)
                    i+=2
                i=34+546
                x_N_mag+=byte_received[i:i+512]
                while i<546*2:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    x_N_mag_list.append(float_temp)
                    i+=2

                #  Y axix
                i=34+546*2
                y_N_mag+=byte_received[i:i+512]
                while i<546*3:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    y_N_mag_list.append(float_temp)
                    i+=2
                i=34+546*3
                y_N_mag+=byte_received[i:i+512]
                while i<546*4:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    y_N_mag_list.append(float_temp)
                    i+=2
                #  Z axix
                i=34+546*4
                z_N_mag+=byte_received[i:i+512]
                while i<546*5:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    z_N_mag_list.append(float_temp)
                    i+=2
                i=34+546*5
                z_N_mag+=byte_received[i:i+512]
                while i<546*6:
                    uint16_amplitude=byte_received[i:i+2]
                    float_temp=(struct.unpack('<H',uint16_amplitude)[0])/1000.0                
                    z_N_mag_list.append(float_temp)
                    i+=2
            curve_x.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( x_N_mag_list ))
            curve_y.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( y_N_mag_list ))
            curve_z.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( z_N_mag_list ))
            #plot_data()
            byte_received=b''
        
        
    else:
        if_data_updated=False
        
    '''
    
    i_read_number =int(546)
    data=ser.read(i_read_number)
    byte_received+=data
    index_head=byte_received.find(b'E703E703\r')
    print('index_head'+str(index_head))
    if index_head>5:
        i_read_number =int(546)
        data=ser.read(i_read_number-6)
        byte_received+=data
        print('len byte'+str(len(byte_received)))
        uint16_trcord_length=byte_received[index_head-4:index_head-2]
        Record_Length=struct.unpack('<B',uint16_trcord_length)[0]
        if Record_length==512:
            mode=1
        else:
            mode=0
        uint16_sample_rate=byte_received[index_head-2:index_head]
        sample_rate=struct.unpack('<B',uint16_sample_rate)[0]
            

        i_read_number=int(Record_Length*2-256)
        data=ser.read(i_read_number)
        byte_received+=  data
    else:
        byte_received=byte_received[max(len(byte_received,index_head+546)):]
        pass
    
    
    if len(byte_received)>=(index_head+Record_Length*2+12):
        byte_fft=byte_received[index_head+12:index_head+Record_Length*2+12]
        list_float=[]
    '''
    '''
    temp=random.randint(1000-30,1000+30)
    x_N_mag+=struct.pack('H',temp)
    for i in range(1,10):
        temp=random.randint(45*(10-i),55*(10-i))
        x_N_mag+=struct.pack('H',temp)
    for i in range(10,512):
        
        x_N_mag+=struct.pack('H',0)'''
        #y_N_mag+=struct.pack('H',512-i)
        #z_N_mag+=struct.pack('H',512-i)
        
def plot_data():
    global x_N_mag_list
    global y_N_mag_list
    global z_N_mag_list
    
    global plot_a_x
    global plot_a_y
    global plot_a_z
    curve_x.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( x_N_mag_list ))
    curve_x.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( y_N_mag_list ))
    curve_x.setData(np.array( range(0,len(x_N_mag_list)) ),np.array( z_N_mag_list ))
    print(x_N_mag_list[0:5])
    print(y_N_mag_list[0:5])
    print(z_N_mag_list[0:5])
def post_data():    
    global url_path
    global x_N_mag
    global y_N_mag
    global z_N_mag
    get_data()
    headers = {'Content-Type': 'application/json'}
    data = {
        'did': device_id,
        'type': 'stream',
        'data':{
            "sampleRate": sample_rate,
            "mode": mode,
            "x": str(base64.b64encode(x_N_mag),encoding='utf-8'),
            "y": str(base64.b64encode(y_N_mag),encoding='utf-8'),
            "z": str(base64.b64encode(z_N_mag),encoding='utf-8')                
                }       
    }
        
    try:
        request = urllib.request.Request(url=url_path, headers=headers, data=json.dumps(data).encode("utf-8"))
        print(urllib.request.urlopen(request).read().decode("utf-8")   )
    except:
        print('error')
        pass

app = pg.mkQApp()
ini_serial()
timer=pg.QtCore.QTimer()
timer.timeout.connect(get_data)
timer.start(2000)

app.exec_()
ser.close()