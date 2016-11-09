from time import sleep
import os
import signal
import subprocess
import CHIP_IO.GPIO as GPIO
import datetime

# adding an event trigger on the rising edge

is_playing = False
global musicprocess

GPIO.setup("XIO-P0", GPIO.IN)
GPIO.add_event_detect("XIO-P0", GPIO.RISING)
if GPIO.event_detected("XIO-P0"):
    print "Rising edge detected ==========="
    if not is_playing:
        fname = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        musicprocess = subprocess.Popen(['arecord', '-f', 'cd', '-D', 'hw:0,0', fname], stdout=PIPE, stderr=PIPE)
        is_playing = True
    else:
        os.killpg(os.getpdig(musicprocess.pid), signal.SIGTERM)
        is_playing = False

