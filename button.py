from time import sleep
import os
import signal
import subprocess
import CHIP_IO.GPIO as GPIO
import datetime

# include later:
# - meteor userId
# - authentication
channel = "XIO-P0"
recording = False

GPIO.setup(channel, GPIO.IN)
print "Mewsician starting."
global musicprocess

def record():
    print "Starting recording."
    # combine current time and uid
    fname = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.mp3'
    # trigger external recording
    cmd = "arecord -f cd -D hw:0,0 -t raw | lame -x -r - - > " + fname
    musicprocess = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True )
    print 'musicprocess pid is ', musicprocess.pid

def upload():
    print "Stopping recording."
    print 'stop: musicprocess pid is ', musicprocess.pid
    os.killpg(os.getpgid(musicprocess.pid), signal.SIGTERM)
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
