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

import threading
import winsound
import time

from threading import Thread

class AUDIO(threading.Thread):

    def play(sound,len):
        try:
            winsound.PlaySound(sound,winsound.SND_FILENAME | winsound.SND_ASYNC)
            time.sleep(len)
            AUDIO.stop()
        except RuntimeError:
            pass

    def stop():
        winsound.PlaySound(None, 0)

    def beep(freq,len):
        try:
            winsound.Beep(freq, len)
        except RuntimeError:
            pass

    def ok():
        try:
            winsound.MessageBeep(winsound.MB_OK)
        except RuntimeError:
            pass

    def question():
        try:
            winsound.MessageBeep(winsound.MB_ICONQUESTION)
        except RuntimeError:
            pass

Thread(target=AUDIO).start()

