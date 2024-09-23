#
# AE86 Speed Chime
# Created by Klayking
#
# Based upon code from RpmBeeper
# Written/Extended by:
#  TKu (AC Forum name)
#
# Based on:
#  http://www.assettocorsa.net/forum/index.php?threads/audible-gear-shift-beep.14237/
#  http://www.assettocorsa.net/forum/index.php?threads/app-request.7234/#post-103371
#
#
# Installation:
#  - Extract to your Assetto Corsa/apps/python directory
#  - Activate the app ingame
#

import ac, acsys
import sys
import math
import configparser , platform , os , os.path , traceback

if platform.architecture()[0] == "64bit":
	libdir = 'rpmbeeper_dll_x64'
else:
	libdir = 'rpmbeeper_dll_x86'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."


from rpmbeeper_third_party.sim_info import SimInfo
from sound_player import SoundPlayer

sim_info = SimInfo()

# sound
AUDIO_UP = os.path.join(os.path.dirname(__file__), "Chime3.wav")

# app window initialization
NAME = "AE86 Speed Chime"
WIDTH = 130
HEIGHT = 60
app = ac.newApp(NAME)
sound_player = SoundPlayer(AUDIO_UP)

# toggle beeper & controls
beeperEnabled = False
LABEL_TOGGLEBEEPER = "{}"
labelToggle = ac.addButton(app, "")

def acMain(ac_version):
	try:	
		
		ac.setSize(app, WIDTH, HEIGHT)

		# toogle control
		ac.setSize(labelToggle, 60, 20)
		ac.setPosition(labelToggle, 35, 30)
		ac.addOnClickedListener(labelToggle, on_click_toggle)
		ac.setBackgroundOpacity(labelToggle, 0.7)
		on_click_toggle(0)

		# remove app icon
		ac.setIconPosition(app, 0, -10000)
		

		return NAME   # say my name
	except Exception as e:
		ac.log("Meep_Meep: Error: %s" % e)

def acUpdate(dt):
	speed = ac.getCarState(0, acsys.CS.SpeedKMH)
	if speed > 100 and ac.getCarName(0) in ["ks_toyota_ae86", "ks_toyota_ae86_drift", "ks_toyota_ae86_tuned", "initiald_toyota_ae86"] and ac.isCameraOnBoard(0) and beeperEnabled:
		sound_player.play(AUDIO_UP)		
	else:
		sound_player.stop()


def on_click_toggle(*args):
    global beeperEnabled
    beeperEnabled = not beeperEnabled
    ac.setText(labelToggle, LABEL_TOGGLEBEEPER.format("on" if beeperEnabled else "off"))
