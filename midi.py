###########################################################################
##                                                                       ##
##  Copyright 2013-2017 Alexandra van den Heetkamp                       ##
##                                                                       ##
##  This file is part of ReaScore/ReaChorder.                            ##
##                                                                       ##
##  ReaScore is free software: you can redistribute it and/or modify it  ##
##  under the terms of the GNU General Public License as published       ##
##  by the Free Software Foundation, either version 3 of the             ##
##  License, or any later version.                                       ##
##                                                                       ##
##  ReaScore is distributed in the hope that it will be useful, but      ##
##  WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        ##
##  GNU General Public License for more details.                         ##
##  <http://www.gnu.org/licenses/>.                                      ##
##                                                                       ##
###########################################################################

import math
import sys
import ctypes

from multiprocessing import Process, Lock

from modules.maps import *
from modules.helpers import *
from modules.caps import *
import time

from ctypes import WINFUNCTYPE, windll, wintypes, c_long, c_char_p, byref
from ctypes.wintypes import *


class MIDI(object):

    def __init__(self):

        global inHandle, outHandle, device, stream, deviceID

        inHandle  = c_long()
        outHandle = c_long()
        device    = c_long()
        stream    = 0
        deviceID  = 0
        self.regDevicesIn  = []
        self.regDevicesOut = []
        self.PROC = WNDPROC(self.capture_midi)
        self.lib  = windll.winmm
        self.noteDelta = 0.4

    def evt_callback(self,val):

        lock = Lock()
        Process(target=self.play_note(int(val[0]),int(val[2]),0,self.noteDelta), args=(lock,)).start()

    def listen_device(self,devID):

        global deviceID
        deviceID = devID
        stream = 1
        try:
            self.lib.midiInOpen(byref(inHandle), devID, self.PROC, devID, MIDI_CALLBACK_FUNCTION)
            self.lib.midiInStart(inHandle)
        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

    def capture_midi(self,inHandle, msg, devID, mim_data, delta):

        if deviceID != devID:
            print('device is gone.')
        else:
            try:
                evt = []
                msgId   = hex(msg)
                recv    = int(mim_data)
                recvMsg = hex(recv & 0xFF)

                if msgId == '0x3c3':

                    if recvMsg == '0x90':
                        note     = int((recv & 0xFF * 256) >> 8)
                        velocity = int((recv & ((2 << 24) - 1)) >> 16)
                        if velocity >=1:
                            evt.append(note)
                            evt.append(delta)
                            evt.append(velocity)
                            self.evt_callback(evt)
                    if recvMsg == '0x80':
                        print('device note-off.')
                        pass

                elif msgId == '0x3c1':
                    # MM_MIM_OPEN
                    return
                elif msgId == '0x3c2':
                    # MM_MIM_CLOSE
                    return
                elif msgId == '0x3c5':
                    # MM_MIM_ERROR
                    return
                elif msgId == '0x3c6':
                    # MM_MIM_LONGERROR
                    return
                elif msgId == '0x3cc':
                    # MOREDATA
                    return
                else:
                    return

            except (RuntimeError, KeyboardInterrupt, EOFError):
                pass

    def play_note(self,note,volume=127,channel=0,sleep=0):

        try:
            midion  = 0x90 + (note * 0x100) + (volume * 0x10000) + channel
            midioff = 0x80 + (note * 0x100) + channel
            self.lib.midiOutShortMsg(outHandle, midion)
            time.sleep(sleep)
            self.lib.midiOutShortMsg(outHandle, midioff)
        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

    def open_device(self,method,devID):

        global deviceID

        if stream == 1:
            self.close_device('out')

        if method == 'in':
            deviceID = devID
            try:
                self.lib.midiInOpen(byref(inHandle), deviceID, 0, 0, 0)
                self.regDevicesIn.append(inHandle)
            except (RuntimeError, TypeError, EOFError):
                pass
        else:
            try:
                self.lib.midiOutOpen(byref(outHandle), devID, 0, 0, 0)
                self.regDevicesOut.append(outHandle)
            except (RuntimeError, TypeError, EOFError):
                pass

    def close_device(self,method):

        global stream

        if method == 'in':
            try:
                stream = 0
            except (RuntimeError, KeyboardInterrupt, EOFError):
                pass
        else:
            try:
                self.lib.midiOutClose(outHandle)
                stream = 0
            except (RuntimeError, KeyboardInterrupt, EOFError):
                pass

    def reset_device(self,method,oldID,devID):

        if method == 'in':
            try:
                self.close_device('in',int(oldID))
            except:
                pass
            finally:
                self.listen_device(int(devID))
        else:
            self.close_device('out')
            self.open_device('out',int(devID))

    def midi_stop(self):
        try:
            self.lib.midiInStop(inHandle)
        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

    def midi_reset(self):
        try:
            self.lib.midiInReset(inHandle)
        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

    def midi_exit(self):

        # be nice, and close all devices.

        self.midi_stop()
        self.midi_reset()

        try:
            self.lib.midiOInClose(inHandle)
            self.lib.midiOutClose(outHandle)
        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

        try:
            devListIn  = self.regDevicesIn
            devListOut = self.regDevicesOut

            for i in range(len(devListIn)):
               self.lib.midiOInClose(devListIn[i])
            for i in range(len(devListOut)):
               self.lib.midiOutClose(devListOut[i])

        except (RuntimeError, KeyboardInterrupt, EOFError):
            pass

    def devices(self,method):

        devicelist = []

        '''
        caps.wMid,
        caps.wPid,
        caps.vDriverVersion,
        caps.wVoices,
        caps.wNotes,
        caps.wChannel_mask,
        caps.dwSupport
        '''

        if method == 'in':

            dev = self.lib.midiInGetNumDevs()
            try:
                caps = MIDIINCAPS()
                for i in range(0,dev):
                    out = self.lib.midiInGetDevCapsA(i,byref(caps),ctypes.sizeof(caps))
                    name = ctypes.string_at(ctypes.cast(caps.szPname, c_char_p))
                    devicelist.extend([
                    name.decode(encoding="utf-8")
                    ])

            except (RuntimeError, NameError, TypeError, AttributeError):
                pass
        else:

            dev = self.lib.midiOutGetNumDevs()
            try:
                caps = MIDIOUTCAPS()
                for i in range(-1,dev):
                    out = self.lib.midiOutGetDevCapsA(i,byref(caps),ctypes.sizeof(caps))
                    name = ctypes.string_at(ctypes.cast(caps.szPname, c_char_p))
                    devicelist.extend([
                    name.decode(encoding="utf-8")
                    ])

            except (RuntimeError, NameError, TypeError, AttributeError):
                pass

        return devicelist


    def write(self,timesig,BPM,notes):

        list                = Helpers.splitInt(timesig)
        self.numerator      = list[0]
        self.denominator    = list[1]
        self.PPQN           = 96
        self.MIDI_CLOCK     = 24
        self.MSPM           = int(float(6e7))                            # ms per minute
        self.MPQN           = (self.MSPM / int(BPM))                     # ms per quarternote
        self.QLS            = (self.MPQN / int(float(1e6)))              #  s per quarternote
        self.TDPS           = (self.QLS / self.PPQN)                     #  s per tick
        self.CLOCK_TICK     = ((self.MPQN / int(float(1e6))) / self.PPQN)    # Tick in Hz
        self.BAR_LENGTH     = ((self.numerator * self.QLS  * 4 ) / self.denominator)
        self.TICKS_PER_BAR  = (int(self.PPQN) * int(self.numerator))
        self.numerator      = Helpers.toHex(self,self.numerator)
        self.denominator    = Helpers.toHex(self,math.ceil(math.sqrt(self.denominator)))

        self.WHOLE          = int(self.TICKS_PER_BAR)
        self.HALF           = int(self.TICKS_PER_BAR / 2)
        self.QUARTER        = int(self.TICKS_PER_BAR / 4)
        self.EIGHTH         = int(self.TICKS_PER_BAR / 8)
        self.SIXTEENTH      = int(self.TICKS_PER_BAR / 16)
        self.THIRTYSECOND   = int(self.TICKS_PER_BAR / 32)
        self.SIXTYFOURTH    = int(self.TICKS_PER_BAR / 64)

        file_header         = ['4D', '54', '68', '64', '00', '00', '00', '06', '00', '01', '00', '01', '00']
        track_header        = ['4D', '54', '72', '6B']
        track               = ['00']
        self.velocity       = '58'
        self.channel        = '3C'
        self.notesInBeat    = '08'

        file_header.append(Helpers.toHex(self,self.PPQN))

        for i in range(0,22):

            track.extend(Helpers.noteOn(self,midi_pitch[i][1],self.velocity))
            track.extend(Helpers.noteDelta(self,self.QUARTER))
            track.extend(Helpers.noteOff(self,midi_pitch[i][1]))
            if i < 21:
                track.extend(Helpers.noteRest(self,self.SIXTYFOURTH)) # rest

        track_size = len(track) + 29

        track_header.extend(Helpers.writeChunk(self,track_size,4))
        track_header.append('00')
        track_header.append('FF')
        track_header.append('51')
        track_header.append('03')

        track_header.extend(Helpers.writeChunk(self,int(self.MPQN),3))
        track_header.append('00')
        track_header.append('FF')
        track_header.append('58') # tempo
        track_header.append('04')

        track_header.append(str('0'+self.numerator))
        track_header.append(str('0'+self.denominator))
        track_header.append(str(self.MIDI_CLOCK))
        track_header.append(str(self.notesInBeat))

        track_header.append('00')
        track_header.append('FF')
        track_header.append('59') # key signature
        track_header.append('02')
        track_header.append('00') # no sharps or flats
        track_header.append('00') # 00 = major mode (01 = minor)

        track.append('20') # silence
        track.append('B0')
        track.append('7B')
        track.append('00')

        track.append('00') # EOF
        track.append('FF')
        track.append('2F')
        track.append('00')

        hexstring  = ''.join(file_header)
        hexstring += ''.join(track_header)
        hexstring += ''.join(track)

        output = Helpers.hexToByteArray(self,str(hexstring))

        return output

#print(MIDI.write(MIDI,22,120,0))


#MIDICONNECT = MIDI()
#MIDICONNECT.open_device('out',-1)
#MIDICONNECT.listen_device(1)

#MIDICONNECT.play_note(60,127,0,10)
#MIDICONNECT.close_device('out')

