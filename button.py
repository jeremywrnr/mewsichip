from time import sleep
import os
import signal
import subprocess
import CHIP_IO.GPIO as GPIO
import datetime
from time import sleep

<<<<<<< HEAD
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
# include later:
# - meteor userId
# - authentication
channel = "XIO-P0"
recording = False

GPIO.setup(channel, GPIO.IN)
print "Mewsician starting."

def record():
    print "Starting recording."
    # trigger external recording
    # combine current time and uid

def upload():
    print "Stopping recording."
    # trigger external uploading
    # will use userId and auth

while True: # continually in this state

    # THIS SEEMS TO CATCH BOTH EDGES :///////
    GPIO.wait_for_edge(channel, GPIO.FALLING)
    print "Button press detected =========="

    if recording:
        upload()
        recording = False
    else:
        record()
        recording = True

    sleep(3) # wait for debouncing 3 secs, bad.
>>>>>>> well then

