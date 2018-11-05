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

from tkinter import *
from tkinter import messagebox

class Helpers(object):

    def __init__(self):
        super(Helpers, self).__init__()

    def replace_all(self,text,dic):
        for i,j in enumerate(dic):
            text = text.replace(j, '')
        return text

    def splitInt(string):
        return [int(i) for i in str(string)]

    def reIndex(array,step):
        return list(enumerate(array, step))

    def toHex(self,dec):
        return hex(dec)[2:]

    def toDec(self,char):
        return int(ord(char))

    def toChar(self,dec):
        return str(char(dec))

    def hexToBytes(self,hex):
        return bytes.fromhex(hex)

    def hexToByteArray(self,hex):
        return bytearray.fromhex(hex)

    def strToHex(self,str=''):
        return ''.join(["\\x%02X" % ord(c) for c in str])

    def intToBytes(self,n, len):
        return ''.join([chr((n >> ((len - i - 1) * 8)) % 256) for i in range(len)])

    def bytesToStr(self,bytes):
        return bytes.decode(encoding="utf-8", errors="strict")

    def byteArrayToStr(self,bytearray):
        return bytearray.decode(encoding="utf-8", errors="strict")

    def readChunk(self, barray, start, step=1):
        chunk = barray[start:step]
        return chunk

    def readBytes(self, n_bytes=1, step=1):
        return Helpers.bytesToStr(Helpers.readChunk(n_bytes,step))

    def noteOn(self,note,velocity):
        return ['90',str(note),str(velocity)]

    def noteOff(self,note):
        return ['90',str(note),'00']

    def noteRest(self,delta):
        return Helpers.noteDelta(self,delta)

    def getDeltaInSeconds(self,delta,mpqn,ppqn):
        return delta * ((mpqn / int(float(1e6))) / ppqn)

    def noteDelta(self,n):
        # returns a list of variable length quantity hex.
        bucket = []
        while n > 0:
             buffer = n & 0x7F
             n      = n >> 7
             bucket.append(buffer + 0x80)
        for i in range(len(bucket)):
             if i == 0:
                 bucket[i] = int(bucket[i]) & 0x7F
             bucket[i] = hex(bucket[i])[2:].upper().zfill(2)
        return bucket[::-1]

    def writeChunk(self,digit,length):
        chunk = ''
        d = hex(int(digit))
        d = d[2:] if len(d) % 2 == 0 else '0' + d[2:]
        bytes = ' '.join(d[i:i+2] for i in range(0, len(d), 2))
        bucket = bytes.split()
        for i in range(len(bucket),length):
            chunk += '00 '
        chunk += bytes.upper()
        return chunk.split()

    def prName():
        (prj,_,prjName,_) = RPR_EnumProjects(-1, "", 10)
        pjname = prjName.rsplit('\\',1)
        return pjname[1].replace('.RPP','')

    def messageBox(title,value,method):

        if      method == 'info':
                messagebox.showinfo(title,value)
        elif    method == 'warning':
                messagebox.showwarning(title,value)
        elif    method == 'error':
                messagebox.showerror(title,value)
        elif    method == 'ask':
                messagebox.askyesno(title,value)
        elif    method == 'quit':
                messagebox.askokcancel("Quit", "Do you really wish to quit?")
        else:
                messagebox.showinfo(title,value)


