# mewsician CHIP code.

import CHIP_IO.GPIO as GPIO
from time import sleep
import subprocess
import datetime
import signal
import os

# TODO source authentication from device environment file
# TODO mechanism for creation / uploading of these??????

GPIO.cleanup()
outled = "XIO-P1"
channel = "XIO-P0"
GPIO.setup(outled, GPIO.OUT)
GPIO.output(outled, GPIO.LOW)
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.RISING)
print "Mewsician starting."
global recording, mpid
recording = False

def record():
    GPIO.output(outled, GPIO.HIGH)
    # trigger external recording and create a new subprocess for this
    # cmd = "arecord -f cd -D hw:0,0 -t raw | lame -x -r - - > " + fname
    # mpid = subprocess.Popen(['arecord', '-f', 'cd', '-D', 'hw:0,0', fname], stdout=PIPE, stderr=PIPE)
    print "Starting recording." # combine current time and uid
    fname = datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S") + '.mp3'
    print 'musicprocess pid is ', musicprocess.pid
    return (musicprocess.pid,  fname)

def upload(mpid):
    # trigger external uploading
    # will use userId and auth
    print "Stopping recording."
    print 'stop: musicprocess pid is ', mpid
    GPIO.output(outled, GPIO.LOW)
    # os.killpg(os.getpgid(mpid), signal.SIGTERM)

def trigger():
    if recording:
        upload(mpid)
        global recording
        recording = False
    else:
        mpid = record()
        global recording
        recording = True
        sleep(3) # wait for debouncing 3 secs, bad.

while True: # continually in this state
    if GPIO.event_detected(channel):
        print """ edge detected.
  |\      _,,,---,,_
  /,`.-'`'    -.  ;-;;,_
 |,4-  ) )-,_..;\ (  `'-'  MEOW!
'---''(_/--'  `-'\_)
        """
        trigger()
