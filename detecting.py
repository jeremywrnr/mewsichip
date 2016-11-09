<<<<<<< HEAD
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
=======
# adding an event trigger on the rising edge

import CHIP_IO.GPIO as GPIO

channel = "XIO-P0"
record = False

GPIO.setup(channel, GPIO.IN)
>>>>>>> encoding state

while True: # continually in this state
    GPIO.wait_for_edge(channel, GPIO.RISING)
    print "Button press detected =========="
    if record:
        print "Stopping recording."
        record = False
    else:
        print "Starting recording."
        record = True

GPIO.cleanup()
