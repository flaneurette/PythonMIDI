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

from ctypes import WINFUNCTYPE, wintypes, c_long, c_char_p, byref
from ctypes.wintypes import *

MIDI_CALLBACK_FUNCTION = 196608

WNDPROC = WINFUNCTYPE(None, c_long, UINT, DWORD, DWORD, DWORD)

class MIDIINCAPS(ctypes.Structure):

    _fields_ = [
        ('wMid', WORD),
        ('wPid', WORD),
        ('vDriverVersion', UINT),
        ('szPname', BYTE * 64),
        ('dwSupport', DWORD),
    ]

class MIDIOUTCAPS(ctypes.Structure):

    _fields_ = [

        ('wMid', WORD),
        ('wPid', WORD),
        ('vDriverVersion', UINT),
        ('szPname', BYTE * 64),
        ('wTechnology', WORD),
        ('wVoices', WORD),
        ('wNotes', WORD),
        ('wChannel_mask', WORD),
        ('dwSupport', DWORD),
    ]

    device_type = [

        'NONE',
        'MOD_MIDIPORT',     # MIDI hardware port.
        'MOD_SYNTH',        # Synthesizer.
        'MOD_SQSYNTH',      # Square wave synthesizer.
        'MOD_FMSYNTH',      # FM synthesizer
        'MOD_MAPPER',       # Microsoft MIDI mapper.
        'MOD_WAVETABLE',    # Hardware wavetable synthesizer.
        'MOD_SWSYNTH',      # Software synthesizer.
        'NONE',
    ]
