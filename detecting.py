# adding an event trigger on the rising edge

import CHIP_IO.GPIO as GPIO
from time import sleep

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

GPIO.cleanup()
