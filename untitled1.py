# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:49:29 2019

@author: Administrator
"""

import pyaudio
import wave


WAVE_OUTPUT_FILENAME = "Oldboy.wav"
CHANNELS=2
SIZE=1024
RATE = 44200
Time_duration=4#s
RECORD_SECONDS = 1
FORMAT = pyaudio.paInt16
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=SIZE)



frames = []
for i in range(0, int(RATE / SIZE * Time_duration)):
    data = stream.read(SIZE)
    if len(frames)<SIZE:
        frames.append(data)
    else:   
        frames[:-1]=frames[1:]
        frames[-1]=data
        
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()