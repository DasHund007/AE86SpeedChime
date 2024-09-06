import ac, acsys, sys, os
import time
import configparser
from math import log
from pydubInst.pydub import AudioSegment
from ctypes import c_buffer, windll
from random import random
from time   import sleep
from sys    import getfilesystemencoding

app_path = __file__
app_path = app_path.replace("\JDMSpeedChime.py", "/")

soundCooldown = 0

config = configparser.ConfigParser()
configFile = app_path + 'config.ini'
config.read(configFile)
app = config['APP']
chimeStartSpeed = int(app['chimeStartSpeed'])
chimeDelay = int(app['chimeDelay'])
chimeVolume = int(app['chimeVolume'])
sound_temp_path = app_path + 'temp_files/temp.wav'

def playsound(sound):

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command.decode() +
                                '\n    ' + errorBuffer.value.decode())
            raise PlaysoundException(exceptionMessage)
        return buf.value

    alias = 'playsound_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

def acMain(ac_version):
    speedChimeSoundfile = AudioSegment.from_file(app_path + 'speedChime.wav', format='wav')
    speedChimeSound = speedChimeSoundfile + ((chimeVolume-100)/10)
    fileHandle = speedChimeSound.export(sound_temp_path, format = 'wav')
    appWindow = ac.newApp("JDM Speed Chime")
    ac.setSize(appWindow,10,10)
    ac.console("JDM Speed Chime loaded!")
    return "JDM Speed Chime"

def acUpdate(deltaT):     
    global soundCooldown, chimeStartSpeed
    carSpeed = ac.getCarState(0,acsys.CS.SpeedKMH)
    if soundCooldown > 0:
        soundCooldown -= 1
    while carSpeed >= chimeStartSpeed and soundCooldown <= 0:
        playsound(sound_temp_path)
        soundCooldown += chimeDelay