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

try:
    from reaper_python import *
    from sws_python import *
except:
    pass

    def getActTakeInEditor():
        return RPR_MIDIEditor_GetTake(RPR_MIDIEditor_GetActive())

    def allocateMIDITake(midiTake):
        return FNG_AllocMidiTake(midiTake)

    def freeMIDITake(midiTake):
        FNG_FreeMidiTake(midiTake)

    def countNotes(midiTake):
        return FNG_CountMidiNotes(midiTake)

    def getMidiNote(midiTake, index):
        return FNG_GetMidiNote(midiTake, index)

    def getMidiNoteIntProperty(midiNote, prop):
        return FNG_GetMidiNoteIntProperty(midiNote, prop)

    def setMidiNoteIntProperty(midiNote, prop, value):
        FNG_SetMidiNoteIntProperty(midiNote, prop, value)

    def selAllNotesTselection(command_id=40746, islistviewcommand=0):
        RPR_MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

    def deleteSelectedNotes(command_id=40002, islistviewcommand=0):
        RPR_MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

    def selAllNotes(command_id=40003, islistviewcommand=0):
        RPR_MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

    def addNote(midiTake, ch, vel, pos, pitch, length, sel):
        try:
            midiNote = FNG_AddMidiNote(midiTake)
            FNG_SetMidiNoteIntProperty(midiNote, "CHANNEL", ch)
            FNG_SetMidiNoteIntProperty(midiNote, "VELOCITY", vel)
            FNG_SetMidiNoteIntProperty(midiNote, "POSITION", pos)
            FNG_SetMidiNoteIntProperty(midiNote, "PITCH", pitch)
            FNG_SetMidiNoteIntProperty(midiNote, "LENGTH", length)
            FNG_SetMidiNoteIntProperty(midiNote, "SELECTED", sel)
            return midiNote
        except:
            RPR_ShowConsoleMsg('Could not draw notes!')
            return