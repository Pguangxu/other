# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:17:41 2019

@author: Administrator
"""

import pywintypes

import struct

import win32event

import win32com.directsound.directsound as ds



BytesPerSample=1
BitsPerSample=BytesPerSample*8
Size=1024

d = ds.DirectSoundCaptureCreate(None, None)
sdesc = ds.DSCBUFFERDESC()
sdesc.dwBufferBytes = 1024  # 2 seconds
sdesc.lpwfxFormat = pywintypes.WAVEFORMATEX()
sdesc.lpwfxFormat.wFormatTag = pywintypes.WAVE_FORMAT_PCM
sdesc.lpwfxFormat.nChannels = 2
sdesc.lpwfxFormat.nSamplesPerSec = 44100
sdesc.lpwfxFormat.nAvgBytesPerSec = 176400
sdesc.lpwfxFormat.nBlockAlign = 4
sdesc.lpwfxFormat.wBitsPerSample = 16
buffer = d.CreateCaptureBuffer(sdesc)




event = win32event.CreateEvent(None, 0, 0, None)

notify = buffer.QueryInterface(ds.IID_IDirectSoundNotify)



notify.SetNotificationPositions((ds.DSBPN_OFFSETSTOP, event))



buffer.Start(0)



win32event.WaitForSingleObject(event, -1)



# in real life, more, smaller buffers should be retrieved

data = buffer.Update(0, 1024)



f = open('recording.wav', 'wb')

#f.write(wav_header_pack(sdesc.lpwfxFormat, 352800))

f.write(data)